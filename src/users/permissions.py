"""src/users/permissions.py."""

import logging

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from .models import Role

logger = logging.getLogger(__name__)


class Permissions:
    """Centralized class for access rights.

    Each attribute is ONE right that grants access to an entire section.
    """

    STATISTICS = "finance.view_statistics"
    CASHBOX = "finance.view_cashbox"
    RECEIPT = "finance.view_receipt"
    PERSONAL_ACCOUNT = "building.view_personalaccount"
    APARTMENT = "building.view_apartment"
    OWNER = "users.view_owner"
    HOUSE = "building.view_house"
    MESSAGE = "users.view_message"
    TICKET = "tickets.view_ticket"
    COUNTERS = "finance.view_counter"
    MANAGEMENT = "website.view_mainpage"
    SERVICE = "finance.view_service"
    TARIFF = "finance.view_tariff"
    ROLE = "users.view_role"
    USER = "users.view_user"
    PAYMENT_DETAILS = "finance.view_paymentdetails"
    ARTICLE = "finance.view_article"


PERMISSION_MAP = {
    "statistics": [Permissions.STATISTICS],
    "cashbox": [Permissions.CASHBOX],
    "receipt": [Permissions.RECEIPT],
    "personal_account": [Permissions.PERSONAL_ACCOUNT],
    "apartment": [Permissions.APARTMENT],
    "owner": [Permissions.OWNER],
    "house": [Permissions.HOUSE],
    "message": [Permissions.MESSAGE],
    "ticket": [Permissions.TICKET],
    "counters": [Permissions.COUNTERS],
    "management": [Permissions.MANAGEMENT],
    "service": [Permissions.SERVICE],
    "tariff": [Permissions.TARIFF],
    "role": [Permissions.ROLE],
    "user": [Permissions.USER],
    "payment_details": [Permissions.PAYMENT_DETAILS],
    "article": [Permissions.ARTICLE],
}


def sync_role_with_group(role: Role):
    """Synchronize the Role object with the corresponding Django Group."""
    group, _ = Group.objects.get_or_create(name=role.name)
    permissions_to_set = []

    for perm_key, perm_list in PERMISSION_MAP.items():
        if getattr(role, f"has_{perm_key}", False):
            for perm_string in perm_list:
                app_label, codename = perm_string.split(".")
                try:
                    perm = Permission.objects.get(
                        content_type__app_label=app_label, codename=codename
                    )
                    permissions_to_set.append(perm)
                except Permission.DoesNotExist:
                    logger.warning(
                        "Permission '%s' not found and was skipped.", perm_string
                    )

    group.permissions.set(permissions_to_set)
