"""src/building/views.py."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from src.users.models import User

from .forms import ApartmentForm
from .forms import FloorFormSet
from .forms import HouseForm
from .forms import HouseStaffFormSet
from .forms import PersonalAccountForm
from .forms import SectionFormSet
from .models import Apartment
from .models import House
from .models import PersonalAccount


class HouseListView(LoginRequiredMixin, ListView):
    """Display a list of houses using a DataTables AJAX source."""

    model = House
    template_name = "core/adminlte/house_list.html"


class HouseDetailView(LoginRequiredMixin, DetailView):
    """Display detailed information about a single house."""

    model = House
    template_name = "core/adminlte/house_detail.html"


class HouseCreateView(LoginRequiredMixin, CreateView):
    """Handle the creation of a new house and its related formsets."""

    model = House
    form_class = HouseForm
    template_name = "core/adminlte/house_form.html"

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
            self.object = form.save()
            section_formset.instance = self.object
            section_formset.save()
            floor_formset.instance = self.object
            floor_formset.save()
            staff_formset.instance = self.object
            staff_formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)


class HouseUpdateView(LoginRequiredMixin, UpdateView):
    """Handle updating an existing house and its related formsets."""

    model = House
    form_class = HouseForm
    template_name = "core/adminlte/house_form.html"

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
            self.object = form.save()
            section_formset.save()
            floor_formset.save()
            staff_formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)


class ApartmentListView(LoginRequiredMixin, ListView):
    """Displays the page with the list of apartments."""

    model = Apartment
    template_name = "core/adminlte/apartment_list.html"

    def get_context_data(self, **kwargs):
        """Add necessary data to the context for filtering."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()
        context["owners"] = User.objects.filter(user_type="owner")
        return context


class ApartmentDetailView(LoginRequiredMixin, DetailView):
    """Display detailed information about an apartment."""

    model = Apartment
    template_name = "core/adminlte/apartment_detail.html"
    context_object_name = "apartment"


class ApartmentCreateView(LoginRequiredMixin, CreateView):
    """Display the form for creating a new apartment."""

    model = Apartment
    form_class = ApartmentForm
    template_name = "core/adminlte/apartment_form.html"

    def get_success_url(self):
        """Determine the redirect URL after successful form submission."""
        if "save_and_add_new" in self.request.POST:
            return reverse_lazy("building:apartment_add")
        return reverse_lazy("building:apartment_list")

    def form_valid(self, form):
        """Handle the valid form submission."""
        return super().form_valid(form)


class ApartmentUpdateView(LoginRequiredMixin, UpdateView):
    """Displays the form for editing an apartment."""

    model = Apartment
    form_class = ApartmentForm
    template_name = "core/adminlte/apartment_form.html"

    def get_success_url(self):
        """Return the URL to redirect to after a successful update."""
        return reverse_lazy("building:apartment_detail", kwargs={"pk": self.object.pk})


class PersonalAccountListView(LoginRequiredMixin, ListView):
    """Display the page with the list of personal accounts."""

    model = PersonalAccount
    template_name = "core/adminlte/personal_account_list.html"

    def get_context_data(self, **kwargs):
        """Add data for filters and statistics cards to the context."""
        context = super().get_context_data(**kwargs)

        context["houses"] = House.objects.all().order_by("title")
        context["owners"] = User.objects.filter(user_type="owner").order_by(
            "last_name", "first_name"
        )

        context["total_accounts_balance"] = (
            PersonalAccount.objects.aggregate(Sum("balance"))["balance__sum"] or 0
        )

        context["total_debt"] = (
            PersonalAccount.objects.filter(balance__lt=0).aggregate(Sum("balance"))[
                "balance__sum"
            ]
            or 0
        )

        context["total_balance"] = context["total_accounts_balance"]

        return context


class PersonalAccountDetailView(LoginRequiredMixin, DetailView):
    """Displays detailed information about a personal account."""

    model = PersonalAccount
    template_name = "core/adminlte/personal_account_detail.html"
    context_object_name = "account"


class PersonalAccountCreateView(LoginRequiredMixin, CreateView):
    """Displays the form for creating a new personal account."""

    model = PersonalAccount
    form_class = PersonalAccountForm
    template_name = "core/adminlte/personal_account_form.html"
    success_url = reverse_lazy("building:personal_account_list")

    def get_context_data(self, **kwargs):
        """Add necessary data for the form to the context."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()
        return context

    def form_valid(self, form):
        """Handle the logic after a valid form submission."""
        self.object = form.save()
        apartment_id = form.cleaned_data.get("apartment")
        if apartment_id:
            try:
                apartment = Apartment.objects.get(pk=apartment_id)
                apartment.personal_account = self.object
                apartment.save()
            except Apartment.DoesNotExist:
                pass
        return super().form_valid(form)


class PersonalAccountUpdateView(LoginRequiredMixin, UpdateView):
    """Display the form for editing a personal account."""

    model = PersonalAccount
    form_class = PersonalAccountForm
    template_name = "core/adminlte/personal_account_form.html"

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
