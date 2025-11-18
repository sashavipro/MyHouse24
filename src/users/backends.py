"""src/users/backends.py."""

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


class CustomBackend(ModelBackend):
    """Custom authentication backend.

    Allow users to log in using either their email address or their `user_id`.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Allow login using email or user_id instead of username."""
        try:
            user = User.objects.get(
                Q(email__iexact=username) | Q(user_id__iexact=username)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        """Get a user by their primary key."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
