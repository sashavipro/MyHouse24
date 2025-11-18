"""src/users/utils.py."""

from django.urls import NoReverseMatch
from django.urls import reverse

from .permissions import Permissions


def get_employee_home_url(user):
    """Identify and returns the URL of the first available page for the employee.

    Return None if no pages are available.
    """
    if not user.is_authenticated or user.user_type != "employee":
        return None

    permission_url_map = (
        (Permissions.STATISTICS, "finance:admin_stats"),
        (Permissions.PERSONAL_ACCOUNT, "building:personal_account_list"),
        (Permissions.APARTMENT, "building:apartment_list"),
        (Permissions.MESSAGE, "users:message_list"),
        (Permissions.OWNER, "users:owner_list"),
        (Permissions.HOUSE, "building:house_list"),
        (Permissions.MANAGEMENT, "website:admin_home"),
        (Permissions.SERVICE, "finance:manage_services"),
        (Permissions.TARIFF, "finance:tariff_list"),
        ("users.change_group", "users:admin_roles"),
        (Permissions.USER, "users:user_list"),
        (Permissions.PAYMENT_DETAILS, "finance:payment_details"),
        (Permissions.ARTICLE, "finance:article_list"),
    )

    for perm, url_name in permission_url_map:
        if user.has_perm(perm):
            try:
                return reverse(url_name)
            except NoReverseMatch:
                continue
    return None
