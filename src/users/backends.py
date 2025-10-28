"""src/users/backends.py."""

from uuid import UUID

from django.contrib.auth.backends import ModelBackend

from .models import User


def is_valid_uuid(uuid_to_test, version=4):
    """Check whether a string is a valid UUID."""
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except (ValueError, TypeError):
        return False
    return str(uuid_obj) == uuid_to_test


class EmailOrUserIdBackend(ModelBackend):
    """Email or user id backend."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate."""
        if is_valid_uuid(username):
            try:
                user = User.objects.get(user_id=username)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        """Get a user by id."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
