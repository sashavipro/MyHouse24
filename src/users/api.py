"""src/users/api.py."""

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import User
from .schemas import RoleResponseSchema
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
    # FIX: TRY300 - Move success return to else block
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
    # FIX: TRY300 - Move success return to else block
    except User.DoesNotExist:
        return 404, {"status": "error", "message": "User not found"}
    else:
        return 200, {"role_name": role_name}


@router.delete("/owner/{owner_id}", response=StatusResponse)
def delete_owner(request, owner_id: int):
    """Delete an owner user by their ID."""
    try:
        # Убеждаемся, что удаляем именно владельца
        owner_to_delete = get_object_or_404(User, id=owner_id, user_type="owner")
        full_name = owner_to_delete.get_full_name()
        owner_to_delete.delete()
    # FIX: BLE001 - Catch specific exceptions, TRY300 - Move to else block
    except (ValueError, IntegrityError, AttributeError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return {
            "status": "success",
            "message": f'Owner "{full_name}" was successfully deleted.',
        }
