"""src/core/views.py."""

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from src.core.forms import CustomAuthenticationForm
from src.core.forms import ResidentHCaptchaForm
from src.users.models import User
from src.users.utils import get_employee_home_url


class LoginView(FormView):
    """Display and processes the login form for both residents and administrators."""

    template_name = "core/adminlte/login.html"
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        """Determine the redirect URL based on the user's role."""
        user = self.request.user

        if user.user_type == User.UserType.OWNER:
            return reverse("users:cabinet")

        if user.user_type == User.UserType.EMPLOYEE:
            home_url = get_employee_home_url(user)

            if home_url:
                return home_url

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
