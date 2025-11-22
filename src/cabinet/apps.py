"""src/cabinet/apps.py."""

from django.apps import AppConfig


class CabinetConfig(AppConfig):
    """Cabinet app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.cabinet"
