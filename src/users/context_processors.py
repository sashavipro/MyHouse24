"""src/users/context_processors.py."""

from django.urls import reverse

from .models import MessageRecipient
from .models import User
from .utils import get_employee_home_url


def notifications_context(request):
    """Provide context for notifications in the header for all types of users."""
    if not request.user.is_authenticated:
        return {}

    user = request.user
    context = {
        "new_users_count": 0,
        "new_users": [],
        "unread_messages_count": 0,
        "unread_messages": [],
    }

    if user.user_type == User.UserType.EMPLOYEE:
        user_groups = set(user.groups.values_list("name", flat=True))
        if "Директор" in user_groups or "Управляющий" in user_groups:
            new_users = User.objects.filter(
                status=User.UserStatus.NEW, user_type=User.UserType.OWNER
            )
            context["new_users_count"] = new_users.count()
            context["new_users"] = new_users[:5]

    elif user.user_type == User.UserType.OWNER:
        unread_message_recipients = (
            MessageRecipient.objects.filter(user=user, is_read=False)
            .select_related("message")
            .order_by("-message__date")
        )

        context["unread_messages_count"] = unread_message_recipients.count()
        context["unread_messages"] = unread_message_recipients[:5]

    return context


def user_home_url(request):
    """Define the user's home page."""
    if not request.user.is_authenticated:
        return {"user_home_url": reverse("core:login")}

    user = request.user
    if user.user_type == User.UserType.OWNER:
        return {"user_home_url": reverse("users:cabinet")}

    if user.user_type == User.UserType.EMPLOYEE:
        home_url = get_employee_home_url(user)
        return {"user_home_url": home_url or reverse("core:login")}

    return {"user_home_url": reverse("core:login")}
