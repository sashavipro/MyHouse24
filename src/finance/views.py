"""src/finance/views.py."""

import io
import logging

import openpyxl
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import IntegerField
from django.db.models import Max
from django.db.models import ProtectedError
from django.db.models import Sum
from django.db.models.functions import Cast
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from src.building.models import Apartment
from src.building.models import House
from src.finance.forms import ArticleForm
from src.finance.forms import CounterReadingForm
from src.finance.forms import PaymentDetailsForm
from src.finance.forms import PrintTemplateForm
from src.finance.forms import ReceiptForm
from src.finance.forms import ReceiptItemFormSet
from src.finance.forms import ServiceFormSet
from src.finance.forms import TariffForm
from src.finance.forms import TariffServiceFormSet
from src.finance.forms import UnitFormSet
from src.finance.models import Article
from src.finance.models import Counter
from src.finance.models import CounterReading
from src.finance.models import PaymentDetails
from src.finance.models import PrintTemplate
from src.finance.models import Receipt
from src.finance.models import Service
from src.finance.models import Tariff
from src.finance.models import Unit
from src.users.models import User
from src.users.permissions import Permissions

logger = logging.getLogger(__name__)


class AdminStatsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Display the main admin panel dashboard."""

    template_name = "core/adminlte/admin_stats.html"
    permission_required = Permissions.STATISTICS

    def get_context_data(self, **kwargs):
        """Add data required for the dashboard to the context."""
        return super().get_context_data(**kwargs)


class ManageServicesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Processes GET and POST requests for managing Services and Units of Measure.

    With correct handling of deletion errors.
    """

    template_name = "core/adminlte/admin_services.html"
    permission_required = Permissions.SERVICE

    def get(self, request, *args, **kwargs):
        """Display form sets for editing."""
        service_formset = ServiceFormSet(
            queryset=Service.objects.all().order_by("name"), prefix="services"
        )
        unit_formset = UnitFormSet(
            queryset=Unit.objects.all().order_by("name"), prefix="units"
        )

        context = {
            "service_formset": service_formset,
            "unit_formset": unit_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Save changes for one of the form sets."""
        if "save_services" in request.POST:
            formset = ServiceFormSet(request.POST, prefix="services")
            if formset.is_valid():
                try:
                    formset.save()
                    return redirect("finance:manage_services")
                except ProtectedError:
                    messages.error(
                        request,
                        "Невозможно удалить услугу, так как она используется в "
                        "квитанциях, счетчиках или тарифах.",
                    )

            unit_formset = UnitFormSet(
                queryset=Unit.objects.all().order_by("name"), prefix="units"
            )
            return render(
                request,
                self.template_name,
                {"service_formset": formset, "unit_formset": unit_formset},
            )

        if "save_units" in request.POST:
            formset = UnitFormSet(request.POST, prefix="units")
            if formset.is_valid():
                try:
                    formset.save()
                    return redirect("finance:manage_services")
                except ProtectedError:
                    messages.error(
                        request,
                        "It is not possible to delete the unit of measurement "
                        "because it is used in one or more services.",
                    )

            service_formset = ServiceFormSet(
                queryset=Service.objects.all().order_by("name"), prefix="services"
            )
            return render(
                request,
                self.template_name,
                {"service_formset": service_formset, "unit_formset": formset},
            )

        return redirect("finance:manage_services")


class TariffListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Display a list of tariffs."""

    model = Tariff
    template_name = "core/adminlte/tariff_list.html"
    permission_required = Permissions.TARIFF


class TariffDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Display detailed information about a single tariff."""

    model = Tariff
    template_name = "core/adminlte/tariff_detail.html"
    context_object_name = "tariff"
    permission_required = Permissions.TARIFF


class TariffCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Handle the creation of a new tariff."""

    model = Tariff
    form_class = TariffForm
    template_name = "core/adminlte/tariff_form.html"
    permission_required = Permissions.TARIFF

    def get_success_url(self):
        """Redirect to the detail page of the newly created tariff."""
        return reverse_lazy("finance:tariff_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add the services formset to the context."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["services_formset"] = TariffServiceFormSet(
                self.request.POST, prefix="services"
            )
        else:
            context["services_formset"] = TariffServiceFormSet(prefix="services")
        return context

    def form_valid(self, form):
        """Save the main form and the related formset if both are valid."""
        context = self.get_context_data(form=form)
        services_formset = context["services_formset"]
        if services_formset.is_valid():
            self.object = form.save()
            services_formset.instance = self.object
            services_formset.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)


class TariffUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Handle updating an existing tariff."""

    model = Tariff
    form_class = TariffForm
    template_name = "core/adminlte/tariff_form.html"
    permission_required = Permissions.TARIFF

    def get_success_url(self):
        """Redirect to the detail page of the updated tariff."""
        return reverse_lazy("finance:tariff_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add the pre-filled services formset to the context."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["services_formset"] = TariffServiceFormSet(
                self.request.POST, instance=self.object, prefix="services"
            )
        else:
            context["services_formset"] = TariffServiceFormSet(
                instance=self.object, prefix="services"
            )
        return context

    def form_valid(self, form):
        """Save the main form and the related formset if both are valid."""
        context = self.get_context_data(form=form)
        services_formset = context["services_formset"]
        if services_formset.is_valid():
            self.object = form.save()
            services_formset.instance = self.object
            services_formset.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)


class ArticleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Display the page with the list of payment articles."""

    model = Article
    template_name = "core/adminlte/article_list.html"
    permission_required = Permissions.ARTICLE


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Display the form for creating a new article."""

    model = Article
    form_class = ArticleForm
    template_name = "core/adminlte/article_form.html"
    success_url = reverse_lazy("finance:article_list")
    permission_required = Permissions.ARTICLE


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Display the form for editing an existing article."""

    model = Article
    form_class = ArticleForm
    template_name = "core/adminlte/article_form.html"
    success_url = reverse_lazy("finance:article_list")
    permission_required = Permissions.ARTICLE


class PaymentDetailsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Handle displaying and updating the singleton PaymentDetails object."""

    model = PaymentDetails
    form_class = PaymentDetailsForm
    template_name = "core/adminlte/payment_details_form.html"
    success_url = reverse_lazy("finance:payment_details")
    permission_required = Permissions.PAYMENT_DETAILS

    def get_object(self, queryset=None):
        """Return the single PaymentDetails instance, creating it if needed.

        This implements the singleton pattern for PaymentDetails.
        """
        obj, _created = self.model.objects.get_or_create(pk=1)
        return obj


class CounterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Display a page with a list of all counters."""

    model = Counter
    template_name = "core/adminlte/counter_list.html"
    permission_required = Permissions.COUNTERS

    def get_context_data(self, **kwargs):
        """Add data for filters to the context."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all().order_by("title")
        context["services"] = Service.objects.filter(show_in_counters=True).order_by(
            "name"
        )
        return context


class CounterReadingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Show a GENERAL list of all indications with the option to filter."""

    model = CounterReading
    template_name = "core/adminlte/counter_reading_list.html"
    permission_required = Permissions.COUNTERS

    def get_context_data(self, **kwargs):
        """Add data for filter dropdown lists to the context."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all().order_by("title")
        context["services"] = Service.objects.filter(show_in_counters=True).order_by(
            "name"
        )
        context["statuses"] = CounterReading.CounterStatus.choices

        return context


class CounterReadingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Processe the creation of a new meter reading."""

    model = CounterReading
    form_class = CounterReadingForm
    template_name = "core/adminlte/counter_reading_form.html"
    permission_required = Permissions.COUNTERS

    def get_success_url(self):
        """Define the URL for redirection after successful saving."""
        if "save_and_add_new" in self.request.POST:
            try:
                current_apartment = self.object.apartment
                next_apartment = (
                    Apartment.objects.filter(
                        house=current_apartment.house,
                        number__gt=current_apartment.number,
                    )
                    .order_by("number")
                    .first()
                )

                if next_apartment:
                    return (
                        reverse_lazy("finance:counter_reading_add")
                        + f"?apartment={next_apartment.pk}"
                    )
            except (AttributeError, Apartment.DoesNotExist):
                pass
            return reverse_lazy("finance:counter_reading_add")

        return (
            reverse_lazy("finance:counter_reading_list")
            + f"?counter={self.object.counter.pk}"
        )

    def get_context_data(self, **kwargs):
        """Add to the context of the home for the drop-down list."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all().order_by("title")
        if hasattr(self, "initial_data"):
            context["initial_data"] = self.initial_data
        return context

    def get_initial(self):
        """Prepare data for pre-filling fields in the form."""
        initial = super().get_initial()
        initial["date"] = timezone.localdate()

        apartment_id = self.request.GET.get("apartment")
        if apartment_id:
            try:
                apartment = Apartment.objects.select_related("house", "section").get(
                    pk=apartment_id
                )

                self.initial_data = {
                    "house_id": apartment.house_id,
                    "section_id": apartment.section_id if apartment.section else None,
                    "apartment_id": apartment.pk,
                }
            except Apartment.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        """Find or creates a counter before saving the reading."""
        apartment = form.cleaned_data.get("apartment")
        service = form.cleaned_data.get("service")

        if not apartment or not service:
            form.add_error(None, "Необходимо выбрать квартиру и услугу.")
            return self.form_invalid(form)

        counter, _created = Counter.objects.get_or_create(
            apartment=apartment,
            service=service,
            defaults={"serial_number": f"auto-{apartment.pk}-{service.pk}"},
        )

        reading = form.save(commit=False)
        reading.counter = counter

        self.object = reading
        reading.save()

        return redirect(self.get_success_url())


class CounterReadingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Processe editing of existing meter readings."""

    model = CounterReading
    form_class = CounterReadingForm
    template_name = "core/adminlte/counter_reading_form.html"
    permission_required = Permissions.COUNTERS

    def get_success_url(self):
        """After editing, always return to the history page."""
        return (
            reverse_lazy("finance:counter_reading_list")
            + f"?counter={self.object.counter.pk}"
        )

    def get_context_data(self, **kwargs):
        """Add data for pre-filling fields in JS."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all().order_by("title")
        context["initial_data"] = {
            "house_id": self.object.apartment.house_id,
            "section_id": self.object.apartment.section_id
            if self.object.apartment.section
            else None,
            "apartment_id": self.object.apartment.pk,
        }
        return context


class ReceiptListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Display a list of receipts with filters and statistics."""

    model = Receipt
    template_name = "core/adminlte/receipt_list.html"
    permission_required = Permissions.RECEIPT

    def get_context_data(self, **kwargs):
        """Add statistics and filter data to the context."""
        context = super().get_context_data(**kwargs)
        context["total_cash"] = 0
        context["total_balance"] = (
            Apartment.objects.aggregate(total=Sum("personal_account__balance"))["total"]
            or 0
        )
        context["total_debt"] = (
            Apartment.objects.filter(personal_account__balance__lt=0).aggregate(
                total=Sum("personal_account__balance")
            )["total"]
            or 0
        )
        context["owners"] = User.objects.filter(user_type="owner")
        context["statuses"] = Receipt.ReceiptStatus.choices
        return context


class ReceiptDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Show detailed information for a single receipt."""

    model = Receipt
    template_name = "core/adminlte/receipt_detail.html"
    permission_required = Permissions.RECEIPT


class ReceiptCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Creating a new receipt."""

    model = Receipt
    form_class = ReceiptForm
    template_name = "core/adminlte/receipt_form.html"
    permission_required = Permissions.RECEIPT

    def get_success_url(self):
        """Redirect to the detail page of the newly created receipt."""
        return reverse_lazy("finance:receipt_detail", kwargs={"pk": self.object.pk})

    def get_initial(self):
        """Prepare initial data for the form.

        Including the next receipt number and apartment details from the GET
        parameter.
        """
        initial = super().get_initial()

        result = Receipt.objects.aggregate(
            max_number=Max(Cast("number", output_field=IntegerField()))
        )

        last_number = result.get("max_number") or 0

        next_number = last_number + 1

        initial["number"] = str(next_number)

        apartment_id = self.request.GET.get("apartment")
        if apartment_id:
            try:
                apartment = Apartment.objects.select_related(
                    "house", "section", "personal_account", "tariff"
                ).get(pk=apartment_id)

                initial["apartment"] = apartment
                if apartment.tariff:
                    initial["tariff"] = apartment.tariff

                self.initial_data = {
                    "house_id": apartment.house_id,
                    "section_id": apartment.section_id if apartment.section else None,
                    "apartment_id": apartment.pk,
                }
            except Apartment.DoesNotExist:
                pass

        return initial

    def get_context_data(self, **kwargs):
        """Add data to the context for JavaScript pre-filling."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.order_by("title")
        context["tariffs"] = Tariff.objects.order_by("name")

        if hasattr(self, "initial_data"):
            context["initial_data"] = self.initial_data

        if self.request.POST:
            context["services_formset"] = ReceiptItemFormSet(
                self.request.POST, prefix="services"
            )
        else:
            context["services_formset"] = ReceiptItemFormSet(prefix="services")
        return context

    def form_valid(self, form):
        """Save the receipt and calculate the total amount from line items."""
        context = self.get_context_data(form=form)
        services_formset = context["services_formset"]
        if services_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.total_amount = 0
            self.object.save()

            services_formset.instance = self.object
            services_formset.save()

            total = (
                self.object.receiptitem_set.aggregate(total=Sum("amount"))["total"] or 0
            )
            self.object.total_amount = total
            self.object.save()

            return redirect(self.get_success_url())
        return self.form_invalid(form)


class ReceiptUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Editing an existing receipt with pre-filled fields."""

    model = Receipt
    form_class = ReceiptForm
    template_name = "core/adminlte/receipt_form.html"
    permission_required = Permissions.RECEIPT

    def get_success_url(self):
        """Redirect to the detail page of the updated receipt."""
        return reverse_lazy("finance:receipt_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add formset and JavaScript pre-fill data to the template context."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.order_by("title")
        context["tariffs"] = Tariff.objects.order_by("name")

        if self.object.apartment:
            apartment = self.object.apartment
            context["initial_data"] = {
                "house_id": apartment.house_id,
                "section_id": apartment.section_id if apartment.section else None,
                "apartment_id": apartment.pk,
            }

        if self.request.POST:
            context["services_formset"] = ReceiptItemFormSet(
                self.request.POST, instance=self.object, prefix="services"
            )
        else:
            context["services_formset"] = ReceiptItemFormSet(
                instance=self.object, prefix="services"
            )
        return context

    def form_valid(self, form):
        """Save the receipt and recalculate the total amount."""
        context = self.get_context_data(form=form)
        services_formset = context["services_formset"]
        if services_formset.is_valid():
            self.object = form.save()
            services_formset.instance = self.object
            services_formset.save()

            total = (
                self.object.receiptitem_set.aggregate(total=Sum("amount"))["total"] or 0
            )
            self.object.total_amount = total
            self.object.save()

            return redirect(self.get_success_url())
        return self.form_invalid(form)


class ReceiptPrintFormView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Show template selection page and generate Excel file from it."""

    template_name = "core/adminlte/receipt_print_form.html"
    permission_required = Permissions.RECEIPT

    def get(self, request, *args, **kwargs):
        """Display the template selection form."""
        receipt = get_object_or_404(Receipt, pk=kwargs["pk"])
        templates = PrintTemplate.objects.all().order_by("-is_default", "name")
        return render(
            request, self.template_name, {"receipt": receipt, "templates": templates}
        )

    def post(self, request, *args, **kwargs):
        """Process the download or upload of the generated Excel file."""
        receipt = get_object_or_404(
            Receipt.objects.select_related(
                "apartment__house",
                "apartment__section",
                "apartment__owner",
                "apartment__personal_account",
                "tariff",
            ),
            pk=kwargs["pk"],
        )
        template_id = request.POST.get("template_id")

        if not template_id:
            templates = PrintTemplate.objects.all().order_by("-is_default", "name")
            return render(
                request,
                self.template_name,
                {"receipt": receipt, "templates": templates},
            )

        template_obj = get_object_or_404(PrintTemplate, pk=template_id)

        try:
            workbook = self._generate_receipt_workbook(receipt, template_obj)

            if "download" in request.POST:
                return self._create_download_response(workbook, receipt)

            if "send_email" in request.POST:
                pass

        except Exception:
            logger.exception("Error generating receipt Excel file")

        templates = PrintTemplate.objects.all().order_by("-is_default", "name")
        return render(
            request, self.template_name, {"receipt": receipt, "templates": templates}
        )

    def _generate_receipt_workbook(self, receipt, template_obj):
        """Generate Excel workbook from receipt and template."""
        workbook = openpyxl.load_workbook(template_obj.template_file.path)
        sheet = workbook.active
        context = self._build_template_context(receipt)
        self._replace_template_variables(sheet, context)
        items = receipt.receiptitem_set.select_related("service__unit").all()
        template_row_idx = self._find_template_row(sheet)

        if template_row_idx and items:
            self._insert_receipt_items(sheet, template_row_idx, items)

        return workbook

    def _build_template_context(self, receipt):
        """Build context dictionary for template variable replacement."""
        status_map = {
            "paid": "Оплачена",
            "partially_paid": "Частично оплачена",
            "unpaid": "Неоплачена",
        }

        period = "—"
        if receipt.period_start and receipt.period_end:
            period = (
                f"{receipt.period_start.strftime('%d.%m.%Y')} "
                f"- {receipt.period_end.strftime('%d.%m.%Y')}"
            )

        return {
            "{{ receipt.is_posted }}": (
                "Conducted" if receipt.is_posted else "Not conducted"
            ),
            "{{ receipt.status }}": status_map.get(receipt.status, "—"),
            "{{ receipt.period }}": period,
            "{{ personal_account.number }}": (
                receipt.apartment.personal_account.number
                if receipt.apartment.personal_account
                else "—"
            ),
            "{{ owner.phone }}": (
                receipt.apartment.owner.phone
                if receipt.apartment.owner and receipt.apartment.owner.phone
                else "—"
            ),
            "{{ apartment.house }}": receipt.apartment.house.title,
            "{{ apartment.number }}": receipt.apartment.number,
            "{{ apartment.section }}": (
                receipt.apartment.section.name if receipt.apartment.section else "—"
            ),
            "{{ receipt.tariff }}": receipt.tariff.name if receipt.tariff else "—",
            "{{ receipt.total_amount }}": f"{receipt.total_amount:.2f}",
            "{{ receipt.number }}": receipt.number,
            "{{ receipt.date }}": receipt.date.strftime("%d.%m.%Y"),
            "{{ owner.full_name }}": (
                receipt.apartment.owner.get_full_name()
                if receipt.apartment.owner
                else "—"
            ),
        }

    def _replace_template_variables(self, sheet, context):
        """Replace template variables in sheet cells with actual values."""
        for row in sheet.iter_rows():
            for cell in row:
                if isinstance(cell.value, str):
                    for key, value in context.items():
                        if key in cell.value:
                            cell.value = cell.value.replace(key, str(value))

    def _find_template_row(self, sheet):
        """Find the row containing item template variables."""
        for i, row in enumerate(sheet.iter_rows(), 1):
            for cell in row:
                if isinstance(cell.value, str) and (
                    "{{ item.name }}" in cell.value or "{{ item.number }}" in cell.value
                ):
                    return i
        return None

    def _insert_receipt_items(self, sheet, template_row_idx, items):
        """Insert receipt items into the sheet using the template row."""
        template_row = sheet[template_row_idx]

        for i, item in enumerate(items, 1):
            sheet.insert_rows(template_row_idx + i)
            new_row = sheet[template_row_idx + i]

            self._copy_row_style(template_row, new_row)
            self._populate_item_row(new_row, template_row, item, i)

        sheet.delete_rows(template_row_idx)

    def _copy_row_style(self, template_row, new_row):
        """Copy cell styles from template row to new row."""
        for j, template_cell in enumerate(template_row, 1):
            new_cell = new_row[j - 1]
            if template_cell.has_style:
                new_cell.font = template_cell.font.copy()
                new_cell.border = template_cell.border.copy()
                new_cell.fill = template_cell.fill.copy()
                new_cell.number_format = template_cell.number_format
                new_cell.protection = template_cell.protection.copy()
                new_cell.alignment = template_cell.alignment.copy()

    def _populate_item_row(self, new_row, template_row, item, item_number):
        """Populate new row with receipt item data."""
        for j, template_cell in enumerate(template_row, 1):
            new_cell = new_row[j - 1]

            if not isinstance(template_cell.value, str):
                continue

            val_str = self._replace_item_placeholders(
                template_cell.value, item, item_number
            )

            try:
                numeric_placeholders = [
                    "{{ item.consumption }}",
                    "{{ item.price }}",
                    "{{ item.amount }}",
                    "{{ item.number }}",
                ]
                if any(p in template_cell.value for p in numeric_placeholders):
                    new_cell.value = float(val_str.replace(",", "."))
                else:
                    new_cell.value = val_str
            except (ValueError, TypeError):
                new_cell.value = val_str

    def _replace_item_placeholders(self, template_value, item, item_number):
        """Replace item placeholders with actual values."""
        return (
            template_value.replace("{{ item.number }}", str(item_number))
            .replace("{{ item.name }}", item.service.name)
            .replace(
                "{{ item.consumption }}",
                f"{item.consumption:.3f}" if item.consumption is not None else "",
            )
            .replace("{{ item.unit }}", item.service.unit.name)
            .replace(
                "{{ item.price }}",
                f"{item.price_per_unit:.2f}" if item.price_per_unit is not None else "",
            )
            .replace(
                "{{ item.amount }}",
                f"{item.amount:.2f}" if item.amount is not None else "",
            )
        )

    def _create_download_response(self, workbook, receipt):
        """Create HTTP response for downloading the Excel file."""
        virtual_workbook = io.BytesIO()
        workbook.save(virtual_workbook)
        virtual_workbook.seek(0)

        response = HttpResponse(
            virtual_workbook.read(),
            content_type=(
                "application/vnd.openxmlformats-officedocument." "spreadsheetml.sheet"
            ),
        )
        response["Content-Disposition"] = (
            f'attachment; filename="receipt_{receipt.number}.xlsx"'
        )
        return response


class ReceiptTemplateSettingsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Managing templates for printing receipts."""

    template_name = "core/adminlte/receipt_template_settings.html"
    permission_required = Permissions.RECEIPT

    def get(self, request, *args, **kwargs):
        """Handle GET requests for template management."""
        action = request.GET.get("action")
        template_id = request.GET.get("template_id")
        if template_id:
            template = get_object_or_404(PrintTemplate, pk=template_id)
            if action == "delete":
                template.delete()
                return redirect("finance:receipt_template_settings")
            if action == "set_default":
                template.is_default = True
                template.save()
                return redirect("finance:receipt_template_settings")

        form = PrintTemplateForm()
        templates = PrintTemplate.objects.all().order_by("-is_default", "name")
        return render(
            request, self.template_name, {"templates": templates, "form": form}
        )

    def post(self, request, *args, **kwargs):
        """Handle POST requests for creating new templates."""
        form = PrintTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("finance:receipt_template_settings")

        templates = PrintTemplate.objects.all().order_by("-is_default", "name")
        return render(
            request, self.template_name, {"templates": templates, "form": form}
        )
