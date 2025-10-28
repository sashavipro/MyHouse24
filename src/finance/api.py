"""src/finance/api.py."""

from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.security import SessionAuth

from .models import Service
from .models import Tariff
from .schemas import StatusResponse
from .schemas import TariffListResponseSchema
from .schemas import UnitSchema

router = Router(tags=["Finance"], auth=SessionAuth())


@router.post("/list", response=TariffListResponseSchema)
def list_tariffs(request: HttpRequest):
    """Provide paginated and sorted tariff data for DataTables."""
    try:
        params = request.POST
        draw = int(params.get("draw", 1))
        start = int(params.get("start", 0))
        length = int(params.get("length", 10))
        order_column_index = int(params.get("order[0][column]", 0))
        order_direction = params.get("order[0][dir]", "asc")
        order_field = "name" if order_column_index == 0 else "id"

        if order_direction == "desc":
            order_field = f"-{order_field}"

        queryset = Tariff.objects.order_by(order_field)
        total_records = queryset.count()
        filtered_records = total_records
        if length > 0:
            queryset = queryset[start : start + length]

        tariff_list = list(queryset.values("pk", "name", "description", "updated_at"))
    except (ValueError, TypeError):
        return {
            "draw": 0,
            "records_total": 0,
            "records_filtered": 0,
            "data": [],
        }
    else:
        return {
            "draw": draw,
            "records_total": total_records,
            "records_filtered": filtered_records,
            "data": tariff_list,
        }


@router.post("/delete", response=StatusResponse)
def delete_tariff(request: HttpRequest):
    """Delete a tariff by its ID."""
    try:
        tariff_id = request.POST.get("tariff_id")
        tariff_to_delete = get_object_or_404(Tariff, id=tariff_id)
        name = tariff_to_delete.name
        tariff_to_delete.delete()
    except (ValueError, IntegrityError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return {
            "status": "success",
            "message": f'Tariff "{name}" deleted successfully.',
        }


@router.get("/service/{service_id}/unit", response=UnitSchema)
def get_service_unit(request, service_id: int):
    """Return the measurement unit for a given service ID."""
    service = get_object_or_404(Service.objects.select_related("unit"), id=service_id)
    return {"name": service.unit.name}
