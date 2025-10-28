"""src/website/apps.py."""

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """website app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.website"
