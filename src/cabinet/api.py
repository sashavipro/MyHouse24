"""src/cabinet/api.py."""

from django.db import DatabaseError
from django.db import IntegrityError
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router

from src.finance.schemas import DeleteItemsSchema
from src.finance.schemas import StatusResponse
from src.users.models import MessageRecipient
from src.users.models import Ticket
from src.users.models import User

router = Router(tags=["Cabinet"])


@router.delete("/cabinet/messages/bulk-hide", response=StatusResponse)
def bulk_hide_messages(request, payload: DeleteItemsSchema):
    """Hide messages for the current owner."""
    if (
        not request.user.is_authenticated
        or request.user.user_type != User.UserType.OWNER
    ):
        return 403, {"status": "error", "message": "Доступ запрещен."}

    with transaction.atomic():
        count = MessageRecipient.objects.filter(
            message_id__in=payload.ids, user=request.user
        ).update(is_hidden=True)

    return {"status": "success", "message": f"Успешно скрыто {count} сообщений."}


@router.delete("/ticket/{ticket_id}", response=StatusResponse)
def delete_ticket(request, ticket_id: int):
    """Delete a ticket by its ID (only if owned by user)."""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    try:
        with transaction.atomic():
            ticket.delete()
    except (IntegrityError, DatabaseError) as e:
        return 500, {"status": "error", "message": str(e)}

    return {"status": "success", "message": "Заявка успешно удалена."}
