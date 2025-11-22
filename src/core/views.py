"""src/core/views.py."""

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import NoReverseMatch
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from src.core.forms import CustomAuthenticationForm
from src.core.forms import ResidentHCaptchaForm
from src.users.models import User


class LoginView(FormView):
    """Display and processes the login form for both residents and administrators."""

    template_name = "core/adminlte/login.html"
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        """Determine the redirect URL based on the user's role and its fields."""
        user = self.request.user

        if not user.is_authenticated:
            return reverse("core:login")

        if user.user_type == User.UserType.OWNER:
            return reverse("cabinet:cabinet")

        if user.user_type == User.UserType.EMPLOYEE:
            user_role = getattr(user, "role", None)
            if not user_role:
                logout(self.request)
                messages.error(
                    self.request, "Your account does not have a role assigned."
                )
                return reverse("core:login")

            role_field_url_map = (
                ("has_statistics", "finance:admin_stats"),
                ("has_receipt", "finance:receipt_list"),
                ("has_message", "users:message_list"),
                ("has_personal_account", "building:personal_account_list"),
                ("has_apartment", "building:apartment_list"),
                ("has_owner", "users:owner_list"),
                ("has_house", "building:house_list"),
                ("has_counters", "finance:counter_list"),
                ("has_management", "website:admin_home"),
                ("has_service", "finance:manage_services"),
                ("has_tariff", "finance:tariff_list"),
                ("has_role", "users:admin_roles"),
                ("has_user", "users:user_list"),
                ("has_payment_details", "finance:payment_details"),
                ("has_article", "finance:article_list"),
            )

            for field_name, url_name in role_field_url_map:
                if getattr(user_role, field_name, False):
                    try:
                        return reverse(url_name)
                    except NoReverseMatch:
                        continue

            logout(self.request)
            messages.error(
                self.request,
                "You do not have permission to access the system. "
                "Please contact your administrator.",
            )
            return reverse("core:login")

        logout(self.request)
        messages.error(self.request, "Unknown user type.")
        return reverse("core:login")

    def form_valid(self, form):
        """Log in the user and then redirects."""
        login(self.request, form.get_user())
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """Handle POST requests based on the active tab."""
        active_tab = request.POST.get("tab", "admin")

        if active_tab == "admin":
            return self._handle_admin_login(request)

        if active_tab == "resident":
            return self._handle_resident_login(request)

        return self.render_to_response(self.get_context_data())

    def _handle_admin_login(self, request):
        """Handle the login logic for the administrator tab."""
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        user = form.get_user()
        if user.user_type == User.UserType.EMPLOYEE:
            return self.form_valid(form)

        messages.error(request, "Access is allowed only for administration.")
        return self.form_invalid(form)

    def _handle_resident_login(self, request):
        """Handle the login logic for the resident tab."""
        captcha_form = ResidentHCaptchaForm(request.POST)
        if not captcha_form.is_valid():
            messages.error(request, "Please confirm that you are not a robot.")
            return self.render_to_response(self.get_context_data(active_tab="resident"))

        username = request.POST.get("username_resident")
        password = request.POST.get("password_resident")

        if not username or not password:
            messages.error(request, "Please enter your E-mail/ID and password.")
            return self.render_to_response(self.get_context_data(active_tab="resident"))

        user = authenticate(request, username=username, password=password)

        if user and user.user_type == User.UserType.OWNER:
            login(request, user)
            return redirect(self.get_success_url())

        if user and user.user_type != User.UserType.OWNER:
            messages.error(
                request, "For administration login, use the appropriate tab."
            )
        else:
            messages.error(request, "Invalid E-mail/ID or password.")

        return self.render_to_response(self.get_context_data(active_tab="resident"))

    def get_context_data(self, **kwargs):
        """Add the active tab and captcha form to the context."""
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["active_tab"] = self.request.POST.get("tab", "admin")
        else:
            context["active_tab"] = self.request.GET.get("tab", "admin")

        if "captcha_form" not in context:
            context["captcha_form"] = ResidentHCaptchaForm()

        return context


class LogoutView(View):
    """Handle user logout for both GET and POST requests."""

    def get(self, request, *args, **kwargs):
        """Log the user out and redirect to the homepage."""
        logout(request)
        return redirect("website:home")

    def post(self, request, *args, **kwargs):
        """Log the user out and redirect to the homepage."""
        logout(request)
        return redirect("website:home")
