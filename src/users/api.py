"""src/users/api.py."""

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Router

from src.finance.schemas import DeleteItemsSchema

from .models import Message
from .models import Ticket
from .models import User
from .schemas import RoleResponseSchema
from .schemas import SimpleUserSchema
from .schemas import StatusResponse

router = Router(tags=["Users"])


@router.delete("/user/{user_id}", response=StatusResponse)
def delete_user(request, user_id: int):
    """Delete a staff user by their ID."""
    try:
        user_to_delete = get_object_or_404(User, id=user_id, user_type="employee")
        if request.user.id == user_to_delete.id:
            return 403, {
                "status": "error",
                "message": "You cannot delete your own account.",
            }

        full_name = user_to_delete.get_full_name()
        user_to_delete.delete()
    except (ValueError, IntegrityError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return {
            "status": "success",
            "message": f'Employee "{full_name}" was successfully deleted.',
        }


@router.get("/get-role/", response={200: RoleResponseSchema, 404: StatusResponse})
def get_user_role(request, user_id: int):
    """Return the name of a user's role by their ID."""
    try:
        user = get_object_or_404(User, id=user_id)
        role_name = user.role.name if user.role else "Role not assigned"
    except User.DoesNotExist:
        return 404, {"status": "error", "message": "User not found"}
    else:
        return 200, {"role_name": role_name}


@router.delete("/owner/{owner_id}", response=StatusResponse)
def delete_owner(request, owner_id: int):
    """Delete an owner user by their ID."""
    try:
        owner_to_delete = get_object_or_404(User, id=owner_id, user_type="owner")
        full_name = owner_to_delete.get_full_name()
        owner_to_delete.delete()
    except (ValueError, IntegrityError, AttributeError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return {
            "status": "success",
            "message": f'Owner "{full_name}" was successfully deleted.',
        }


@router.delete("/message/{message_id}", response=StatusResponse)
def delete_message(request, message_id: int):
    """Удаляет сообщение по ID, если оно принадлежит текущему пользователю."""
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    message.delete()
    return {"status": "success", "message": "Сообщение успешно удалено."}


@router.delete("/messages/bulk-delete", response=StatusResponse)
def bulk_delete_messages(request, payload: DeleteItemsSchema):
    """Массово удаляет сообщения по списку ID."""
    count, _ = Message.objects.filter(id__in=payload.ids, sender=request.user).delete()
    return {"status": "success", "message": f"Успешно удалено {count} сообщений."}


@router.delete("/admin/ticket/{ticket_id}", response=StatusResponse)
def delete_ticket_admin(request, ticket_id: int):
    """Delete a ticket by ID (admin access)."""
    if (
        not request.user.is_authenticated
        or request.user.user_type != User.UserType.EMPLOYEE
    ):
        return 403, {"status": "error", "message": "Forbidden"}

    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    return {"status": "success", "message": "Заявка успешно удалена."}


@router.get("/masters/by-role", response=list[SimpleUserSchema])
def get_masters_by_role(request, role_id: int | None = None):
    """Return a list of employees (masters).

    If role_id is passed, filters by role.
    Shows employees with status active or new.
    """
    queryset = User.objects.filter(user_type="employee")

    queryset = queryset.exclude(status="inactive")

    if role_id:
        queryset = queryset.filter(role_id=role_id)

    return [
        {"id": u.id, "name": f"{u.last_name} {u.first_name}".strip() or u.username}
        for u in queryset
    ]
