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
