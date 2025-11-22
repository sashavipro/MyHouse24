"""src/building/api.py."""

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import DatabaseError
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Apartment
from .models import Floor
from .models import House
from .models import PersonalAccount
from .models import Section
from .schemas import StatusResponse

router = Router(tags=["Buildings"])


@router.delete("/house/{house_id}", response=StatusResponse)
def delete_house(request: HttpRequest, house_id: int):
    """Delete a house by its ID."""
    house_to_delete = get_object_or_404(House, id=house_id)
    name = house_to_delete.title
    try:
        house_to_delete.delete()
    except (IntegrityError, DatabaseError, ValidationError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return {"status": "success", "message": f'Дом "{name}" успешно удален.'}


@router.get("/house/{house_id}/sections")
def get_sections(request, house_id: int):
    """Return sections for a selected house."""
    sections = Section.objects.filter(house_id=house_id).values("id", "name")
    return list(sections)


@router.get("/house/{house_id}/floors")
def get_floors(request, house_id: int):
    """Return floors for a selected house."""
    floors = Floor.objects.filter(house_id=house_id).values("id", "name")
    return list(floors)


@router.get("/house/{house_id}/apartments")
def get_apartments(
    request,
    house_id: int,
    section: int | None = None,
):
    """Return apartments for a selected house, optionally filtered by section."""
    queryset = Apartment.objects.filter(house_id=house_id)

    if section:
        queryset = queryset.filter(section_id=section)

    apartments = queryset.select_related("owner").values(
        "id", "number", "owner__first_name", "owner__last_name"
    )

    return [
        {
            "id": apt["id"],
            "number": apt["number"],
            "owner_name": (
                f"{apt['owner__first_name'] or ''} " f"{apt['owner__last_name'] or ''}"
            ).strip()
            or "не выбран",
        }
        for apt in apartments
    ]


@router.get("/personal-accounts/search")
def search_personal_accounts(
    request,
    term: str | None = None,
    current_apartment_id: int | None = None,
    page: int = 1,
):
    """Search for available personal accounts with pagination."""
    queryset = PersonalAccount.objects.all().order_by(
        "number"
    )  # Важно добавить сортировку для пагинации

    q_filter = Q(apartment__isnull=True)

    if current_apartment_id:
        try:
            current_apartment = Apartment.objects.get(pk=current_apartment_id)
            if current_apartment.personal_account:
                q_filter |= Q(pk=current_apartment.personal_account.pk)
        except Apartment.DoesNotExist:
            pass

    queryset = queryset.filter(q_filter)

    if term:
        queryset = queryset.filter(number__icontains=term)

    page_size = 10
    paginator = Paginator(queryset, page_size)

    page_obj = paginator.get_page(page)

    results = [{"id": acc.pk, "text": acc.number} for acc in page_obj]

    return {"results": results, "pagination": {"more": page_obj.has_next()}}


@router.delete("/apartment/{apartment_id}", response=StatusResponse)
def delete_apartment(request: HttpRequest, apartment_id: int):
    """Delete an apartment by its ID from the URL."""
    apartment_to_delete = get_object_or_404(Apartment, id=apartment_id)
    number = apartment_to_delete.number
    house_title = apartment_to_delete.house.title

    try:
        apartment_to_delete.delete()
    except (IntegrityError, DatabaseError, ValidationError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return 200, {
            "status": "success",
            "message": f'Квартира №{number} в доме "{house_title}" успешно удалена.',
        }


@router.delete("/personal-account/{account_id}", response=StatusResponse)
def delete_personal_account(request: HttpRequest, account_id: int):
    """Delete a personal account by its ID."""
    account = get_object_or_404(PersonalAccount, id=account_id)
    number = account.number
    try:
        account.delete()
    except (IntegrityError, DatabaseError, ValidationError) as e:
        return 500, {"status": "error", "message": str(e)}
    else:
        return {
            "status": "success",
            "message": f'Лицевой счет "{number}" успешно удален.',
        }


@router.get("/apartment/{apartment_id}/details")
def get_apartment_details(request, apartment_id: int):
    """Return detailed information about the apartment.

    Includes the owner, personal account, and rate.
    """
    apartment = get_object_or_404(
        Apartment.objects.select_related("owner", "personal_account", "tariff"),
        id=apartment_id,
    )

    owner_name = "не выбран"
    owner_phone = "не выбран"
    if apartment.owner:
        owner_name = apartment.owner.get_full_name()
        owner_phone = apartment.owner.phone or "не указан"

    personal_account_number = (
        apartment.personal_account.number if apartment.personal_account else ""
    )
    tariff_id = apartment.tariff.id if apartment.tariff else None

    return {
        "owner_name": owner_name,
        "owner_phone": owner_phone,
        "personal_account_number": personal_account_number,
        "tariff_id": tariff_id,
    }


@router.get("/apartments/search-by-owner")
def search_apartments_by_owner(
    request, owner_id: int, term: str | None = None, page: int = 1
):
    """Search for apartments owned by a specific owner for Select2 (Lazy Load)."""
    queryset = Apartment.objects.filter(owner_id=owner_id).select_related(
        "house", "section"
    )

    if term:
        queryset = queryset.filter(
            Q(number__icontains=term) | Q(house__title__icontains=term)
        )

    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(page)

    results = []
    for apt in page_obj:
        text = f"№{apt.number}, {apt.house.title}"
        results.append({"id": apt.id, "text": text})

    return {"results": results, "pagination": {"more": page_obj.has_next()}}
