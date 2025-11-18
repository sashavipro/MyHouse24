"""src/building/datatables.py."""

from contextlib import suppress

from ajax_datatable.views import AjaxDatatableView
from django.db.models import Q
from django.urls import reverse

from .models import Apartment
from .models import House
from .models import PersonalAccount


class HouseAjaxDatatableView(AjaxDatatableView):
    """Provides server-side processing for the House list DataTable."""

    model = House
    title = "Дома"
    show_column_filters = False

    column_defs = [
        {
            "name": "pk",
            "title": "#",
            "width": "50px",
            "orderable": True,
            "searchable": False,
        },
        {"name": "title", "title": "Название", "orderable": True, "searchable": False},
        {"name": "address", "title": "Адрес", "orderable": False, "searchable": False},
        {
            "name": "actions",
            "title": "",
            "orderable": False,
            "searchable": False,
            "width": "120px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build the initial queryset and applies filters."""
        queryset = House.objects.all().order_by("pk")

        if not request:
            return queryset

        filters = {
            "title__icontains": request.POST.get("title"),
            "address__icontains": request.POST.get("address"),
        }

        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        """Apply a dictionary of filters to the queryset."""
        query_conditions = Q()

        for key, value in filters.items():
            if value:
                cleaned_value = value.strip() if isinstance(value, str) else value
                query_conditions &= Q(**{key: cleaned_value})

        return queryset.filter(query_conditions)

    def customize_row(self, row, obj):
        """Customize each row of the DataTable."""
        row["DT_RowAttr"] = {
            "data-detail-url": reverse("building:house_detail", args=[obj.pk])
        }

        edit_url = reverse("building:house_edit", args=[obj.pk])
        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{edit_url}" class="btn btn-sm
                 btn-primary edit-house-link" title="Редактировать">
                    <i class="bi bi-pencil"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger delete-house-btn"
                        data-id="{obj.pk}" data-name="{obj.title}" title="Удалить">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row


class ApartmentAjaxDatatableView(AjaxDatatableView):
    """Provide server-side processing for the Apartment list DataTable."""

    model = Apartment
    title = "Квартиры"
    show_column_filters = False

    column_defs = [
        {
            "name": "number",
            "title": "№ квартиры",
            "searchable": False,
            "orderable": False,
        },
        {"name": "house", "title": "Дом", "searchable": False, "orderable": False},
        {"name": "section", "title": "Секция", "searchable": False, "orderable": False},
        {"name": "floor", "title": "Этаж", "searchable": False, "orderable": False},
        {"name": "owner", "title": "Владелец", "searchable": False, "orderable": False},
        {
            "name": "balance",
            "title": "Остаток (грн)",
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "actions",
            "title": "",
            "searchable": False,
            "orderable": False,
            "width": "12_px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build the initial queryset and applies filters."""
        queryset = Apartment.objects.select_related(
            "house", "section", "floor", "owner"
        ).order_by("id")

        if not request:
            return queryset

        filters = {
            "number__icontains": request.POST.get("number"),
            "house_id": request.POST.get("house"),
            "section_id": request.POST.get("section"),
            "floor_id": request.POST.get("floor"),
            "owner_id": request.POST.get("owner"),
            "balance": request.POST.get("balance"),
        }

        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        """Apply a dictionary of filters to the queryset."""
        query_conditions = Q()

        for key, value in filters.items():
            if not value:
                continue

            if key == "balance":
                if value == "debt":
                    query_conditions &= Q(personal_account__balance__lt=0)
                elif value == "no_debt":
                    query_conditions &= Q(personal_account__balance__gte=0)
                continue

            cleaned_value = value.strip() if isinstance(value, str) else value
            query_conditions &= Q(**{key: cleaned_value})

        return queryset.filter(query_conditions)

    def customize_row(self, row, obj):
        """Customize each row of the DataTable."""
        row["number"] = obj.number or "—"
        row["house"] = obj.house.title if obj.house else "—"
        row["section"] = obj.section.name if obj.section else "—"
        row["floor"] = obj.floor.name if obj.floor else "—"
        row["owner"] = obj.owner.get_full_name() if obj.owner else "—"

        balance_value = obj.personal_account.balance if obj.personal_account else 0.0

        balance_class = ""
        if balance_value < 0:
            balance_class = "text-danger"
        elif balance_value > 0:
            balance_class = "text-success"

        row["balance"] = (
            f'<span class="{balance_class} fw-bold">{balance_value:.2f}</span>'
        )

        edit_url = reverse("building:apartment_edit", args=[obj.pk])
        row["DT_RowAttr"] = {
            "data-detail-url": reverse("building:apartment_detail", args=[obj.pk])
        }
        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                    title="Редактировать" onclick="event.stopPropagation();">
                    <i class="bi bi-pencil"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger delete-apartment-btn"
                        data-id="{obj.pk}" data-name="№{obj.number}" title="Удалить">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row


class PersonalAccountAjaxDatatableView(AjaxDatatableView):
    """Provide server-side processing for the Personal Account list DataTable."""

    model = PersonalAccount
    title = "Лицевые счета"
    initial_order = [["pk", "asc"]]
    show_column_filters = False

    column_defs = [
        {"name": "pk", "visible": False, "orderable": True},
        {"name": "number", "title": "№", "orderable": True},
        {"name": "status", "title": "Статус", "searchable": False, "orderable": False},
        {
            "name": "apartment_number",
            "title": "Квартира",
            "searchable": False,
            "orderable": False,
        },
        {"name": "house", "title": "Дом", "searchable": False, "orderable": False},
        {"name": "section", "title": "Секция", "searchable": False, "orderable": False},
        {"name": "owner", "title": "Владелец", "searchable": False, "orderable": False},
        {"name": "balance", "title": "Остаток (грн)", "orderable": True},
        {
            "name": "actions",
            "title": "",
            "searchable": False,
            "orderable": False,
            "width": "80px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build the initial queryset and applies filters."""
        queryset = PersonalAccount.objects.all().order_by("pk")

        if not request:
            return queryset

        filters = {
            "number__icontains": request.POST.get("number"),
            "status": request.POST.get("status"),
            "apartment__number__icontains": request.POST.get("apartment_number"),
            "apartment__house_id": request.POST.get("house"),
            "apartment__section_id": request.POST.get("section"),
            "apartment__owner_id": request.POST.get("owner"),
            "balance": request.POST.get("balance"),
        }

        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        """Apply a dictionary of filters to the queryset."""
        query_conditions = Q()

        for key, value in filters.items():
            if not value:
                continue

            if key == "balance":
                if value == "debt":
                    query_conditions &= Q(balance__lt=0)
                elif value == "no_debt":
                    query_conditions &= Q(balance__gte=0)
                elif value == "zero":
                    query_conditions &= Q(balance=0)
                continue

            cleaned_value = value.strip() if isinstance(value, str) else value
            query_conditions &= Q(**{key: cleaned_value})

        return queryset.filter(query_conditions)

    def customize_row(self, row, obj):
        """Customize each row to add HTML and data from related models."""
        badge_class = "bg-success" if obj.status == "active" else "bg-danger"
        status_text = "Активен" if obj.status == "active" else "Неактивен"
        row["status"] = f'<span class="badge {badge_class}">{status_text}</span>'

        apt = None
        with suppress(self.model.apartment.RelatedObjectDoesNotExist):
            apt = obj.apartment

        row["apartment_number"] = apt.number if apt else "(не задано)"
        row["house"] = apt.house.title if apt and apt.house else "(не задано)"
        row["section"] = apt.section.name if apt and apt.section else "(не задано)"
        row["owner"] = apt.owner.get_full_name() if apt and apt.owner else "(не задано)"

        balance_value = obj.balance
        balance_class = ""
        if balance_value < 0:
            balance_class = "text-danger"
        elif balance_value > 0:
            balance_class = "text-success"
        row["balance"] = (
            f'<span class="{balance_class} fw-bold">{balance_value:.2f}</span>'
        )

        edit_url = reverse("building:personal_account_edit", args=[obj.pk])
        detail_url = reverse("building:personal_account_detail", args=[obj.pk])
        row["DT_RowAttr"] = {"data-detail-url": detail_url}
        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                    title="Редактировать" onclick="event.stopPropagation();">
                    <i class="bi bi-pencil"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger delete-account-btn"
                        data-id="{obj.pk}" data-name="{obj.number}" title="Удалить">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row
