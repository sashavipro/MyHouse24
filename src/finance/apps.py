"""src/finance/apps.py."""

from django.apps import AppConfig


class FinanceConfig(AppConfig):
    """Finance App Config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.finance"
