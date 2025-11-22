"""src/users/views.py."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db import IntegrityError
from django.db import transaction
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
from .forms import MessageForm
from .forms import OwnerForm
from .forms import RoleFormSet
from .forms import TicketForm
from .models import Message
from .models import Role
from .models import Ticket
from .models import User
from .permissions import RoleRequiredMixin


class AdminRolesPageView(LoginRequiredMixin, View):
    """Display and processes the form for editing all roles."""

    template_name = "core/adminlte/admin_roles_page.html"

    def dispatch(self, request, *args, **kwargs):
        """We check access rights manually.

        Access is granted to:
        1. Superusers.
        2. Users with the “Director” role.
        3. Users whose role has the has_role flag.
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        user_role = getattr(request.user, "role", None)

        if not user_role:
            messages.error(
                request,
                "У вас нет прав для доступа к этой странице.",  # noqa: RUF001
            )
            return redirect(getattr(request, "user_home_url", None) or "core:login")

        if user_role.name == "Директор" or user_role.has_role:
            return super().dispatch(request, *args, **kwargs)

        messages.error(
            request,
            "У вас нет прав для доступа к этой странице.",  # noqa: RUF001
        )
        return redirect(getattr(request, "user_home_url", None) or "core:login")

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
        """Save changes to roles."""
        formset = RoleFormSet(request.POST, queryset=self.queryset)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
            except (DatabaseError, IntegrityError):
                messages.error(request, "Произошла ошибка при сохранении ролей.")
                return render(request, self.template_name, {"formset": formset})

            messages.success(request, "Права ролей успешно обновлены.")
            return redirect("users:admin_roles")

        context = {"formset": formset}
        return render(request, self.template_name, context)


class UserListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    """Display the base template for the user list."""

    model = User
    template_name = "core/adminlte/user_list.html"
    permission_required = "has_user"

    def get_context_data(self, **kwargs):
        """Provide necessary data for filter dropdowns to the template."""
        context = super().get_context_data(**kwargs)
        context["all_roles"] = Role.objects.all()
        context["all_statuses"] = User.UserStatus.choices
        return context


class UserDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    """Display detailed information about a single user."""

    model = User
    template_name = "core/adminlte/user_detail.html"
    context_object_name = "user_obj"
    permission_required = "has_user"


class UserCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Handle the creation of a new user."""

    model = User
    form_class = CustomUserForm
    template_name = "core/adminlte/user_form.html"
    success_url = reverse_lazy("users:user_list")
    permission_required = "has_user"

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


class UserUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Handle editing an existing user."""

    model = User
    form_class = CustomUserForm
    template_name = "core/adminlte/user_form.html"
    success_url = reverse_lazy("users:user_list")
    permission_required = "has_user"

    def get_context_data(self, **kwargs):
        """Add a page title and the user object to the context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование пользователя"
        context["user_obj"] = self.object
        return context


class OwnerListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    """Display the page with the list of owners."""

    model = User
    template_name = "core/adminlte/owner_list.html"
    permission_required = "has_owner"

    def get_context_data(self, **kwargs):
        """Provide data for filter dropdowns to the template context."""
        context = super().get_context_data(**kwargs)
        context["all_houses"] = House.objects.all()
        context["all_statuses"] = User.UserStatus.choices
        return context


class OwnerDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    """Display detailed information about an owner."""

    model = User
    template_name = "core/adminlte/owner_detail.html"
    context_object_name = "owner_obj"
    permission_required = "has_owner"

    def get_queryset(self):
        """Ensure that only users of type 'owner' can be accessed."""
        return super().get_queryset().filter(user_type="owner")


class OwnerCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Handle the creation of a new owner."""

    model = User
    form_class = OwnerForm
    template_name = "core/adminlte/owner_form.html"
    success_url = reverse_lazy("users:owner_list")
    permission_required = "has_owner"

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


class OwnerUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Handle editing an existing owner."""

    model = User
    form_class = OwnerForm
    template_name = "core/adminlte/owner_form.html"
    context_object_name = "owner_obj"
    permission_required = "has_owner"

    def get_queryset(self):
        """Ensure that only users of type 'owner' can be accessed."""
        return super().get_queryset().filter(user_type="owner")

    def get_success_url(self):
        """Redirect to the owner's detail page after a successful update."""
        return reverse_lazy("users:owner_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add a page title to the context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование профиля владельца"
        return context


class MessageListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    """List of sent messages for the administrator/employee."""

    model = Message
    template_name = "core/adminlte/message_list.html"
    permission_required = "has_message"

    def get_queryset(self):
        """Return messages sent by the employee."""
        return Message.objects.filter(sender=self.request.user)


class MessageDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    """Display one specific message for an employee (admin panel)."""

    model = Message
    template_name = "core/adminlte/message_detail.html"
    context_object_name = "message"
    permission_required = "has_message"

    def get_queryset(self):
        """Return only messages sent by the employee."""
        return Message.objects.filter(sender=self.request.user)

    def get_context_data(self, **kwargs):
        """Add a variable for the base template to the context."""
        context = super().get_context_data(**kwargs)
        context["base_layout"] = "core/adminlte/admin_layout.html"
        context["list_url"] = reverse_lazy("users:message_list")
        return context


class MessageCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Create a new message. Available only to employees."""

    model = Message
    form_class = MessageForm
    template_name = "core/adminlte/message_form.html"
    permission_required = "has_message"
    success_url = reverse_lazy("users:message_list")

    def get_context_data(self, **kwargs):
        """Add available houses to the context."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()
        return context

    def form_valid(self, form):
        """Save the message with sender and recipients."""
        try:
            with transaction.atomic():
                final_recipients = form.cleaned_data["final_recipients"]

                self.object = form.save(commit=False)
                self.object.sender = self.request.user
                self.object.save()

                self.object.recipients.set(final_recipients)
        except (DatabaseError, IntegrityError):
            return self.form_invalid(form)

        return super(CreateView, self).form_valid(form)


class TicketListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    """List of tickets for administrators."""

    model = Ticket
    template_name = "core/adminlte/ticket_list.html"
    permission_required = "has_ticket"

    def get_context_data(self, **kwargs):
        """Provide necessary data for filter dropdowns to the template context."""
        context = super().get_context_data(**kwargs)
        context["all_roles"] = Role.objects.all()
        context["all_owners"] = User.objects.filter(user_type=User.UserType.OWNER)
        context["all_masters"] = User.objects.filter(user_type=User.UserType.EMPLOYEE)
        return context


class TicketCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Create a new ticket by administrator."""

    model = Ticket
    form_class = TicketForm
    template_name = "core/adminlte/ticket_form.html"
    permission_required = "has_ticket"
    success_url = reverse_lazy("users:ticket_list")

    def get_context_data(self, **kwargs):
        """Add houses and initial data to context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Новая заявка"
        context["houses"] = House.objects.all()

        context["initial_data"] = {
            "house_id": "",
            "section_id": "",
            "floor_id": "",
            "apartment_id": "",
        }

        return context

    def form_valid(self, form):
        """Process the form before saving using atomic transaction."""
        try:
            with transaction.atomic():
                if form.cleaned_data.get("user"):
                    form.instance.phone = form.cleaned_data["user"].phone or ""

                self.object = form.save()
        except (DatabaseError, ValidationError) as e:
            messages.error(self.request, f"Ошибка при сохранении: {e}")
            return self.form_invalid(form)

        messages.success(self.request, "Заявка успешно создана")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме")
        return super().form_invalid(form)


class TicketUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Edit an existing ticket."""

    model = Ticket
    form_class = TicketForm
    template_name = "core/adminlte/ticket_form.html"
    permission_required = "has_ticket"

    def get_success_url(self):
        """Redirect to ticket detail page after successful update."""
        return reverse_lazy("users:ticket_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add houses and initial data to context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование заявки №{self.object.pk}"
        context["houses"] = House.objects.all()

        apartment = self.object.apartment
        initial_data = {
            "house_id": "",
            "section_id": "",
            "floor_id": "",
            "apartment_id": "",
        }

        if apartment:
            initial_data["apartment_id"] = apartment.pk

            if apartment.house:
                initial_data["house_id"] = apartment.house.pk

            if apartment.section:
                initial_data["section_id"] = apartment.section.pk

            if apartment.floor:
                initial_data["floor_id"] = apartment.floor.pk

        context["initial_data"] = initial_data

        return context

    def form_valid(self, form):
        """Process the form before saving using atomic transaction."""
        try:
            with transaction.atomic():
                if "house" in form.cleaned_data:
                    form.cleaned_data.pop("house")

                if not form.cleaned_data.get("phone") and form.cleaned_data.get("user"):
                    form.instance.phone = form.cleaned_data["user"].phone or ""

                self.object = form.save()
        except (DatabaseError, ValidationError) as e:
            messages.error(self.request, f"Ошибка при сохранении: {e}")
            return self.form_invalid(form)

        messages.success(self.request, "Заявка успешно обновлена")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме")
        return super().form_invalid(form)


class TicketDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    """Display detailed information about a ticket."""

    model = Ticket
    template_name = "core/adminlte/ticket_detail.html"
    permission_required = "has_ticket"
    context_object_name = "ticket"
