"""src/finance/api.py."""

from django.db import DatabaseError
from django.db import transaction
from django.db.models import ProtectedError
from django.db.models import Sum
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from src.building.models import PersonalAccount

from .models import Article
from .models import CashBox
from .models import CounterReading
from .models import Receipt
from .models import Service
from .models import Tariff
from .models import TariffService
from .schemas import CounterReadingSchema
from .schemas import DeleteItemsSchema
from .schemas import StatusResponse
from .schemas import TariffServiceSchema
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


@router.get("/tariff/{tariff_id}/services", response=list[TariffServiceSchema])
def get_tariff_services(request, tariff_id: int):
    """Return a list of services with prices and units of measurement.

    Returns services for the specified tariff.
    """
    tariff_services = TariffService.objects.filter(tariff_id=tariff_id).select_related(
        "service", "service__unit"
    )

    return [
        {
            "service_id": ts.service.id,
            "service_name": ts.service.name,
            "price": ts.price,
            "unit_name": ts.service.unit.name,
        }
        for ts in tariff_services
    ]


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
    except (ProtectedError, ValueError, AttributeError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return {
            "status": "success",
            "message": f'Article "{name}" was successfully deleted.',
        }


@router.delete(
    "/counter-reading/{reading_id}", response={200: StatusResponse, 500: StatusResponse}
)
def delete_counter_reading(request: HttpRequest, reading_id: int):
    """Delete the meter reading by its ID."""
    try:
        reading_to_delete = get_object_or_404(CounterReading, id=reading_id)
        reading_number = reading_to_delete.number
        reading_to_delete.delete()
    except (ProtectedError, ValueError, AttributeError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return 200, {
            "status": "success",
            "message": f'Показание №"{reading_number}" было успешно удалено.',
        }


@router.delete(
    "/receipt/{receipt_id}",
    response={200: StatusResponse, 404: StatusResponse, 500: StatusResponse},
)
def delete_receipt(request: HttpRequest, receipt_id: int):
    """Delete a receipt by its ID."""
    try:
        receipt_to_delete = get_object_or_404(Receipt, id=receipt_id)
        receipt_number = receipt_to_delete.number
        receipt_to_delete.delete()
    except (ProtectedError, ValueError, AttributeError) as e:
        return 500, {
            "status": "error",
            "message": f"Произошла ошибка при удалении: {e}",
        }
    else:
        return 200, {
            "status": "success",
            "message": f"Квитанция №{receipt_number} была успешно удалена.",
        }


@router.get(
    "/apartment/{apartment_id}/counter-readings", response=list[CounterReadingSchema]
)
def get_apartment_counter_readings(request, apartment_id: int):
    """Return the last 10 meter readings for the specified apartment."""
    readings = (
        CounterReading.objects.filter(counter__apartment_id=apartment_id)
        .select_related("counter__service__unit")
        .order_by("-date", "-id")[:10]
    )

    months = [
        "",
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь",
    ]

    return [
        {
            "id": r.id,
            "number": r.number,
            "status": r.status,
            "status_display": r.get_status_display(),
            "date": r.date,
            "month_display": f"{months[r.date.month]} {r.date.year}",
            "service_name": r.service.name,
            "service_id": r.counter.service.id,
            "value": r.value,
            "unit_name": r.service.unit.name,
        }
        for r in readings
    ]


@router.delete(
    "/receipts/bulk-delete", response={200: StatusResponse, 500: StatusResponse}
)
def bulk_delete_receipts(request: HttpRequest, payload: DeleteItemsSchema):
    """Bulk delete receipts by their ID list."""
    try:
        receipts_to_delete = Receipt.objects.in_bulk(payload.ids)

        if len(receipts_to_delete) != len(payload.ids):
            pass

        count = len(receipts_to_delete)

        Receipt.objects.filter(id__in=payload.ids).delete()

    except (ProtectedError, ValueError, AttributeError) as e:
        return 500, {
            "status": "error",
            "message": f"Произошла ошибка при массовом удалении: {e}",
        }
    else:
        return 200, {
            "status": "success",
            "message": f"Успешно удалено {count} квитанций.",
        }


@router.get(
    "/apartment/{apartment_id}/unread-readings", response=list[CounterReadingSchema]
)
def get_apartment_unread_readings(request, apartment_id: int):
    """Return unread (new) counter readings for the apartment."""
    readings = (
        CounterReading.objects.filter(
            counter__apartment_id=apartment_id, status=CounterReading.CounterStatus.NEW
        )
        .select_related("counter__service__unit")
        .order_by("date")
    )

    return [
        {
            "id": r.id,
            "number": r.number,
            "status": r.status,
            "status_display": r.get_status_display(),
            "date": r.date,
            "month_display": "",
            "service_name": r.counter.service.name,
            "service_id": r.counter.service.id,
            "value": r.value,
            "unit_name": r.counter.service.unit.name,
        }
        for r in readings
    ]


@router.post(
    "/counter-readings/mark-as-considered",
    response={200: StatusResponse, 500: StatusResponse},
)
def mark_readings_as_considered(request: HttpRequest, payload: DeleteItemsSchema):
    """Mark counter readings as 'considered' (учтено)."""
    try:
        updated_count = CounterReading.objects.filter(
            id__in=payload.ids, status=CounterReading.CounterStatus.NEW
        ).update(status=CounterReading.CounterStatus.CONSIDERED)

    # Fixed BLE001: Catch specific exceptions instead of bare Exception
    except (DatabaseError, ValueError, AttributeError) as e:
        return 500, {
            "status": "error",
            "message": f"Ошибка при обновлении статусов: {e}",
        }
    else:
        return 200, {
            "status": "success",
            "message": f"Обновлено показаний: {updated_count}",
        }


@router.delete("/cashbox/{cashbox_id}")
def delete_cashbox(request: HttpRequest, cashbox_id: int):
    """Delete a cashbox transaction and return updated stats."""
    cashbox_to_delete = get_object_or_404(CashBox, id=cashbox_id)

    try:
        with transaction.atomic():
            if cashbox_to_delete.is_posted and cashbox_to_delete.personal_account:
                account = cashbox_to_delete.personal_account
                if cashbox_to_delete.article.type == Article.ArticleType.INCOME:
                    account.balance -= cashbox_to_delete.amount
                elif cashbox_to_delete.article.type == Article.ArticleType.EXPENSE:
                    account.balance += cashbox_to_delete.amount
                account.save()

            cashbox_to_delete.delete()

            income = (
                CashBox.objects.filter(
                    is_posted=True, article__type="income"
                ).aggregate(s=Sum("amount"))["s"]
                or 0
            )
            expense = (
                CashBox.objects.filter(
                    is_posted=True, article__type="expense"
                ).aggregate(s=Sum("amount"))["s"]
                or 0
            )
            total_cash = income - expense

            total_balance = (
                PersonalAccount.objects.aggregate(t=Sum("balance"))["t"] or 0
            )

            total_debt = (
                PersonalAccount.objects.filter(balance__lt=0).aggregate(
                    t=Sum("balance")
                )["t"]
                or 0
            )

    # Fixed BLE001: Catch specific exceptions instead of bare Exception
    except (DatabaseError, ValueError, AttributeError, ProtectedError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return {
            "status": "success",
            "message": "Запись удалена",
            "stats": {
                "total_cash": float(total_cash),
                "total_balance": float(total_balance),
                "total_debt": float(total_debt),
            },
        }
