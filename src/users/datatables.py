"""src/users/datatables.py."""

import re

from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import DecimalField
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.html import escape

from .models import Message
from .models import MessageRecipient
from .models import User

MIN_YEAR = 1900
MAX_YEAR = 2100
MAX_DAYS_IN_MONTH = 31
SNIPPET_LENGTH = 70
RECIPIENT_DISPLAY_LIMIT = 2


class UserAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """Provide server-side processing for the User (employee) list DataTable."""

    model = User
    title = "Пользователи"
    show_column_filters = False

    column_defs = [
        {
            "name": "pk",
            "title": "#",
            "searchable": False,
            "orderable": True,
            "width": "40px",
        },
        {
            "name": "full_name",
            "title": "Пользователь",
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "role",
            "title": "Роль",
            "searchable": False,
            "orderable": False,
            "width": "120px",
        },
        {
            "name": "phone",
            "title": "Телефон",
            "searchable": False,
            "orderable": False,
            "width": "140px",
        },
        {
            "name": "email",
            "title": "Email (логин)",
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "status",
            "title": "Статус",
            "searchable": False,
            "orderable": False,
            "width": "100px",
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
        """Build the initial queryset and applies filters for employees."""
        queryset = (
            User.objects.filter(user_type="employee")
            .select_related("role")
            .order_by("pk")
        )

        if not request:
            return queryset

        filters = {
            "full_name": request.POST.get("full_name"),
            "role_id": request.POST.get("role"),
            "phone__icontains": request.POST.get("phone"),
            "email__icontains": request.POST.get("email"),
            "status": request.POST.get("status"),
        }

        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        """Apply a dictionary of filters to the queryset."""
        query_conditions = Q()

        for key, value in filters.items():
            if not value:
                continue

            cleaned_value = value.strip() if isinstance(value, str) else value

            if key == "full_name":
                query_conditions &= (
                    Q(first_name__icontains=cleaned_value)
                    | Q(last_name__icontains=cleaned_value)
                    | Q(middle_name__icontains=cleaned_value)
                )
                continue

            query_conditions &= Q(**{key: cleaned_value})

        return queryset.filter(query_conditions)

    def customize_row(self, row, obj):
        """Customize each row of the DataTable."""
        full_name = obj.get_full_name() or "—"

        row["full_name"] = f"""
            <div style="white-space: nowrap; overflow: hidden;
             text-overflow: ellipsis; max-width: 250px;">
                {full_name}
            </div>
        """

        status_display = obj.get_status_display()
        badge_class = "bg-secondary"
        if obj.status == "active":
            badge_class = "bg-success"
        elif obj.status == "new":
            badge_class = "bg-warning"
        elif obj.status == "inactive":
            badge_class = "bg-danger"
        row["status"] = f'<span class="badge {badge_class}">{status_display}</span>'

        edit_url = reverse("users:user_edit", args=[obj.pk])
        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="#" class="btn btn-sm btn-secondary" title="Send Invitation">
                    <i class="bi bi-arrow-repeat"></i>
                </a>
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                title="Edit" onclick="event.stopPropagation();">
                    <i class="bi bi-pencil"></i>
                </a>
                <button class="btn btn-sm btn-danger delete-user"
                        data-id="{obj.pk}"
                        data-name="{full_name}"
                        title="Delete">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row


class OwnerAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """Provide server-side processing for the Owner list DataTable."""

    model = User
    title = "Владельцы квартир"
    show_column_filters = False
    show_date_filters = None

    column_defs = [
        {
            "name": "pk",
            "title": "PK",
            "visible": False,
            "searchable": False,
            "orderable": True,
        },
        {
            "name": "owner_id_display",
            "title": "ID",
            "searchable": False,
            "orderable": False,
            "width": "80px",
        },
        {"name": "full_name", "title": "ФИО", "searchable": False, "orderable": False},
        {"name": "phone", "title": "Телефон", "searchable": False, "orderable": False},
        {"name": "email", "title": "Email", "searchable": False, "orderable": False},
        {"name": "house", "title": "Дом", "searchable": False, "orderable": False},
        {
            "name": "apartment",
            "title": "Квартира",
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "date_joined",
            "title": "Добавлен",
            "searchable": False,
            "orderable": True,
        },
        {
            "name": "status",
            "title": "Статус",
            "searchable": False,
            "orderable": False,
            "width": "120px",
        },
        {
            "name": "has_debt",
            "title": "Есть долг",
            "searchable": False,
            "orderable": False,
            "width": "100px",
        },
        {
            "name": "actions",
            "title": "",
            "searchable": False,
            "orderable": False,
            "width": "140px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build the initial queryset with filtering for owners."""
        self.request = request
        queryset = (
            User.objects.filter(user_type="owner")
            .prefetch_related("apartments__house", "apartments__personal_account")
            .annotate(
                total_balance=Sum(
                    Coalesce(
                        "apartments__personal_account__balance",
                        0.0,
                        output_field=DecimalField(),
                    )
                )
            )
            .order_by("pk")
        )

        if not request:
            return queryset.distinct()

        filters = {
            "user_id": request.POST.get("user_id"),
            "full_name": request.POST.get("full_name"),
            "phone": request.POST.get("phone"),
            "email": request.POST.get("email"),
            "house": request.POST.get("house"),
            "apartment": request.POST.get("apartment"),
            "date_joined": request.POST.get("date_joined"),
            "status": request.POST.get("status"),
            "has_debt": request.POST.get("has_debt"),
        }

        return self.apply_filters(queryset, filters).distinct()

    def _filter_by_date(self, queryset, value):
        """Apply date-based filters to the queryset."""
        try:
            if re.match(r"^\d{1,2}\.\d{1,2}\.\d{4}$", value):
                day, month, year = value.split(".")
                date_iso = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                return queryset.filter(date_joined__date=date_iso)
            if re.match(r"^\d{1,2}\.\d{4}$", value):
                month, year = value.split(".")
                return queryset.filter(
                    date_joined__month=int(month), date_joined__year=int(year)
                )
            if re.match(r"^\d{4}$", value):
                year = int(value)
                if MIN_YEAR < year < MAX_YEAR:
                    return queryset.filter(date_joined__year=year)
            if re.match(r"^\d{1,2}$", value):
                day_or_month = int(value)
                if 1 <= day_or_month <= MAX_DAYS_IN_MONTH:
                    return queryset.filter(date_joined__day=day_or_month)
        except (ValueError, TypeError):
            pass
        return queryset

    def apply_filters(self, queryset, filters):
        """Apply a dictionary of filters to the queryset."""
        for key, value in filters.items():
            if not value or not value.strip():
                continue

            cleaned_value = value.strip().lower()

            if key == "full_name":
                for word in cleaned_value.split():
                    queryset = queryset.filter(
                        Q(first_name__icontains=word)
                        | Q(last_name__icontains=word)
                        | Q(middle_name__icontains=word)
                    )
            elif key == "date_joined":
                queryset = self._filter_by_date(queryset, cleaned_value)
            elif key == "has_debt":
                if cleaned_value == "yes":
                    queryset = queryset.filter(total_balance__lt=0)
            elif key == "house":
                queryset = queryset.filter(apartments__house_id=cleaned_value)
            elif key == "apartment":
                queryset = queryset.filter(apartments__number__icontains=cleaned_value)
            else:
                lookup = (
                    f"{key}__icontains" if key in ["user_id", "phone", "email"] else key
                )
                queryset = queryset.filter(**{lookup: cleaned_value})

        return queryset

    def render_column(self, row, column):
        """Override column rendering to handle custom columns safely."""
        custom_columns = [
            "owner_id_display",
            "full_name",
            "house",
            "apartment",
            "status",
            "actions",
            "has_debt",
        ]
        if column in custom_columns:
            return ""

        try:
            if hasattr(row, column):
                value = getattr(row, column)
                if column == "date_joined" and value:
                    return value.strftime("%d.%m.%Y %H:%M")
                return value if value is not None else "—"
        except (AttributeError, TypeError):
            pass
        return "—"

    def customize_row(self, row, obj):
        """Customize the data for each row in the DataTable."""
        row["pk"] = obj.pk
        row["owner_id_display"] = obj.user_id or "—"
        full_name = obj.get_full_name() or "—"
        row["full_name"] = full_name
        row["phone"] = obj.phone or "—"
        row["email"] = obj.email or "—"
        row["date_joined"] = obj.date_joined.strftime("%d.%m.%Y")

        status_display = obj.get_status_display()
        status_colors = {
            "active": "bg-success",
            "new": "bg-warning",
            "inactive": "bg-danger",
        }
        badge_class = status_colors.get(obj.status, "bg-secondary")
        row["status"] = f'<span class="badge {badge_class}">{status_display}</span>'

        house_filter_id = (
            self.request.POST.get("house", "").strip()
            if hasattr(self, "request")
            else None
        )
        all_apartments = list(obj.apartments.all())

        apartments_to_display = (
            [
                apt
                for apt in all_apartments
                if apt.house and str(apt.house.id) == house_filter_id
            ]
            if house_filter_id
            else all_apartments
        )

        if apartments_to_display:
            houses_apartments = {}
            for apt in apartments_to_display:
                if apt.house and apt.house not in houses_apartments:
                    houses_apartments[apt.house] = []
                if apt.house:
                    houses_apartments[apt.house].append(apt)

            house_html_parts = []
            apartment_html_parts = []
            for house, apt_list in houses_apartments.items():
                house_url = reverse("building:house_detail", args=[house.pk])
                house_link = (
                    f'<a href="{house_url}" '
                    f'onclick="event.stopPropagation();">{house.title}</a>'
                )
                house_html_parts.append(house_link)
                apt_links = [
                    (
                        f'<a href="{reverse("building:apartment_detail",args=[apt.pk])}'
                        f'" onclick="event.stopPropagation();">№ {apt.number}</a>'
                    )
                    for apt in apt_list
                ]
                apartment_html_parts.append(", ".join(apt_links))
            row["house"] = "<br>".join(house_html_parts)
            row["apartment"] = "<br>".join(apartment_html_parts)
        else:
            row["house"] = "—"
            row["apartment"] = "—"

        total_balance = obj.total_balance or 0
        row["has_debt"] = (
            '<span class="text-danger fw-bold">Да</span>' if total_balance < 0 else ""
        )
        detail_url = reverse("users:owner_detail", args=[obj.pk])
        row["DT_RowAttr"] = {"data-detail-url": detail_url}
        edit_url = reverse("users:owner_edit", args=[obj.pk])
        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="#" class="btn btn-sm btn-secondary"
                 title="Send message" onclick="event.stopPropagation();">
                    <i class="bi bi-envelope"></i>
                </a>
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                 title="Edit" onclick="event.stopPropagation();">
                    <i class="bi bi-pencil"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger delete-owner-btn"
                        data-id="{obj.pk}" data-name="{full_name}" title="Delete">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row


class MessageAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """Provide data for the sent messages table (admin panel).

    Brought to a uniform structure.
    """

    model = Message
    title = "Сообщения"
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
        {"name": "recipients", "title": "Получатели", "orderable": False},
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
        """Build the initial queryset of messages sent by the current user."""
        queryset = Message.objects.filter(sender=request.user).prefetch_related(
            "recipients"
        )
        if not request:
            return queryset
        search_value = request.POST.get("search_value", "").strip()
        if search_value:
            query = (
                Q(title__icontains=search_value)
                | Q(text__icontains=search_value)
                | Q(recipients__first_name__icontains=search_value)
                | Q(recipients__last_name__icontains=search_value)
            )
            queryset = queryset.filter(query).distinct()
        return queryset

    def customize_row(self, row, obj):
        """Fully generates data for a table row."""
        row["checkbox"] = (
            f'<input type="checkbox" '
            f'class="form-check-input message-checkbox" data-id="{obj.pk}">'
        )
        recipients = obj.recipients.all()
        if recipients.count() > RECIPIENT_DISPLAY_LIMIT:
            recipients_str = ", ".join(
                [r.get_full_name() for r in recipients[:RECIPIENT_DISPLAY_LIMIT]]
            )
            recipients_str += f" и еще {recipients.count() - RECIPIENT_DISPLAY_LIMIT}"
        else:
            recipients_str = ", ".join([r.get_full_name() for r in recipients])
        row["recipients"] = recipients_str or "Нет получателей"

        text_snippet = (
            (obj.text[:SNIPPET_LENGTH] + "...")
            if len(obj.text) > SNIPPET_LENGTH
            else obj.text
        )
        row["text"] = f"<strong>{escape(obj.title)}</strong> - {escape(text_snippet)}"
        row["date"] = obj.date.strftime("%d.%m.%Y - %H:%M")
        row["actions"] = ""
        row["DT_RowAttr"] = {
            "data-detail-url": reverse("users:message_detail", args=[obj.pk])
        }
        return row


class CabinetMessageAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """Provide data for the message table in the owner's personal account.

    Brought to a uniform structure.
    """

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
        """Return visible messages addressed to the current user."""
        visible_message_ids = MessageRecipient.objects.filter(
            user=request.user, is_hidden=False
        ).values_list("message_id", flat=True)

        queryset = Message.objects.filter(pk__in=visible_message_ids).select_related(
            "sender"
        )

        if not request:
            return queryset

        search_value = request.POST.get("search_value", "").strip()
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
            f'<input type="checkbox" '
            f'class="form-check-input message-checkbox" data-id="{obj.pk}">'
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
            "data-detail-url": reverse("users:cabinet_message_detail", args=[obj.pk])
        }
        return row
