"""src/finance/datatables.py."""

import datetime

from ajax_datatable.views import AjaxDatatableView
from django.db.models import IntegerField
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.db.models.functions import Cast
from django.urls import reverse
from django.utils import timezone

from .models import Article
from .models import CashBox
from .models import Counter
from .models import CounterReading
from .models import Receipt
from .models import Tariff


class ArticleAjaxDatatableView(AjaxDatatableView):
    """Provides server-side processing for the Article list DataTable."""

    model = Article
    title = "Статьи"
    initial_order = [["name", "asc"]]
    show_search_form = False
    show_column_filters = False

    column_defs = [
        {
            "name": "name",
            "title": "Название",
            "visible": True,
            "orderable": True,
            "className": "text-start",
        },
        {
            "name": "type",
            "title": "Приход/расход",
            "visible": True,
            "orderable": True,
            "className": "text-start",
        },
        {
            "name": "actions",
            "title": "",
            "visible": True,
            "orderable": False,
            "searchable": False,
            "className": "text-end",
            "width": "80px",
        },
    ]

    def customize_row(self, row, obj):
        """Customize each row of the DataTable."""
        type_display = obj.get_type_display()
        if obj.type == "income":
            row["type"] = f'<span class="text-success">{type_display}</span>'
        elif obj.type == "expense":
            row["type"] = f'<span class="text-danger">{type_display}</span>'

        edit_url = reverse("finance:article_edit", args=[obj.pk])

        row["DT_RowAttr"] = {"data-detail-url": edit_url}

        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                    title="Редактировать" onclick="event.stopPropagation();">
                    <i class="bi bi-pencil"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger delete-article-btn"
                        data-id="{obj.pk}"
                        data-name="{obj.name}"
                        title="Удалить">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row


