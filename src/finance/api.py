"""src/finance/api.py."""

from django.db.models import ProtectedError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Article
from .models import Service
from .models import Tariff
from .schemas import StatusResponse
from .schemas import UnitSchema

router = Router(tags=["Finance"])


@router.delete(
    "/tariff/{tariff_id}",
    response={200: StatusResponse, 400: StatusResponse, 500: StatusResponse},
)
def delete_tariff(request: HttpRequest, tariff_id: int):
    """Delete a tariff by its ID, with a check for its usage."""
    try:
        tariff_to_delete = get_object_or_404(Tariff, id=tariff_id)
        name = tariff_to_delete.name
        tariff_to_delete.delete()
    except ProtectedError:
        return 400, {
            "status": "error",
            "message": (
                f'Cannot delete tariff "{name}" because it is in use '
                f"in one or more apartments."
            ),
        }
    # FIX: BLE001 - Catch specific exceptions instead of bare Exception
    except (ValueError, AttributeError) as e:
        return 500, {
            "status": "error",
            "message": f"An unexpected error occurred: {e!s}",
        }
    else:
        return 200, {
            "status": "success",
            "message": f'Tariff "{name}" was successfully deleted.',
        }


@router.get("/service/{service_id}/unit", response=UnitSchema)
def get_service_unit(request, service_id: int):
    """Return the measurement unit for a given service ID."""
    service = get_object_or_404(Service.objects.select_related("unit"), id=service_id)
    return {"name": service.unit.name}


@router.delete("/article/{article_id}", response=StatusResponse)
def delete_article(request: HttpRequest, article_id: int):
    """Delete a payment article by its ID."""
    try:
        article_to_delete = get_object_or_404(Article, id=article_id)
        name = article_to_delete.name
        article_to_delete.delete()
    # FIX: BLE001 - Catch specific exceptions instead of bare Exception
    except (ProtectedError, ValueError, AttributeError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return {
            "status": "success",
            "message": f'Article "{name}" was successfully deleted.',
        }
