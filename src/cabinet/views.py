"""src/cabinet/views.py."""

import datetime
import io
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db import transaction
from django.db.models import Avg
from django.db.models import Max
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView
from weasyprint import HTML
from xlsx2html import xlsx2html

from src.building.models import Apartment
from src.cabinet.forms import CabinetTicketForm
from src.cabinet.forms import PaymentCardForm
from src.core.utils import ReceiptExcelGenerator
from src.finance.models import Article
from src.finance.models import CashBox
from src.finance.models import PrintTemplate
from src.finance.models import Receipt
from src.finance.models import ReceiptItem
from src.finance.models import TariffService
from src.users.forms import OwnerProfileForm
from src.users.models import Message
from src.users.models import MessageRecipient
from src.users.models import Ticket
from src.users.models import User

logger = logging.getLogger(__name__)


class CabinetView(LoginRequiredMixin, DetailView):
    """Display the personal cabinet page for the currently logged-in owner."""

    model = User
    template_name = "core/adminlte/cabinet.html"
    context_object_name = "owner"

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user is an authenticated owner."""
        if (
            not request.user.is_authenticated
            or request.user.user_type != User.UserType.OWNER
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Return the currently logged-in user."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Add the owner's apartments to the context."""
        context = super().get_context_data(**kwargs)
        if self.object.user_type == User.UserType.OWNER:
            context["apartments"] = self.object.apartments.select_related(
                "house", "section", "floor", "personal_account"
            ).all()
        else:
            context["apartments"] = []
        return context


class CabinetUpdateView(LoginRequiredMixin, UpdateView):
    """Handle editing of the owner's own profile."""

    model = User
    form_class = OwnerProfileForm
    template_name = "core/adminlte/cabinet_form.html"
    success_url = reverse_lazy("cabinet:cabinet")

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user is an authenticated owner."""
        if (
            not request.user.is_authenticated
            or request.user.user_type != User.UserType.OWNER
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Ensure the user can only edit their own profile."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Add a page title to the context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование профиля"
        return context


class CabinetMessageListView(LoginRequiredMixin, ListView):
    """Display a page with a list of incoming messages for the owner.

    Data for the table is loaded via CabinetMessageAjaxDatatableView.
    """

    model = Message
    template_name = "core/adminlte/cabinet_message_list.html"
    context_object_name = "messages"

    def dispatch(self, request, *args, **kwargs):
        """Verify that only authenticated owners have access to the page."""
        if (
            not request.user.is_authenticated
            or request.user.user_type != User.UserType.OWNER
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return messages addressed to the current user (owner)."""
        return Message.objects.filter(recipients=self.request.user).order_by("-date")


