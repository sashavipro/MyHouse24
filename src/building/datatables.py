"""src/building/datatables.py."""

from contextlib import suppress

from ajax_datatable.views import AjaxDatatableView
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
            "orderable": False,
            "searchable": False,
        },
        {"name": "title", "title": "Название", "orderable": False, "searchable": False},
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
        """Build the initial queryset for the DataTable."""
        queryset = House.objects.all().order_by("pk")
        if request:
            if title := request.POST.get("title", "").strip():
                queryset = queryset.filter(title__icontains=title)
            if address := request.POST.get("address", "").strip():
                queryset = queryset.filter(address__icontains=address)
        return queryset

    def customize_row(self, row, obj):
        """Customize each row of the DataTable."""
        row["DT_RowAttr"] = {
            "data-detail-url": reverse("building:house_detail", args=[obj.pk])
        }

        # Формируем кнопки действий
        edit_url = reverse("building:house_edit", args=[obj.pk])
        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{edit_url}" class="btn btn-sm btn-primary
                    edit-house-link" title="Редактировать">
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
    """Provides server-side processing for the Apartment list DataTable."""

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
            "width": "120px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build the initial queryset for the DataTable."""
        queryset = Apartment.objects.select_related(
            "house", "section", "floor", "owner"
        ).order_by("id")

        if request:
            if number := request.POST.get("number", "").strip():
                queryset = queryset.filter(number__icontains=number)
            if house_id := request.POST.get("house", "").strip():
                queryset = queryset.filter(house_id=house_id)
            if section_id := request.POST.get("section", "").strip():
                queryset = queryset.filter(section_id=section_id)
            if floor_id := request.POST.get("floor", "").strip():
                queryset = queryset.filter(floor_id=floor_id)
            if owner_id := request.POST.get("owner", "").strip():
                queryset = queryset.filter(owner_id=owner_id)
            if balance_filter := request.POST.get("balance", "").strip():
                if balance_filter == "debt":
                    queryset = queryset.filter(personal_account__balance__lt=0)
                elif balance_filter == "no_debt":
                    queryset = queryset.filter(personal_account__balance__gte=0)

        return queryset

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
    """Provides server-side processing for the Personal Account list DataTable."""

    model = PersonalAccount
    title = "Лицевые счета"
    initial_order = [["pk", "asc"]]
    show_column_filters = False

    column_defs = [
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
        """Build the initial queryset for the DataTable."""
        queryset = PersonalAccount.objects.all().order_by("pk")

        if not request:
            return queryset

        return self._apply_balance_filter(
            request,
            self._apply_owner_filter(
                request,
                self._apply_section_filter(
                    request,
                    self._apply_house_filter(
                        request,
                        self._apply_apartment_filter(
                            request,
                            self._apply_status_filter(
                                request, self._apply_number_filter(request, queryset)
                            ),
                        ),
                    ),
                ),
            ),
        )

    def _apply_number_filter(self, request, queryset):
        """Apply number filter if present."""
        if number := request.POST.get("number", "").strip():
            return queryset.filter(number__icontains=number)
        return queryset

    def _apply_status_filter(self, request, queryset):
        """Apply status filter if present."""
        if status := request.POST.get("status", "").strip():
            return queryset.filter(status=status)
        return queryset

    def _apply_apartment_filter(self, request, queryset):
        """Apply apartment number filter if present."""
        if apartment_number := request.POST.get("apartment_number", "").strip():
            return queryset.filter(apartment__number__icontains=apartment_number)
        return queryset

    def _apply_house_filter(self, request, queryset):
        """Apply house filter if present."""
        if house_id := request.POST.get("house", "").strip():
            return queryset.filter(apartment__house_id=house_id)
        return queryset

    def _apply_section_filter(self, request, queryset):
        """Apply section filter if present."""
        if section_id := request.POST.get("section", "").strip():
            return queryset.filter(apartment__section_id=section_id)
        return queryset

    def _apply_owner_filter(self, request, queryset):
        """Apply owner filter if present."""
        if owner_id := request.POST.get("owner", "").strip():
            return queryset.filter(apartment__owner_id=owner_id)
        return queryset

    def _apply_balance_filter(self, request, queryset):
        """Apply balance filter if present."""
        if balance := request.POST.get("balance", "").strip():
            if balance == "debt":
                return queryset.filter(balance__lt=0)
            if balance == "no_debt":
                return queryset.filter(balance__gte=0)
            if balance == "zero":
                return queryset.filter(balance=0)
        return queryset

    def customize_row(self, row, obj):
        """Customize each row to add HTML and data from related models."""
        badge_class = "bg-success" if obj.status == "active" else "bg-danger"
        status_text = "Активен" if obj.status == "active" else "Неактивен"
        row["status"] = f'<span class="badge {badge_class}">{status_text}</span>'

        apt = None
        if hasattr(obj, "apartment"):
            with suppress(AttributeError):
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
