"""src/users/views.py."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import View

from .forms import CustomUserForm
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


class GetUserRoleApiView(LoginRequiredMixin, View):
    """Return the user's role in JSON format for AJAX requests."""

    def get(self, request, *args, **kwargs):
        """Find a user by ID and returns their role name."""
        user_id = request.GET.get("user_id")
        if not user_id:
            return JsonResponse({"error": "User ID not provided"}, status=400)
        try:
            user = User.objects.get(id=user_id)
            role_name = user.role.name if user.role else "Роль не назначена"
            return JsonResponse({"role_name": role_name})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
