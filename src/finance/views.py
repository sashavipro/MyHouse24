"""src/finance/views.py."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from src.finance.forms import ServiceFormSet
from src.finance.forms import TariffForm
from src.finance.forms import TariffServiceFormSet
from src.finance.forms import UnitFormSet
from src.finance.models import Service
from src.finance.models import Tariff
from src.finance.models import Unit


class AdminStatsView(LoginRequiredMixin, TemplateView):
    """Display the main admin panel dashboard."""

    template_name = "core/adminlte/admin_stats.html"

    def get_context_data(self, **kwargs):
        """Add data required for the dashboard to the context."""
        return super().get_context_data(**kwargs)


class ManageServicesView(LoginRequiredMixin, View):
    """Handle GET and POST requests for managing Services and Units."""

    template_name = "core/adminlte/admin_services.html"

    def get(self, request, *args, **kwargs):
        """Display formsets for editing all services and units."""
        service_formset = ServiceFormSet(
            queryset=Service.objects.all(), prefix="services"
        )
        unit_formset = UnitFormSet(queryset=Unit.objects.all(), prefix="units")

        context = {
            "service_formset": service_formset,
            "unit_formset": unit_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Save changes for either the services or units formset."""
        if "save_services" in request.POST:
            formset = ServiceFormSet(request.POST, prefix="services")
            if formset.is_valid():
                formset.save()
                return redirect("finance:manage_services")

            unit_formset = UnitFormSet(queryset=Unit.objects.all(), prefix="units")
            return render(
                request,
                self.template_name,
                {"service_formset": formset, "unit_formset": unit_formset},
            )

        if "save_units" in request.POST:
            formset = UnitFormSet(request.POST, prefix="units")
            if formset.is_valid():
                formset.save()
                return redirect("finance:manage_services")

            service_formset = ServiceFormSet(
                queryset=Service.objects.all(), prefix="services"
            )
            return render(
                request,
                self.template_name,
                {"service_formset": service_formset, "unit_formset": formset},
            )
        return redirect("finance:manage_services")


class TariffListView(LoginRequiredMixin, ListView):
    """Displays a list of tariffs using a DataTables AJAX source."""

    model = Tariff
    template_name = "core/adminlte/tariff_list.html"


class TariffDetailView(LoginRequiredMixin, DetailView):
    """Displays detailed information about a single tariff."""

    model = Tariff
    template_name = "core/adminlte/tariff_detail.html"
    context_object_name = "tariff"


class TariffCreateView(LoginRequiredMixin, CreateView):
    """Handles the creation of a new tariff and its related services."""

    model = Tariff
    form_class = TariffForm
    template_name = "core/adminlte/tariff_form.html"

    def get_success_url(self):
        """Redirects to the detail page of the newly created tariff."""
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


class TariffUpdateView(LoginRequiredMixin, UpdateView):
    """Handles updating an existing tariff and its related services."""

    model = Tariff
    form_class = TariffForm
    template_name = "core/adminlte/tariff_form.html"

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
