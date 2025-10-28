"""src/users/api.py."""

from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import User
from .schemas import StatusResponse
from .schemas import UserListResponseSchema

router = Router(tags=["Users"])


@router.post("/list", response=UserListResponseSchema)
def list_users(request: HttpRequest):
    """Provide paginated and filtered user data for DataTables."""
    params = request.POST

    draw = int(params.get("draw", 0))
    start = int(params.get("start", 0))
    length = int(params.get("length", 10))

    query_name = params.get("full_name", "")
    query_role = params.get("role", "")
    query_phone = params.get("phone", "")
    query_email = params.get("email", "")
    query_status = params.get("status", "")

    queryset = User.objects.select_related("role").order_by("id")
    total_records = queryset.count()

    if query_name:
        queryset = queryset.filter(
            Q(first_name__icontains=query_name)
            | Q(last_name__icontains=query_name)
            | Q(middle_name__icontains=query_name)
        )
    if query_role:
        queryset = queryset.filter(role__id=query_role)
    if query_phone:
        queryset = queryset.filter(phone__icontains=query_phone)
    if query_email:
        queryset = queryset.filter(email__icontains=query_email)
    if query_status:
        queryset = queryset.filter(status=query_status)

    filtered_records = queryset.count()
    queryset = queryset[start : start + length]

    user_list = [
        {
            "pk": user.pk,
            "full_name": user.get_full_name(),
            "role": user.role.name if user.role else "-",
            "phone": user.phone,
            "email": user.email,
            "status": user.status,
        }
        for user in queryset
    ]

    return {
        "draw": draw,
        "records_total": total_records,
        "records_filtered": filtered_records,
        "data": user_list,
    }


@router.post("/delete", response=StatusResponse)
def delete_user(request: HttpRequest):
    """Delete a user by their ID."""
    try:
        user_id = request.POST.get("user_id")
        user_to_delete = get_object_or_404(User, id=user_id)
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
            "message": f'User "{full_name}" has been deleted successfully.',
        }
