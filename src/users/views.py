"""src/users/views.py."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import View

from src.building.models import Apartment
from src.building.models import House
from src.finance.models import ReceiptItem
from src.finance.models import TariffService

from .forms import CustomUserForm
from .forms import MessageForm
from .forms import OwnerForm
from .forms import OwnerProfileForm
from .forms import RoleFormSet
from .models import Message
from .models import MessageRecipient
from .models import Role
from .models import User
from .permissions import Permissions
from .permissions import sync_role_with_group


class AdminRolesPageView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Display and processes the form for editing all roles."""

    template_name = "core/adminlte/admin_roles_page.html"
    permission_required = "users.change_group"

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
        """Save changes to role permissions and synchronizes with Django groups."""
        formset = RoleFormSet(request.POST, queryset=self.queryset)
        if formset.is_valid():
            saved_roles = formset.save()
            for role in saved_roles:
                sync_role_with_group(role)

        context = {"formset": formset}
        return render(request, self.template_name, context)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Display the base template for the user list."""

    model = User
    template_name = "core/adminlte/user_list.html"
    permission_required = Permissions.USER

    def get_context_data(self, **kwargs):
        """Provide necessary data for filter dropdowns to the template."""
        context = super().get_context_data(**kwargs)
        context["all_roles"] = Role.objects.all()
        context["all_statuses"] = User.UserStatus.choices
        return context


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Display detailed information about a single user."""

    model = User
    template_name = "core/adminlte/user_detail.html"
    context_object_name = "user_obj"
    permission_required = Permissions.USER


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Handle the creation of a new user."""

    model = User
    form_class = CustomUserForm
    template_name = "core/adminlte/user_form.html"
    success_url = reverse_lazy("users:user_list")
    permission_required = Permissions.USER

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


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Handle editing an existing user."""

    model = User
    form_class = CustomUserForm
    template_name = "core/adminlte/user_form.html"
    success_url = reverse_lazy("users:user_list")
    permission_required = Permissions.USER

    def get_context_data(self, **kwargs):
        """Add a page title and the user object to the context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование пользователя"
        context["user_obj"] = self.object
        return context


class OwnerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Display the page with the list of owners."""

    model = User
    template_name = "core/adminlte/owner_list.html"
    permission_required = Permissions.OWNER

    def get_context_data(self, **kwargs):
        """Provide data for filter dropdowns to the template context."""
        context = super().get_context_data(**kwargs)
        context["all_houses"] = House.objects.all()
        context["all_statuses"] = User.UserStatus.choices
        return context


class OwnerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Display detailed information about an owner."""

    model = User
    template_name = "core/adminlte/owner_detail.html"
    context_object_name = "owner_obj"
    permission_required = Permissions.OWNER

    def get_queryset(self):
        """Ensure that only users of type 'owner' can be accessed."""
        return super().get_queryset().filter(user_type="owner")


class OwnerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Handle the creation of a new owner."""

    model = User
    form_class = OwnerForm
    template_name = "core/adminlte/owner_form.html"
    success_url = reverse_lazy("users:owner_list")
    permission_required = Permissions.OWNER

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


class OwnerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Handle editing an existing owner."""

    model = User
    form_class = OwnerForm
    template_name = "core/adminlte/owner_form.html"
    context_object_name = "owner_obj"
    permission_required = Permissions.OWNER

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
    success_url = reverse_lazy("users:cabinet")

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


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """List of sent messages for the administrator/employee."""

    model = Message
    template_name = "core/adminlte/message_list.html"
    permission_required = Permissions.MESSAGE

    def get_queryset(self):
        """Return messages sent by the employee."""
        return Message.objects.filter(sender=self.request.user)


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Display one specific message for an employee (admin panel)."""

    model = Message
    template_name = "core/adminlte/message_detail.html"
    context_object_name = "message"
    permission_required = Permissions.MESSAGE

    def get_queryset(self):
        """Return only messages sent by the employee."""
        return Message.objects.filter(sender=self.request.user)

    def get_context_data(self, **kwargs):
        """Add a variable for the base template to the context."""
        context = super().get_context_data(**kwargs)
        context["base_layout"] = "core/adminlte/admin_layout.html"
        context["list_url"] = reverse_lazy("users:message_list")
        return context


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create a new message. Available only to employees.."""

    model = Message
    form_class = MessageForm
    template_name = "core/adminlte/message_form.html"
    permission_required = Permissions.MESSAGE
    success_url = reverse_lazy("users:message_list")

    def get_context_data(self, **kwargs):
        """Add available houses to the context."""
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()
        return context

    def form_valid(self, form):
        """Save the message with sender and recipients."""
        final_recipients = form.cleaned_data["final_recipients"]

        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.save()

        self.object.recipients.set(final_recipients)

        return super(CreateView, self).form_valid(form)


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
    """Display all services for a specific apartment owner.

    Shows services from both the tariff and receipts.
    """

    model = Apartment
    template_name = "core/adminlte/cabinet_tariff_detail.html"
    context_object_name = "apartment"
    pk_url_kwarg = "apartment_id"

    def get_queryset(self):
        """Allow the user to view only their own apartments."""
        return Apartment.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        """Add combined services from tariff and receipts to the context."""
        context = super().get_context_data(**kwargs)
        apartment = self.get_object()

        combined_services = {}

        if apartment.tariff:
            tariff_services = TariffService.objects.filter(
                tariff=apartment.tariff
            ).select_related("service", "service__unit")

            for ts in tariff_services:
                if ts.service_id not in combined_services:
                    combined_services[ts.service_id] = {
                        "name": ts.service.name,
                        "unit": ts.service.unit.name,
                        "price": ts.price,
                    }

        receipt_items = (
            ReceiptItem.objects.filter(receipt__apartment=apartment)
            .select_related("service", "service__unit")
            .order_by("service_id")
            .distinct("service_id")
        )

        for item in receipt_items:
            if item.service_id not in combined_services:
                combined_services[item.service_id] = {
                    "name": item.service.name,
                    "unit": item.service.unit.name,
                    "price": item.price_per_unit,
                }

        final_services_list = sorted(
            combined_services.values(), key=lambda x: x["name"]
        )

        context["all_services"] = final_services_list
        return context