class CabinetMessageDetailView(LoginRequiredMixin, DetailView):
    """Display one specific message for the owner.

    When viewed, marks it as read.
    """

    model = Message
    template_name = "core/adminlte/cabinet_message_detail.html"
    context_object_name = "message"

    def dispatch(self, request, *args, **kwargs):
        """Allow access only to authenticated owners."""
        if (
            not request.user.is_authenticated
            or request.user.user_type != User.UserType.OWNER
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Allow the owner to view only those messages where they are the recipient."""
        return Message.objects.filter(recipients=self.request.user)

    def get(self, request, *args, **kwargs):
        """Before displaying the page, marks the message as read."""
        response = super().get(request, *args, **kwargs)

        MessageRecipient.objects.filter(
            user=self.request.user, message=self.get_object(), is_read=False
        ).update(is_read=True)

        return response


class CabinetTariffDetailView(LoginRequiredMixin, DetailView):
    """Display services for a specific apartment tariff."""

    model = Apartment
    template_name = "core/adminlte/cabinet_tariff_detail.html"
    context_object_name = "apartment"
    pk_url_kwarg = "apartment_id"

    def get_queryset(self):
        """Allow the user to view only their own apartments.

        Optimized with select_related for the tariff.
        """
        return Apartment.objects.filter(owner=self.request.user).select_related(
            "tariff"
        )

    def get_context_data(self, **kwargs):
        """Add tariff services to the context."""
        context = super().get_context_data(**kwargs)
        apartment = self.object

        if apartment.tariff:
            context["tariff_services"] = (
                TariffService.objects.filter(tariff=apartment.tariff)
                .select_related("service", "service__unit")
                .order_by("service__name")
            )
        else:
            context["tariff_services"] = []

        return context


class CabinetReceiptListView(LoginRequiredMixin, ListView):
    """Display a list of receipts for the owner.

    Can show all receipts or receipts for a single apartment.
    """

    model = Receipt
    template_name = "core/adminlte/cabinet_receipt_list.html"

    def get_context_data(self, **kwargs):
        """Prepare the context for the template."""
        context = super().get_context_data(**kwargs)
        apartment_id = self.kwargs.get("apartment_id")

        if apartment_id:
            apartment = get_object_or_404(
                Apartment, pk=apartment_id, owner=self.request.user
            )
            context["page_title"] = (
                f"Квитанции: {apartment.house.title}, кв.{apartment.number}"
            )
            context["ajax_url"] = (
                reverse_lazy("cabinet:ajax_datatable_cabinet_receipts")
                + f"?apartment_id={apartment_id}"
            )
        else:
            context["page_title"] = "Все квитанции"  # noqa: RUF001
            context["ajax_url"] = reverse_lazy(
                "cabinet:ajax_datatable_cabinet_receipts"
            )

        context["receipt_statuses"] = Receipt.ReceiptStatus.choices
        return context


class CabinetReceiptDetailView(LoginRequiredMixin, DetailView):
    """Display detailed information on a single receipt for the owner."""

    model = Receipt
    template_name = "core/adminlte/cabinet_receipt_detail.html"
    context_object_name = "receipt"

    def get_queryset(self):
        """Allow the owner to see only receipts for their apartments."""
        return Receipt.objects.filter(apartment__owner=self.request.user)

    def get_context_data(self, **kwargs):
        """Add a list of services from the receipt to the context."""
        context = super().get_context_data(**kwargs)
        context["receipt_items"] = self.object.receiptitem_set.select_related(
            "service", "service__unit"
        ).all()
        return context


class CabinetTicketListView(LoginRequiredMixin, ListView):
    """Display the list of tickets for the owner."""

    model = Ticket
    template_name = "core/adminlte/cabinet_ticket_list.html"

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user is an authenticated owner."""
        if (
            not request.user.is_authenticated
            or request.user.user_type != User.UserType.OWNER
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CabinetTicketCreateView(LoginRequiredMixin, CreateView):
    """Create a new ticket by the owner."""

    model = Ticket
    form_class = CabinetTicketForm
    template_name = "core/adminlte/cabinet_ticket_form.html"
    success_url = reverse_lazy("cabinet:cabinet_ticket_list")

    def dispatch(self, request, *args, **kwargs):
        """Allow access only to owners."""
        if (
            not request.user.is_authenticated
            or request.user.user_type != User.UserType.OWNER
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Pass the current user to the form so it can filter apartments."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Automatically set the ticket owner."""
        try:
            with transaction.atomic():
                form.instance.user = self.request.user
                form.instance.status = Ticket.TicketStatus.NEW
                self.object = form.save()
        except (DatabaseError, ValidationError):
            return self.form_invalid(form)

        return redirect(self.get_success_url())


class ReceiptPdfView(LoginRequiredMixin, View):
    """Receiption pdf view."""

    def get(self, request, pk):
        """Get."""
        receipt = get_object_or_404(Receipt, pk=pk, apartment__owner=request.user)

        template = PrintTemplate.objects.filter(is_default=True).first()
        if not template:
            template = PrintTemplate.objects.first()

        if not template:
            return HttpResponse("Шаблон квитанции не найден.", status=404)

        # FIXED: TRY300 - Move success return to else block
        try:
            generator = ReceiptExcelGenerator(receipt, template.template_file.path)
            workbook = generator.generate_workbook()

            excel_buffer = io.BytesIO()
            workbook.save(excel_buffer)
            excel_buffer.seek(0)

            html_buffer = io.StringIO()
            xlsx2html(excel_buffer, html_buffer)
            raw_html = html_buffer.getvalue()

            custom_css = """
            <style>
                @page {
                    size: 250mm 300mm;

                    margin: 0;
                }

                body {
                    margin: 10mm;
                    padding: 0;

                    overflow: hidden;

                    background-color: white;
                }

                table {
                    border-collapse: collapse;
                    border-spacing: 0;
                }

                tr[height="0"], tr[style*="height:0"], tr[style*="height: 0"] {
                    display: none !important;
                }
            </style>
            """

            final_html_content = custom_css + raw_html

            pdf_file = HTML(
                string=final_html_content, base_url=request.build_absolute_uri()
            ).write_pdf()

        except (OSError, ValueError, RuntimeError) as e:
            logger.exception("Error generating PDF for receipt %s", receipt.number)
            return HttpResponse(f"Ошибка при формировании PDF: {e!s}", status=500)
        else:
            # Success path - only executes if no exception occurred
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="receipt_{receipt.number}.pdf"'
            )
            return response


class ReceiptPrintView(LoginRequiredMixin, View):
    """View to render the receipt as HTML and trigger the browser print dialog."""

    def get(self, request, pk):
        """Get."""
        receipt = get_object_or_404(Receipt, pk=pk, apartment__owner=request.user)

        template = PrintTemplate.objects.filter(is_default=True).first()
        if not template:
            template = PrintTemplate.objects.first()

        if not template:
            return HttpResponse("Шаблон квитанции не найден.", status=404)

        try:
            generator = ReceiptExcelGenerator(receipt, template.template_file.path)
            workbook = generator.generate_workbook()

            excel_buffer = io.BytesIO()
            workbook.save(excel_buffer)
            excel_buffer.seek(0)

            html_buffer = io.StringIO()
            xlsx2html(excel_buffer, html_buffer)
            html_content = html_buffer.getvalue()

            custom_html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Квитанция #{receipt.number}</title>
                <style>
                    /* Стили для печати */
                    @media print {{
                        @page {{
                            size: landscape; /* Альбомная ориентация */
                            margin: 1cm;
                        }}
                        body {{
                            -webkit-print-color-adjust: exact; /* Печатать цвета фона */
                            print-color-adjust: exact;
                        }}
                    }}
                    /* Общие стили для просмотра */
                    body {{
                        font-family: sans-serif;
                        margin: 0;
                        padding: 20px;
                    }}
                    /* Фик для таблицы, чтобы не уезжала */
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                </style>
            </head>
            <body>
                {html_content}
                <script>
                    // Автоматически вызываем окно печати при загрузке
                    window.onload = function() {{
                        window.print();
                    }}
                </script>
            </body>
            </html>
            """

            return HttpResponse(custom_html)

        except (OSError, ValueError, RuntimeError) as e:
            logger.exception(
                "Error generating Print View for receipt %s", receipt.number
            )
            return HttpResponse(f"Ошибка при подготовке к печати: {e!s}", status=500)


class CabinetSummaryView(LoginRequiredMixin, DetailView):
    """Summary page for a specific apartment of the owner."""

    model = Apartment
    template_name = "core/adminlte/cabinet_summary.html"
    context_object_name = "apartment"
    pk_url_kwarg = "apartment_id"

    def get_queryset(self):
        """Get queryset."""
        return Apartment.objects.filter(owner=self.request.user).select_related(
            "house", "section", "floor", "personal_account"
        )

    def get_context_data(self, **kwargs):
        """Get context."""
        context = super().get_context_data(**kwargs)
        apartment = self.object
        account = apartment.personal_account

        today = timezone.now()
        current_year = today.year

        balance = account.balance if account else 0.00
        context["account_balance"] = balance

        context["account_number"] = account.number if account else "Не привязан"  # noqa: RUF001

        avg_expense = (
            Receipt.objects.filter(
                apartment=apartment, date__year=current_year, status="paid"
            ).aggregate(avg=Avg("total_amount"))["avg"]
            or 0
        )

        context["avg_expense"] = avg_expense

        monthly_expenses = (
            Receipt.objects.filter(
                apartment=apartment, date__year=current_year, is_posted=True
            )
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("total_amount"))
            .order_by("month")
        )

        chart_data_year = [0.0] * 12
        chart_labels_year = []
        for i in range(1, 13):
            date_obj = datetime.date(current_year, i, 1)
            chart_labels_year.append(date_obj.strftime("%b %Y"))

            for entry in monthly_expenses:
                if entry["month"].month == i:
                    chart_data_year[i - 1] = float(entry["total"])
                    break

        context["chart_labels_year"] = chart_labels_year
        context["chart_data_year"] = chart_data_year

        category_expenses = (
            ReceiptItem.objects.filter(
                receipt__apartment=apartment,
                receipt__date__year=current_year,
                receipt__is_posted=True,
            )
            .values("service__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        chart_labels_pie = [item["service__name"] for item in category_expenses]
        chart_data_pie = [float(item["total"]) for item in category_expenses]

        context["chart_labels_pie"] = chart_labels_pie
        context["chart_data_pie"] = chart_data_pie

        return context


class PaymentSelectBankView(LoginRequiredMixin, DetailView):
    """Step 1: Select payment method."""

    model = Receipt
    template_name = "core/adminlte/payment_select_bank.html"
    context_object_name = "receipt"

    def get_queryset(self):
        """Get_queryset."""
        return Receipt.objects.filter(apartment__owner=self.request.user).exclude(
            status=Receipt.ReceiptStatus.PAID
        )


class PaymentProcessView(LoginRequiredMixin, FormView):
    """Step 2: Fake card processing."""

    template_name = "core/adminlte/payment_process.html"
    form_class = PaymentCardForm

    def dispatch(self, request, *args, **kwargs):
        """Dispatch."""
        self.receipt = get_object_or_404(
            Receipt, pk=self.kwargs["pk"], apartment__owner=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get_context_data."""
        ctx = super().get_context_data(**kwargs)
        ctx["receipt"] = self.receipt
        return ctx

    def form_valid(self, form):
        """Form_valid."""
        try:
            with transaction.atomic():
                last_id = CashBox.objects.aggregate(max_id=Max("id"))["max_id"] or 0
                new_number = f"{last_id + 1}".zfill(10)

                article, _ = Article.objects.get_or_create(
                    name="Оплата квитанции",
                    defaults={"type": Article.ArticleType.INCOME},
                )

                CashBox.objects.create(
                    number=new_number,
                    date=timezone.now().date(),
                    is_posted=True,
                    amount=self.receipt.total_amount,
                    article=article,
                    personal_account=self.receipt.apartment.personal_account,
                    receipt=self.receipt,
                    comment=f"Онлайн-оплата квитанции №{self.receipt.number}",
                )

                self.receipt.status = Receipt.ReceiptStatus.PAID
                self.receipt.save()

                if self.receipt.apartment.personal_account:
                    self.receipt.apartment.personal_account.balance += (
                        self.receipt.total_amount
                    )
                    self.receipt.apartment.personal_account.save()

            messages.success(
                self.request, f"Оплата квитанции №{self.receipt.number} прошла успешно!"
            )
            return redirect("cabinet:cabinet_receipt_list")

        except (DatabaseError, ValidationError) as e:
            logger.exception("Payment error for receipt %s", self.receipt.number)
            error_message = f"Ошибка при оплате: {e!s}"
            messages.error(self.request, error_message)
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Form invalid."""
        logger.warning("Payment form validation failed: %s", form.errors)
        return super().form_invalid(form)
