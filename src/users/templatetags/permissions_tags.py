"""src/users/templatetags/permissions_tags.py."""

from django import template

from src.users.permissions import Permissions

register = template.Library()


@register.simple_tag
def get_perms():
    """Make the Permissions class available in templates."""
    return Permissions


@register.filter(name="has_perm")
def has_perm_filter(user, permission):
    """Template filter to check if the user has a specific permission.

    Usage: {% if request.user|has_perm:Permissions.STATISTICS %}.
    """
    if user.is_authenticated:
        return user.has_perm(permission)
    return False
