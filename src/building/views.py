"""src/building/views.py."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import FloorFormSet
from .forms import HouseForm
from .forms import HouseStaffFormSet
from .forms import SectionFormSet
from .models import House


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
