"""src/users/context_processors.py."""

from django.urls import NoReverseMatch
from django.urls import reverse

from .models import MessageRecipient
from .models import Ticket
from .models import User


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
        "new_tickets_count": 0,
        "new_tickets": [],
    }

    if user.user_type == User.UserType.EMPLOYEE:
        user_role_name = user.role.name if user.role else ""

        if user_role_name in ["Директор", "Управляющий"]:
            new_users = User.objects.filter(
                status=User.UserStatus.NEW, user_type=User.UserType.OWNER
            )
            context["new_users_count"] = new_users.count()
            context["new_users"] = new_users[:5]

        master_tickets = Ticket.objects.filter(
            master=user, status=Ticket.TicketStatus.NEW
        ).order_by("-created_at")

        if master_tickets.exists():
            context["new_tickets_count"] = master_tickets.count()
            context["new_tickets"] = master_tickets[:5]

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
    """Define the user's home page based on Role fields."""
    if not request.user.is_authenticated:
        return {"user_home_url": reverse("core:login")}

    user = request.user
    if user.user_type == User.UserType.OWNER:
        return {"user_home_url": reverse("cabinet:cabinet")}

    if user.user_type == User.UserType.EMPLOYEE:
        user_role = getattr(user, "role", None)
        if not user_role:
            return {"user_home_url": reverse("core:login")}

        role_field_url_map = (
            ("has_statistics", "finance:admin_stats"),
            ("has_receipt", "finance:receipt_list"),
            ("has_message", "users:message_list"),
            ("has_personal_account", "building:personal_account_list"),
            ("has_apartment", "building:apartment_list"),
            ("has_owner", "users:owner_list"),
            ("has_house", "building:house_list"),
            ("has_counters", "finance:counter_list"),
            ("has_management", "website:admin_home"),
            ("has_service", "finance:manage_services"),
            ("has_tariff", "finance:tariff_list"),
            ("has_role", "users:admin_roles"),
            ("has_user", "users:user_list"),
            ("has_payment_details", "finance:payment_details"),
            ("has_article", "finance:article_list"),
        )

        for field_name, url_name in role_field_url_map:
            if getattr(user_role, field_name, False):
                try:
                    return {"user_home_url": reverse(url_name)}
                except NoReverseMatch:
                    continue

    return {"user_home_url": reverse("core:login")}
