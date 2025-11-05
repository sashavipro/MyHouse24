"""src/users/views.py."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import View

from src.building.models import House

from .forms import CustomUserForm
from .forms import OwnerForm
from .forms import RoleFormSet
from .models import Role
from .models import User


class AdminRolesPageView(LoginRequiredMixin, View):
    """Display and processes the form for editing all roles."""

    template_name = "core/adminlte/admin_roles_page.html"

    def setup(self, request, *args, **kwargs):
        """Ensure that a set of predefined roles exist in the database."""
        super().setup(request, *args, **kwargs)
        predefined_roles = [
            "Директор",
            "Управляющий",
            "Бухгалтер",
            "Электрик",
            "Сантехник",
        ]
        for role_name in predefined_roles:
            Role.objects.get_or_create(name=role_name)
        self.queryset = Role.objects.all().order_by("id")

    def get(self, request, *args, **kwargs):
        """Display a formset for editing roles and their permissions."""
        formset = RoleFormSet(queryset=self.queryset)
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Save changes to role permissions."""
        formset = RoleFormSet(request.POST, queryset=self.queryset)
        if formset.is_valid():
            formset.save()
            return redirect("users:admin_roles")

        context = {"formset": formset}
        return render(request, self.template_name, context)


class UserListView(LoginRequiredMixin, ListView):
    """Display the base template for the user list, populated by AJAX."""

    model = User
    template_name = "core/adminlte/user_list.html"

    def get_context_data(self, **kwargs):
        """Provide necessary data for filter dropdowns to the template."""
        context = super().get_context_data(**kwargs)
        context["all_roles"] = Role.objects.all()
        context["all_statuses"] = User.UserStatus.choices
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    """Display detailed information about a single user."""

    model = User
    template_name = "core/adminlte/user_detail.html"
    context_object_name = "user_obj"


class UserCreateView(LoginRequiredMixin, CreateView):
    """Handle the creation of a new user."""

    model = User
    form_class = CustomUserForm
    template_name = "core/adminlte/user_form.html"
    success_url = reverse_lazy("users:user_list")

    def get_context_data(self, **kwargs):
        """Add a page title to the context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Новый пользователь"
        return context

    def form_valid(self, form):
        """Set new user as staff and employee type before saving."""
        user = form.save(commit=False)
        user.is_staff = True
        user.user_type = "employee"
        user.save()
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Handle editing an existing user."""

    model = User
    form_class = CustomUserForm
    template_name = "core/adminlte/user_form.html"
    success_url = reverse_lazy("users:user_list")

    def get_context_data(self, **kwargs):
        """Add a page title and the user object to the context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование пользователя"
        context["user_obj"] = self.object
        return context


class OwnerListView(LoginRequiredMixin, ListView):
    """Displays the page with the list of owners, populated via AJAX."""

    model = User
    template_name = "core/adminlte/owner_list.html"

    def get_context_data(self, **kwargs):
        """Provide data for filter dropdowns to the template context."""
        context = super().get_context_data(**kwargs)
        context["all_houses"] = House.objects.all()
        context["all_statuses"] = User.UserStatus.choices
        return context


class OwnerDetailView(LoginRequiredMixin, DetailView):
    """Displays detailed information about an owner."""

    model = User
    template_name = "core/adminlte/owner_detail.html"
    context_object_name = "owner_obj"

    def get_queryset(self):
        """Ensure that only users of type 'owner' can be accessed."""
        return super().get_queryset().filter(user_type="owner")


class OwnerCreateView(LoginRequiredMixin, CreateView):
    """Handles the creation of a new owner."""

    model = User
    form_class = OwnerForm
    template_name = "core/adminlte/owner_form.html"
    success_url = reverse_lazy("users:owner_list")

    def get_context_data(self, **kwargs):
        """Add a page title to the context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Новый владелец"
        return context

    def form_valid(self, form):
        """Set the user type to 'owner' and saves the new user."""
        user = form.save(commit=False)
        user.user_type = User.UserType.OWNER
        user.is_staff = False
        user.save()
        return redirect(self.success_url)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """Handles editing an existing owner."""

    model = User
    form_class = OwnerForm
    template_name = "core/adminlte/owner_form.html"
    context_object_name = "owner_obj"

    def get_queryset(self):
        """Ensure that only users of type 'owner' can be accessed."""
        return super().get_queryset().filter(user_type="owner")

    def get_success_url(self):
        """Redirects to the owner's detail page after a successful update."""
        return reverse_lazy("users:owner_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add a page title to the context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование профиля владельца"
        return context
