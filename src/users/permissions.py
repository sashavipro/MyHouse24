"""src/users/permissions.py."""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse


class RoleRequiredMixin(PermissionRequiredMixin):
    """A custom mixin that inherits from PermissionRequiredMixin.

    It checks permissions based on Boolean fields (`has_...`) in the associated
    Role model.
    """

    def get_permission_required(self):
        """Override this method to ensure permission_required is handled correctly.

        This ensures correct handling whether it's a string or an iterable.
        """
        if self.permission_required is None:
            return None

        if isinstance(self.permission_required, (list, tuple)):
            return self.permission_required[0] if self.permission_required else None

        return str(self.permission_required)

    def has_permission(self):
        """Override the standard permission check method.

        Returns True if the user has the required permission in their role.
        """
        if not self.request.user.is_authenticated:
            return False

        if self.request.user.is_superuser:
            return True

        if not self.request.user.is_staff and self.request.user.user_type != "employee":
            return False

        permission = self.get_permission_required()
        if not permission:
            return True

        user_role = getattr(self.request.user, "role", None)

        if (
            user_role
            and isinstance(permission, str)
            and getattr(user_role, permission, False)
        ):
            return True

        return False

    def handle_no_permission(self):
        """Override the permission denied handler."""
        if self.request.session.get("impersonator_id"):
            current_url = self.request.get_full_path()
            stop_impersonate_url = reverse("users:stop_impersonate")

            return redirect(f"{stop_impersonate_url}?next={current_url}")

        messages.error(self.request, "У вас нет прав для доступа к этой странице.")  # noqa: RUF001
        home_url = getattr(self.request, "user_home_url", None) or "core:login"
        return redirect(home_url)
