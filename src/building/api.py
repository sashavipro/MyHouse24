"""src/building/api.py."""

from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import House
from .schemas import HouseListResponseSchema
from .schemas import StatusResponse

router = Router(tags=["Buildings"])


@router.post("/list", response=HouseListResponseSchema)
def list_houses(request: HttpRequest):
    """Provide paginated and filtered house data for DataTables."""
    params = request.POST
    draw = int(params.get("draw", 0))
    start = int(params.get("start", 0))
    length = int(params.get("length", 10))
    query_title = params.get("title", "")
    query_address = params.get("address", "")
    queryset = House.objects.order_by("id")
    total_records = queryset.count()
    if query_title:
        queryset = queryset.filter(title__icontains=query_title)
    if query_address:
        queryset = queryset.filter(address__icontains=query_address)
    filtered_records = queryset.count()
    queryset = queryset[start : start + length]
    house_list = [
        {"pk": house.pk, "title": house.title, "address": house.address}
        for house in queryset
    ]
    return {
        "draw": draw,
        "records_total": total_records,
        "records_filtered": filtered_records,
        "data": house_list,
    }


@router.post("/delete", response={200: StatusResponse, 500: StatusResponse})
def delete_house(request: HttpRequest):
    """Delete a house by its ID."""
    try:
        house_id = request.POST.get("house_id")
        if not house_id:
            return 400, {
                "status": "error",
                "message": "House ID not provided",
            }

        house_to_delete = get_object_or_404(House, id=house_id)
        title = house_to_delete.title
        house_to_delete.delete()

    except House.DoesNotExist:
        return 404, {
            "status": "error",
            "message": f"House with ID {house_id} not found",
        }
    except (ValueError, IntegrityError) as e:
        error_message = f"Error during deletion: {e!s}"
        return 500, {"status": "error", "message": error_message}
    else:
        success_message = f'House "{title}" deleted successfully.'
        return 200, {"status": "success", "message": success_message}
