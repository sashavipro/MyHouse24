"""src/cabinet/views.py."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from src.building.models import Apartment
from src.cabinet.forms import CabinetTicketForm
from src.finance.models import Receipt
from src.finance.models import TariffService
from src.users.forms import OwnerProfileForm
from src.users.models import Message
from src.users.models import MessageRecipient
from src.users.models import Ticket
from src.users.models import User


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
