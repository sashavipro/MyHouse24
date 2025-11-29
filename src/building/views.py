"""src/building/views.py."""

import openpyxl
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from openpyxl.styles import Font

from src.finance.models import CashBox
from src.users.models import User
from src.users.models import logger
from src.users.permissions import RoleRequiredMixin

from .forms import ApartmentForm
from .forms import FloorFormSet
from .forms import HouseForm
from .forms import HouseStaffFormSet
from .forms import PersonalAccountForm
from .forms import SectionFormSet
from .models import Apartment
from .models import House
from .models import PersonalAccount


class HouseListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    """Display a list of houses using a DataTables AJAX source."""

    model = House
    template_name = "core/adminlte/house_list.html"
    permission_required = "has_house"


class HouseDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    """Display detailed information about a single house."""

    model = House
    template_name = "core/adminlte/house_detail.html"
    permission_required = "has_house"


class HouseCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Handle the creation of a new house and its related formsets."""

    model = House
    form_class = HouseForm
    template_name = "core/adminlte/house_form.html"
    permission_required = "has_house"

    def get_success_url(self):
        """Return the URL to redirect to after successful creation."""
        return reverse_lazy("building:house_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add formsets for sections, floors, and staff to the context."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["section_formset"] = SectionFormSet(
                self.request.POST, prefix="sections"
            )
            context["floor_formset"] = FloorFormSet(self.request.POST, prefix="floors")
            context["staff_formset"] = HouseStaffFormSet(
                self.request.POST, prefix="staff"
            )
        else:
            context["section_formset"] = SectionFormSet(prefix="sections")
            context["floor_formset"] = FloorFormSet(prefix="floors")
            context["staff_formset"] = HouseStaffFormSet(prefix="staff")
        return context

    def form_valid(self, form):
        """Validate and saves the main form and all related formsets."""
        context = self.get_context_data()
        section_formset = context["section_formset"]
        floor_formset = context["floor_formset"]
        staff_formset = context["staff_formset"]

        if all(
            [
                section_formset.is_valid(),
                floor_formset.is_valid(),
                staff_formset.is_valid(),
            ]
        ):
            try:
                with transaction.atomic():
                    self.object = form.save()
                    section_formset.instance = self.object
                    section_formset.save()
                    floor_formset.instance = self.object
                    floor_formset.save()
                    staff_formset.instance = self.object
                    staff_formset.save()
            except (DatabaseError, ValidationError) as e:  # Fixed BLE001
                logger.error("Error creating house: %s", e)
                return self.form_invalid(form)

            return super().form_valid(form)
        return self.form_invalid(form)


class HouseUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Handle updating an existing house."""

    model = House
    form_class = HouseForm
    template_name = "core/adminlte/house_form.html"
    permission_required = "has_house"

    def get_success_url(self):
        """Return the URL to redirect to after a successful update."""
        return reverse_lazy("building:house_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add pre-filled formsets for sections, floors, and staff."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["section_formset"] = SectionFormSet(
                self.request.POST, instance=self.object, prefix="sections"
            )
            context["floor_formset"] = FloorFormSet(
                self.request.POST, instance=self.object, prefix="floors"
            )
            context["staff_formset"] = HouseStaffFormSet(
                self.request.POST, instance=self.object, prefix="staff"
            )
        else:
            context["section_formset"] = SectionFormSet(
                instance=self.object, prefix="sections"
            )
            context["floor_formset"] = FloorFormSet(
                instance=self.object, prefix="floors"
            )
            context["staff_formset"] = HouseStaffFormSet(
                instance=self.object, prefix="staff"
            )
        return context

    def form_valid(self, form):
        """Validate and saves the main form and all related formsets."""
        context = self.get_context_data()
        section_formset = context["section_formset"]
        floor_formset = context["floor_formset"]
        staff_formset = context["staff_formset"]

        if all(
            [
                section_formset.is_valid(),
                floor_formset.is_valid(),
                staff_formset.is_valid(),
            ]
        ):
            try:
                with transaction.atomic():
                    self.object = form.save()
                    section_formset.save()
                    floor_formset.save()
                    staff_formset.save()
            except (DatabaseError, ValidationError) as e:  # Fixed BLE001
                logger.error("Error updating house: %s", e)
                return self.form_invalid(form)

            return super().form_valid(form)
        return self.form_invalid(form)


class ApartmentListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    """Display the page with the list of apartments."""

    model = Apartment
    template_name = "core/adminlte/apartment_list.html"
    permission_required = "has_apartment"

    def get_context_data(self, **kwargs):
        """Add necessary data to the context for filtering."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()
        context["owners"] = User.objects.filter(user_type="owner")
        return context


class ApartmentDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    """Display detailed information about an apartment."""

    model = Apartment
    template_name = "core/adminlte/apartment_detail.html"
    context_object_name = "apartment"
    permission_required = "has_apartment"


class ApartmentCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Display the form for creating a new apartment."""

    model = Apartment
    form_class = ApartmentForm
    template_name = "core/adminlte/apartment_form.html"
    permission_required = "has_apartment"

    def get_success_url(self):
        """Determine the redirect URL after successful form submission."""
        if "save_and_add_new" in self.request.POST:
            return reverse_lazy("building:apartment_add")
        return reverse_lazy("building:apartment_list")

    def form_valid(self, form):
        """Handle the valid form submission."""
        with transaction.atomic():
            return super().form_valid(form)


class ApartmentUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Displays the form for editing an apartment."""

    model = Apartment
    form_class = ApartmentForm
    template_name = "core/adminlte/apartment_form.html"
    permission_required = "has_apartment"

    def form_valid(self, form):
        """Handle the valid form submission."""
        with transaction.atomic():
            return super().form_valid(form)


class PersonalAccountListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    """Display the page with the list of personal accounts."""

    model = PersonalAccount
    template_name = "core/adminlte/personal_account_list.html"
    permission_required = "has_personal_account"

    def get_context_data(self, **kwargs):
        """Add data for filters and statistics cards to the context."""
        context = super().get_context_data(**kwargs)

        context["houses"] = House.objects.all().order_by("title")
        context["owners"] = User.objects.filter(user_type="owner").order_by(
            "last_name", "first_name"
        )

        income = (
            CashBox.objects.filter(is_posted=True, article__type="income").aggregate(
                s=Sum("amount")
            )["s"]
            or 0
        )
        expense = (
            CashBox.objects.filter(is_posted=True, article__type="expense").aggregate(
                s=Sum("amount")
            )["s"]
            or 0
        )
        context["total_cash"] = income - expense

        context["total_balance_accounts"] = (
            Apartment.objects.aggregate(total=Sum("personal_account__balance"))["total"]
            or 0
        )
        context["total_debt"] = (
            Apartment.objects.filter(personal_account__balance__lt=0).aggregate(
                total=Sum("personal_account__balance")
            )["total"]
            or 0
        )

        return context


class PersonalAccountDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    """Displays detailed information about a personal account."""

    model = PersonalAccount
    template_name = "core/adminlte/personal_account_detail.html"
    context_object_name = "account"
    permission_required = "has_personal_account"


class PersonalAccountCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Displays the form for creating a new personal account."""

    model = PersonalAccount
    form_class = PersonalAccountForm
    template_name = "core/adminlte/personal_account_form.html"
    success_url = reverse_lazy("building:personal_account_list")
    permission_required = "has_personal_account"

    def get_context_data(self, **kwargs):
        """Add necessary data for the form to the context."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()
        return context

    def form_valid(self, form):
        """Handle the logic after a valid form submission."""
        try:
            with transaction.atomic():
                self.object = form.save()
                apartment_id = form.cleaned_data.get("apartment")
                if apartment_id:
                    try:
                        apartment = Apartment.objects.get(pk=apartment_id)
                        apartment.personal_account = self.object
                        apartment.save()
                    except Apartment.DoesNotExist:
                        pass
        except (DatabaseError, ValidationError) as e:  # Fixed BLE001
            logger.error("Error creating personal account: %s", e)
            return self.form_invalid(form)

        return super().form_valid(form)


class PersonalAccountUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Display the form for editing a personal account."""

    model = PersonalAccount
    form_class = PersonalAccountForm
    template_name = "core/adminlte/personal_account_form.html"
    permission_required = "has_personal_account"

    def get_success_url(self):
        """Return the URL to redirect to after a successful update."""
        return reverse_lazy(
            "building:personal_account_detail", kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        """Add data for the form and initial pre-filling to the context."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()

        if hasattr(self.object, "apartment") and self.object.apartment:
            apartment = self.object.apartment
            context["initial_data"] = {
                "house_id": apartment.house_id,
                "section_id": apartment.section_id,
                "apartment_id": apartment.pk,
            }

        return context

    def form_valid(self, form):
        """Handle the valid form submission with atomic transaction."""  # Fixed D102
        with transaction.atomic():
            return super().form_valid(form)


class ExportPersonalAccountsExcelView(LoginRequiredMixin, RoleRequiredMixin, View):
    """Handle the export of personal accounts to an Excel file."""

    permission_required = "has_personal_account"

    def filter_queryset(self, request):
        """Apply filters from request parameters to the queryset."""
        queryset = PersonalAccount.objects.all().order_by("pk")

        filters_map = {
            "number": ("number__icontains", str),
            "status": ("status", str),
            "apartment_number": ("apartment__number__icontains", str),
            "house": ("apartment__house_id", str),
            "section": ("apartment__section_id", str),
            "owner": ("apartment__owner_id", str),
        }

        for param, (field, cast) in filters_map.items():
            value = request.GET.get(param, "").strip()
            if value:
                queryset = queryset.filter(**{field: cast(value)})

        balance = request.GET.get("balance", "").strip()
        if balance:
            if balance == "debt":
                queryset = queryset.filter(balance__lt=0)
            elif balance == "no_debt":
                queryset = queryset.filter(balance__gte=0)
            elif balance == "zero":
                queryset = queryset.filter(balance=0)

        return queryset

    def get(self, request, *args, **kwargs):
        """Generate and return an Excel file with filtered personal account data."""
        queryset = self.filter_queryset(request)

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Лицевые счета"

        headers = [
            "№",
            "Статус",
            "Квартира",
            "Дом",
            "Секция",
            "Владелец",
            "Остаток (грн)",
        ]
        sheet.append(headers)

        for cell in sheet[1]:
            cell.font = Font(bold=True)

        for account in queryset:
            apt = getattr(account, "apartment", None)

            row_data = [
                account.number,
                "Активен" if account.status == "active" else "Неактивен",
                getattr(apt, "number", "(не задано)") if apt else "(не задано)",
                getattr(apt.house, "title", "(не задано)")
                if apt and apt.house
                else "(не задано)",
                getattr(apt.section, "name", "(не задано)")
                if apt and apt.section
                else "(не задано)",
                apt.owner.get_full_name() if apt and apt.owner else "(не задано)",
                account.balance,
            ]
            sheet.append(row_data)

        column_widths = [20, 15, 15, 25, 20, 35, 20]
        for i, width in enumerate(column_widths, 1):
            sheet.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            'attachment; filename="personal_accounts.xlsx"'
        )

        workbook.save(response)
        return response
