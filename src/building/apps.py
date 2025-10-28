"""src/building/apps.py."""

from django.apps import AppConfig


class BuildingConfig(AppConfig):
    """Building app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.building"
