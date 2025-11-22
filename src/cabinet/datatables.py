"""src/cabinet/datatables.py."""

import datetime
import re

from ajax_datatable import AjaxDatatableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import escape

from src.finance.models import Receipt
from src.users.models import Message
from src.users.models import MessageRecipient
from src.users.models import Ticket

SNIPPET_LENGTH = 70
MIN_YEAR = 1900
MAX_YEAR = 2100
MAX_DAYS_IN_MONTH = 31


class CabinetMessageAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """Provide data for the message table in the owner's personal account."""

    model = Message
    title = "Входящие сообщения"
    initial_order = [["date", "desc"]]

    column_defs = [
        {
            "name": "checkbox",
            "title": "",
            "orderable": False,
            "searchable": False,
            "width": "20px",
            "className": "text-center",
        },
        {"name": "sender", "title": "Отправитель", "orderable": False},
        {"name": "text", "title": "Текст", "orderable": False},
        {"name": "date", "title": "Дата", "orderable": True},
        {
            "name": "actions",
            "title": "",
            "orderable": False,
            "searchable": False,
            "width": "50px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build the initial queryset and collect filters."""
        visible_message_ids = MessageRecipient.objects.filter(
            user=request.user, is_hidden=False
        ).values_list("message_id", flat=True)

        queryset = Message.objects.filter(pk__in=visible_message_ids).select_related(
            "sender"
        )

        if not request:
            return queryset

        filters = {
            "search_value": request.POST.get("search_value"),
        }
        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        """Apply a dictionary of filters to a queryset."""
        search_value = filters.get("search_value", "").strip()

        if search_value:
            query = (
                Q(title__icontains=search_value)
                | Q(text__icontains=search_value)
                | Q(sender__first_name__icontains=search_value)
                | Q(sender__last_name__icontains=search_value)
            )
            queryset = queryset.filter(query).distinct()

        return queryset

    def customize_row(self, row, obj):
        """Fully generates data for a table row."""
        row["checkbox"] = (
            f'<input type="checkbox"'
            f' class="form-check-input message-checkbox" data-id="{obj.pk}">'
        )
        row["sender"] = (
            obj.sender.get_full_name() if obj.sender else "Системное сообщение"
        )

        text_snippet = (
            (obj.text[:SNIPPET_LENGTH] + "...")
            if len(obj.text) > SNIPPET_LENGTH
            else obj.text
        )
        row["text"] = f"<strong>{escape(obj.title)}</strong> - {escape(text_snippet)}"

        row["date"] = obj.date.strftime("%d.%m.%Y - %H:%M")
        row["actions"] = ""
        row["DT_RowAttr"] = {
            "data-detail-url": reverse("cabinet:cabinet_message_detail", args=[obj.pk])
        }
        return row


class CabinetReceiptAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """Provide data for the receipt table in your personal account."""

    model = Receipt
    title = "Квитанции"
    initial_order = [["date", "desc"]]

    column_defs = [
        {"name": "number", "title": "№", "orderable": True},
        {"name": "date", "title": "Дата", "orderable": True},
        {"name": "status", "title": "Статус", "searchable": True, "orderable": False},
        {
            "name": "total_amount",
            "title": "Сумма",
            "className": "text-end",
            "orderable": True,
        },
    ]

    def _filter_by_date(self, queryset, value):
        """Apply date-based filters to the queryset for the 'date' field."""
        try:
            if re.match(r"^\d{1,2}\.\d{1,2}\.\d{4}$", value):
                filter_date = datetime.datetime.strptime(value, "%d.%m.%Y").date()  # noqa: DTZ007
                return queryset.filter(date=filter_date)
            if re.match(r"^\d{1,2}\.\d{4}$", value):
                month, year = value.split(".")
                return queryset.filter(date__month=int(month), date__year=int(year))
            if re.match(r"^\d{4}$", value):
                year = int(value)
                if MIN_YEAR < year < MAX_YEAR:
                    return queryset.filter(date__year=year)
            if re.match(r"^\d{1,2}$", value):
                day_or_month = int(value)
                if 1 <= day_or_month <= MAX_DAYS_IN_MONTH:
                    return queryset.filter(
                        Q(date__day=day_or_month) | Q(date__month=day_or_month)
                    )
        except (ValueError, TypeError):
            pass
        return queryset

    def get_initial_queryset(self, request=None):
        """Build the initial queryset and collect filters."""
        queryset = Receipt.objects.filter(apartment__owner=request.user)

        apartment_id = request.GET.get("apartment_id")
        if apartment_id:
            queryset = queryset.filter(apartment_id=apartment_id)

        if not request:
            return queryset

        filters = {
            "date": request.POST.get("date_filter"),
            "status": request.POST.get("status_filter"),
        }
        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        """Apply a dictionary of filters to a queryset."""
        for key, value in filters.items():
            if value:
                cleaned_value = value.strip()
                if key == "date":
                    queryset = self._filter_by_date(queryset, cleaned_value)
                else:  # для 'status'
                    queryset = queryset.filter(**{key: cleaned_value})

        return queryset

    def customize_row(self, row, obj):
        """Prepare data for table rows."""
        row["date"] = obj.date.strftime("%d.%m.%Y")
        status_map = {
            "paid": ("Оплачена", "bg-success"),
            "partially_paid": ("Частично", "bg-warning"),
            "unpaid": ("Неоплачена", "bg-danger"),
        }
        status_text, badge_class = status_map.get(obj.status, ("-", "bg-secondary"))
        row["status"] = f'<span class="badge {badge_class}">{status_text}</span>'
        row["total_amount"] = f"{obj.total_amount:.2f}"
        row["DT_RowAttr"] = {
            "data-detail-url": reverse("cabinet:cabinet_receipt_detail", args=[obj.pk])
        }
        return row


class CabinetTicketAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """Provide data for the ticket table in the owner's personal account."""

    model = Ticket
    title = "Заявки вызова мастера"
    initial_order = [["pk", "desc"]]

    column_defs = [
        {"name": "pk", "title": "№ заявки", "width": "80px"},
        {"name": "role", "title": "Тип мастера", "foreign_field": "role__name"},
        {"name": "description", "title": "Описание"},
        {
            "name": "date_time",
            "title": "Удобное время",
            "searchable": False,
            "orderable": False,
        },
        {"name": "status", "title": "Статус", "width": "120px"},
        {
            "name": "actions",
            "title": "",
            "searchable": False,
            "orderable": False,
            "width": "50px",
            "className": "text-center",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Return tickets belonging to the current user."""
        return Ticket.objects.filter(user=request.user).select_related("role")

    def customize_row(self, row, obj):
        """Customize row data."""
        row["pk"] = obj.pk

        row["date_time"] = (
            f"{obj.date.strftime('%d.%m.%Y')} - {obj.time.strftime('%H:%M')}"
        )

        status_map = {
            "new": ("Новое", "bg-primary"),
            "in_progress": ("В работе", "bg-warning"),  # noqa: RUF001
            "done": ("Выполнено", "bg-success"),
        }
        status_text, badge_class = status_map.get(
            obj.status, (obj.get_status_display(), "bg-secondary")
        )
        row["status"] = f'<span class="badge {badge_class}">{status_text}</span>'

        row["actions"] = f"""
            <button type="button" class="btn btn-sm btn-default delete-ticket-btn"
                    data-id="{obj.pk}" title="Удалить">
                <i class="bi bi-trash text-danger"></i>
            </button>
        """
        return row
