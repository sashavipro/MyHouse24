"""src/core/apps.py."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Config app core."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"