class TariffAjaxDatatableView(AjaxDatatableView):
    """Provide server-side processing for the Tariff list DataTable."""

    model = Tariff
    title = "Тарифы"
    initial_order = [["name", "asc"]]
    show_column_filters = False

    column_defs = [
        {
            "name": "pk",
            "title": "#",
            "visible": True,
            "orderable": True,
            "width": "40px",
        },
        {
            "name": "name",
            "title": "Название тарифа",
            "visible": True,
            "orderable": True,
        },
        {
            "name": "description",
            "title": "Описание тарифа",
            "visible": True,
            "orderable": True,
        },
        {
            "name": "updated_at",
            "title": "Дата редактирования",
            "visible": True,
            "orderable": True,
        },
        {
            "name": "actions",
            "title": "",
            "visible": True,
            "orderable": False,
            "searchable": False,
            "width": "120px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build the initial queryset and apply filters."""
        queryset = Tariff.objects.all()

        if not request:
            return queryset

        filters = {
            "name__icontains": request.POST.get("name"),
            "description__icontains": request.POST.get("description"),
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
        row["updated_at"] = obj.updated_at.strftime("%d.%m.%Y - %H:%M")
        edit_url = reverse("finance:tariff_edit", args=[obj.pk])

        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                 title="Edit" onclick="event.stopPropagation();">
                    <i class="bi bi-pencil"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger delete-tariff-btn"
                        data-id="{obj.pk}"
                        data-name="{obj.name}"
                        title="Delete">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row


class CounterAjaxDatatableView(AjaxDatatableView):
    """Display a list of counters with the latest reading for each one."""

    model = Counter
    title = "Счетчики"
    initial_order = [["apartment_number_as_int", "asc"]]
    show_column_filters = False

    column_defs = [
        {"name": "apartment_number_as_int", "visible": False},
        {
            "name": "house",
            "title": "Дом",
            "foreign_field": "apartment__house__title",
            "orderable": False,
        },
        {
            "name": "section",
            "title": "Секция",
            "foreign_field": "apartment__section__name",
            "orderable": False,
        },
        {
            "name": "apartment_number",
            "title": "№ квартиры",
            "foreign_field": "apartment__number",
            "orderable": True,
        },
        {
            "name": "service",
            "title": "Счетчик",
            "foreign_field": "service__name",
            "orderable": False,
        },
        {
            "name": "latest_reading",
            "title": "Текущие показания",
            "orderable": False,
            "searchable": False,
        },
        {
            "name": "unit",
            "title": "Ед. изм.",
            "foreign_field": "service__unit__name",
            "orderable": False,
        },
        {
            "name": "actions",
            "title": "",
            "orderable": False,
            "searchable": False,
            "width": "100px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build initial queryset with latest reading annotation."""
        latest_reading_subquery = (
            CounterReading.objects.filter(counter=OuterRef("pk"))
            .order_by("-date", "-id")
            .values("value")[:1]
        )
        queryset = Counter.objects.annotate(
            latest_reading=Subquery(latest_reading_subquery),
            apartment_number_as_int=Cast("apartment__number", IntegerField()),
        ).select_related("apartment__house", "apartment__section", "service__unit")
        if not request:
            return queryset
        filters = {
            "apartment__house_id": request.POST.get("house"),
            "apartment__section_id": request.POST.get("section"),
            "apartment__number__icontains": request.POST.get("apartment_number"),
            "service_id": request.POST.get("service"),
        }
        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        """Apply filters to queryset."""
        query_conditions = Q()
        for key, value in filters.items():
            if value:
                cleaned_value = value.strip() if isinstance(value, str) else value
                query_conditions &= Q(**{key: cleaned_value})
        return queryset.filter(query_conditions)

    def customize_row(self, row, obj):
        """Customize row data."""
        from urllib.parse import urlencode

        row["house"] = obj.apartment.house.title
        row["section"] = obj.apartment.section.name if obj.apartment.section else "—"
        row["apartment_number"] = obj.apartment.number
        row["service"] = obj.service.name
        row["latest_reading"] = (
            f"{obj.latest_reading:.1f}" if obj.latest_reading is not None else "—"
        )
        row["unit"] = obj.service.unit.name
        base_url = reverse("finance:counter_reading_list")
        params = {
            "house": obj.apartment.house_id,
            "section": obj.apartment.section_id if obj.apartment.section else "",
            "apartment_number": obj.apartment.number,
            "service": obj.service_id,
        }
        history_url_with_filters = f"{base_url}?{urlencode(params)}"
        add_reading_url = (
            reverse("finance:counter_reading_add") + f"?apartment={obj.apartment.pk}"
        )
        row["DT_RowAttr"] = {
            "data-href": history_url_with_filters,
            "style": "cursor: pointer;",
        }
        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{history_url_with_filters}" class="btn btn-sm btn-info"
                 title="Открыть историю показаний" onclick="event.stopPropagation();">
                    <i class="bi bi-eye"></i>
                </a>
                <a href="{add_reading_url}" class="btn btn-sm btn-success"
                 title="Снять новое показание" onclick="event.stopPropagation();">
                    <i class="bi bi-plus"></i>
                </a>
            </div>
        """
        return row


class CounterReadingAjaxDatatableView(AjaxDatatableView):
    """Provide data for the GENERAL meter reading history table."""

    model = CounterReading
    title = "Показания счетчиков"
    initial_order = [["date", "desc"], ["id", "desc"]]
    show_column_filters = False

    column_defs = [
        {"name": "number", "title": "№", "orderable": False, "width": "80px"},
        {"name": "status", "title": "Статус", "orderable": False},
        {"name": "date", "title": "Дата", "orderable": True},
        {"name": "month", "title": "Месяц", "orderable": False},
        {
            "name": "house",
            "title": "Дом",
            "foreign_field": "counter__apartment__house__title",
            "orderable": False,
        },
        {
            "name": "section",
            "title": "Секция",
            "foreign_field": "counter__apartment__section__name",
            "orderable": False,
        },
        {
            "name": "apartment_number",
            "title": "№ квартиры",
            "foreign_field": "counter__apartment__number",
            "orderable": False,
        },
        {
            "name": "service",
            "title": "Счетчик",
            "foreign_field": "counter__service__name",
            "orderable": False,
        },
        {"name": "value", "title": "Показания", "orderable": False},
        {
            "name": "unit",
            "title": "Ед. изм.",
            "foreign_field": "counter__service__unit__name",
            "orderable": False,
        },
        {
            "name": "actions",
            "title": "",
            "orderable": False,
            "searchable": False,
            "width": "100px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build initial queryset with related objects."""
        queryset = CounterReading.objects.select_related(
            "counter__apartment__house",
            "counter__apartment__section",
            "counter__service__unit",
        )
        if not request:
            return queryset
        filters = {
            "number__icontains": request.POST.get("number"),
            "status": request.POST.get("status"),
            "counter__apartment__house_id": request.POST.get("house"),
            "counter__apartment__section_id": request.POST.get("section"),
            "counter__apartment__number__icontains": request.POST.get(
                "apartment_number"
            ),
            "counter__service_id": request.POST.get("service"),
        }
        queryset = self.apply_filters(queryset, filters)
        date_str = request.POST.get("date")
        if date_str:
            try:
                filter_date = (
                    datetime.datetime.strptime(date_str, "%d.%m.%Y")
                    .replace(tzinfo=timezone.get_current_timezone())
                    .date()
                )
                queryset = queryset.filter(date=filter_date)
            except ValueError:
                pass
        return queryset

    def apply_filters(self, queryset, filters):
        """Apply filters to queryset."""
        query_conditions = Q()
        for key, value in filters.items():
            if value:
                query_conditions &= Q(**{key: value})
        return queryset.filter(query_conditions)

    def customize_row(self, row, obj):
        """Customize row data."""
        status_map = {
            "new": ("Новое", "bg-warning"),
            "considered": ("Учтено", "bg-info"),
            "zero": ("Нулевое", "bg-secondary"),
            "paid": ("Учтено и оплачено", "bg-success"),
        }
        status_text, badge_class = status_map.get(
            obj.status, (obj.get_status_display(), "bg-light")
        )
        row["status"] = f'<span class="badge {badge_class}">{status_text}</span>'
        row["number"] = obj.number or "—"
        row["date"] = obj.date.strftime("%d.%m.%Y")
        row["month"] = obj.date.strftime("%B %Y")
        row["house"] = obj.counter.apartment.house.title
        row["section"] = (
            obj.counter.apartment.section.name if obj.counter.apartment.section else "—"
        )
        row["apartment_number"] = obj.counter.apartment.number
        row["service"] = obj.counter.service.name
        row["value"] = f"{obj.value:.3f}".rstrip("0").rstrip(".")
        row["unit"] = obj.counter.service.unit.name
        edit_url = reverse("finance:counter_reading_edit", args=[obj.pk])
        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                   title="Редактировать">
                    <i class="bi bi-pencil"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger delete-reading-btn"
                        data-id="{obj.pk}" title="Удалить">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row


class ReceiptAjaxDatatableView(AjaxDatatableView):
    """Provide data for the receipt table with consistent filtering."""

    model = Receipt
    title = "Квитанции"
    initial_order = [["date", "desc"]]
    show_column_filters = False

    column_defs = [
        {
            "name": "checkbox",
            "title": (
                '<input type="checkbox" '
                'class="form-check-input" id="select-all-receipts">'
            ),
            "orderable": False,
            "searchable": False,
            "width": "20px",
            "className": "text-center",
        },
        {"name": "number", "title": "№ квитанции", "orderable": True},
        {"name": "date", "title": "Дата", "orderable": True},
        {"name": "total_amount", "title": "Сумма (грн)", "orderable": True},
        {"name": "status", "title": "Статус", "orderable": False, "searchable": False},
        {"name": "month", "title": "Месяц", "orderable": False, "searchable": False},
        {
            "name": "apartment",
            "title": "Квартира",
            "orderable": False,
            "searchable": False,
        },
        {"name": "owner", "title": "Владелец", "orderable": False, "searchable": False},
        {
            "name": "is_posted",
            "title": "Проведена",
            "orderable": False,
            "searchable": False,
        },
        {
            "name": "actions",
            "title": "",
            "orderable": False,
            "searchable": False,
            "width": "120px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build optimized database query and collect filters."""
        queryset = Receipt.objects.select_related(
            "apartment", "apartment__house", "apartment__owner"
        )
        if not request:
            return queryset

        filters = {
            "number__icontains": request.POST.get("number"),
            "status": request.POST.get("status"),
            "date": request.POST.get("date"),
            "month": request.POST.get("month"),
            "apartment__number__icontains": request.POST.get("apartment_number"),
            "apartment__owner_id": request.POST.get("owner"),
            "is_posted": request.POST.get("is_posted"),
        }
        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        """Apply a dictionary of filters to a queryset."""
        for key, value in filters.items():
            if not value:
                continue

            cleaned_value = value.strip()

            if key == "date":
                try:
                    # Parse as date components to avoid timezone issues
                    day, month, year = map(int, cleaned_value.split("."))
                    filter_date = datetime.date(year, month, day)
                    queryset = queryset.filter(date=filter_date)
                except (ValueError, AttributeError):
                    pass

            elif key == "is_posted":
                queryset = queryset.filter(is_posted=(cleaned_value.lower() == "true"))

            elif key == "month":
                pass

            else:
                queryset = queryset.filter(**{key: cleaned_value})

        return queryset

    def customize_row(self, row, obj):
        """Customize row data."""
        row["checkbox"] = (
            f'<input type="checkbox" class="form-check-input receipt-checkbox" '
            f'data-id="{obj.pk}">'
        )
        status_map = {
            "paid": ("Оплачена", "bg-success"),
            "partially_paid": ("Частично", "bg-warning"),
            "unpaid": ("Неоплачена", "bg-danger"),
        }
        status_text, badge_class = status_map.get(obj.status)
        row["status"] = f'<span class="badge {badge_class}">{status_text}</span>'
        row["date"] = obj.date.strftime("%d.%m.%Y")
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
        row["month"] = f"{months[obj.date.month]} {obj.date.year}"
        if obj.apartment:
            row["apartment"] = f"{obj.apartment.number}, {obj.apartment.house.title}"
            row["owner"] = (
                obj.apartment.owner.get_full_name() if obj.apartment.owner else "—"
            )
        else:
            row["apartment"], row["owner"] = "—", "—"
        row["is_posted"] = "Conducted" if obj.is_posted else "Not conducted"
        row["total_amount"] = f"{obj.total_amount:.2f}"
        detail_url = reverse("finance:receipt_detail", args=[obj.pk])
        edit_url = reverse("finance:receipt_edit", args=[obj.pk])
        row["DT_RowAttr"] = {"data-detail-url": detail_url}

        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{detail_url}" class="btn btn-sm btn-secondary"
                title="Просмотр">
                    <i class="bi bi-file-earmark-text"></i>
                </a>
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                title="Редактировать">
                    <i class="bi bi-pencil"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger delete-receipt-btn"
                        data-id="{obj.pk}" data-number="{obj.number}"
                        title="Удалить">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row


class CashBoxAjaxDatatableView(AjaxDatatableView):
    """Provide data for the CashBox transaction table."""

    model = CashBox
    title = "Касса"  # noqa: RUF001
    initial_order = [["date", "desc"]]
    show_column_filters = False

    column_defs = [
        {"name": "number", "title": "№", "orderable": True},
        {"name": "date", "title": "Дата", "orderable": True},
        {"name": "is_posted", "title": "Статус", "orderable": True},
        {"name": "article", "title": "Тип платежа", "foreign_field": "article__name"},
        {"name": "owner", "title": "Владелец", "searchable": False, "orderable": False},
        {
            "name": "personal_account",
            "title": "Лицевой счет",
            "foreign_field": "personal_account__number",
        },
        {
            "name": "type_display",
            "title": "Приход/Расход",
            "searchable": False,
            "orderable": False,
        },
        {"name": "amount", "title": "Сумма (грн)", "className": "text-end"},
        {"name": "actions", "title": "", "searchable": False, "orderable": False},
    ]

    def get_initial_queryset(self, request=None):
        """Build initial queryset and apply filters."""
        queryset = CashBox.objects.select_related("article", "personal_account")

        if not request:
            return queryset

        filters = {
            "number__icontains": request.POST.get("number"),
            "date": request.POST.get("date"),
            "is_posted": request.POST.get("is_posted"),
            "article_id": request.POST.get("article"),
            "personal_account__apartment__owner_id": request.POST.get("owner"),
            "personal_account__number__icontains": request.POST.get("personal_account"),
            "article__type": request.POST.get("type"),
        }

        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        """Apply filters to the queryset."""
        for key, value in filters.items():
            if not value:
                continue

            cleaned_value = value.strip()

            if key == "date":
                try:
                    # Parse as date components to avoid timezone issues
                    day, month, year = map(int, cleaned_value.split("."))
                    filter_date = datetime.date(year, month, day)
                    queryset = queryset.filter(date=filter_date)
                except (ValueError, AttributeError):
                    pass

            elif key == "is_posted":
                queryset = queryset.filter(is_posted=(cleaned_value.lower() == "true"))
            else:
                queryset = queryset.filter(**{key: cleaned_value})

        return queryset

    def customize_row(self, row, obj):
        """Customize row rendering."""
        row["date"] = obj.date.strftime("%d.%m.%Y")

        if obj.is_posted:
            row["is_posted"] = '<span class="badge bg-success">Проведен</span>'
        else:
            row["is_posted"] = '<span class="badge bg-danger">Не проведен</span>'  # noqa: RUF001

        owner_name = "-"
        if (
            obj.personal_account
            and hasattr(obj.personal_account, "apartment")
            and obj.personal_account.apartment
            and obj.personal_account.apartment.owner
        ):
            owner_name = obj.personal_account.apartment.owner.get_full_name()
        row["owner"] = owner_name

        if obj.article.type == "income":
            row["type_display"] = '<span class="text-success">Приход</span>'
            row["amount"] = f'<span class="text-success">{obj.amount}</span>'
        else:
            row["type_display"] = '<span class="text-danger">Расход</span>'
            row["amount"] = f'<span class="text-danger">-{obj.amount}</span>'

        edit_url = reverse("finance:cashbox_update", args=[obj.pk])
        detail_url = reverse("finance:cashbox_detail", args=[obj.pk])

        row["DT_RowAttr"] = {
            "data-detail-url": detail_url,
            "style": "cursor: pointer;",
        }

        row["actions"] = f"""
                    <div class="btn-group btn-group-sm">
                        <a href="{edit_url}" class="btn btn-primary"
                         title="Редактировать" onclick="event.stopPropagation();">
                            <i class="bi bi-pencil"></i>
                        </a>
                        <button class="btn btn-danger delete-cashbox-btn"
                                data-id="{obj.pk}" title="Удалить">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                """
        return row
