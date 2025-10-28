"""src/finance/schemas.py."""

from datetime import datetime

from ninja import Schema


class TariffSchema(Schema):
    """Defines the data structure for a single Tariff object."""

    pk: int
    name: str
    description: str | None
    updated_at: datetime


class TariffListResponseSchema(Schema):
    """Defines the response structure required by DataTables."""

    draw: int
    records_total: int
    records_filtered: int
    data: list[TariffSchema]


class StatusResponse(Schema):
    """Defines a generic status/message response for actions like delete."""

    status: str
    message: str


class UnitSchema(Schema):
    """Defines the data structure for a measurement Unit."""

    name: str
