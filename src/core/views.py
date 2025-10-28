"""src/core/views.py."""

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class LoginView(auth_views.LoginView):
    """Отображает и обрабатывает форму входа в систему."""

    template_name = "core/adminlte/login.html"


class LogoutView(auth_views.LogoutView):
    """Обрабатывает выход пользователя из системы."""

    next_page = reverse_lazy("core:login")
