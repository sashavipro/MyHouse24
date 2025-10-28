"""src/users/schemas.py."""

from ninja import Schema
from pydantic import field_validator


class UserSchema(Schema):
    """Defines the data structure for a single User object."""

    pk: int
    full_name: str
    role: str
    phone: str
    email: str
    status: str

    @field_validator("full_name", mode="before")
    @classmethod
    def compute_full_name(cls, v, info):
        """Compute full name from user instance."""
        user = info.data
        if hasattr(user, "get_full_name"):
            return user.get_full_name()
        return v


class UserListResponseSchema(Schema):
    """Define the response structure required by DataTables."""

    draw: int
    records_total: int
    records_filtered: int
    data: list[UserSchema]


class StatusResponse(Schema):
    """Define a generic status/message response for actions like delete."""

    status: str
    message: str
