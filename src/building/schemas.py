"""src/building/schemas.py."""

from ninja import Schema


class HouseSchema(Schema):
    """Define the data structure for a single House object."""

    pk: int
    title: str
    address: str


class HouseListResponseSchema(Schema):
    """Define the response structure required by DataTables."""

    draw: int
    records_total: int
    records_filtered: int
    data: list[HouseSchema]


class StatusResponse(Schema):
    """Define a generic status/message response for actions like delete."""

    status: str
    message: str


class ApartmentSchema(Schema):
    """Define the data structure for a single Apartment object."""

    pk: int
    number: str
    house_title: str | None = None
    section_name: str | None = None
    floor_name: str | None = None
    owner_full_name: str | None = None
    balance: float | None = None


class ApartmentListResponseSchema(Schema):
    """Define the response structure for an apartment list required by DataTables."""

    draw: int
    records_total: int
    records_filtered: int
    data: list[ApartmentSchema]
