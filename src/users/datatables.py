"""src/users/datatables.py."""

import re

from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import DecimalField
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

from .models import User


class UserAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """AJAX DataTable view for User model."""

    model = User
    title = "Пользователи"

    show_column_filters = False
    show_date_filters = None

    column_defs = [
        {
            "name": "pk",
            "title": "#",
            "visible": True,
            "searchable": False,
            "orderable": False,
            "width": "40px",
        },
        {
            "name": "full_name",
            "title": "Пользователь",
            "visible": True,
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "role",
            "title": "Роль",
            "visible": True,
            "searchable": False,
            "orderable": False,
            "width": "120px",
        },
        {
            "name": "phone",
            "title": "Телефон",
            "visible": True,
            "searchable": False,
            "orderable": False,
            "width": "140px",
        },
        {
            "name": "email",
            "title": "Email (логин)",
            "visible": True,
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "status",
            "title": "Статус",
            "visible": True,
            "searchable": False,
            "orderable": False,
            "width": "100px",
        },
        {
            "name": "actions",
            "title": "",
            "visible": True,
            "searchable": False,
            "orderable": False,
            "width": "120px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build the initial queryset with filtering for employees."""
        queryset = (
            User.objects.filter(user_type="employee")
            .select_related("role")
            .order_by("id")
        )

        if request:
            full_name = request.POST.get("full_name", "").strip()
            role_id = request.POST.get("role", "").strip()
            phone = request.POST.get("phone", "").strip()
            email = request.POST.get("email", "").strip()
            status = request.POST.get("status", "").strip()

            if full_name:
                queryset = queryset.filter(
                    Q(first_name__icontains=full_name)
                    | Q(last_name__icontains=full_name)
                    | Q(middle_name__icontains=full_name)
                )

            if role_id:
                queryset = queryset.filter(role__id=role_id)

            if phone:
                queryset = queryset.filter(phone__icontains=phone)

            if email:
                queryset = queryset.filter(email__icontains=email)

            if status:
                queryset = queryset.filter(status=status)

        return queryset

    def customize_row(self, row, obj):
        """Customize each row of the DataTable."""
        # Имя пользователя
        full_name = (
            obj.get_full_name()
            if hasattr(obj, "get_full_name")
            else f"{obj.first_name or ''} {obj.last_name or ''}".strip()
        )
        if not full_name:
            full_name = "—"

        row["full_name"] = f"""
            <div style="white-space: nowrap; overflow: hidden;
                text-overflow: ellipsis; max-width: 250px;">
                {full_name}
            </div>
        """

        status_display = getattr(obj, "get_status_display", lambda: obj.status)()
        if obj.status == "active" or status_display.lower() == "активен":
            badge_class = "bg-success"
        elif obj.status == "new" or status_display.lower() == "новый":
            badge_class = "bg-warning"
        else:
            badge_class = "bg-danger"

        row["status"] = f'<span class="badge {badge_class}">{status_display}</span>'

        edit_url = reverse("users:user_edit", args=[obj.pk])
        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="#" class="btn btn-sm btn-secondary"
                    title="Отправить приглашение">
                    <i class="bi bi-arrow-repeat"></i>
                </a>
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                    title="Редактировать" onclick="event.stopPropagation();">
                    <i class="bi bi-pencil"></i>
                </a>
                <button class="btn btn-sm btn-danger delete-user"
                        data-id="{obj.pk}"
                        data-name="{full_name}"
                        title="Удалить">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row


class OwnerAjaxDatatableView(LoginRequiredMixin, AjaxDatatableView):
    """AJAX DataTable view for Owner users."""

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
            "visible": True,
            "searchable": False,
            "orderable": False,
            "width": "80px",
        },
        {
            "name": "full_name",
            "title": "ФИО",
            "visible": True,
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "phone",
            "title": "Телефон",
            "visible": True,
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "email",
            "title": "Email",
            "visible": True,
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "house",
            "title": "Дом",
            "visible": True,
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "apartment",
            "title": "Квартира",
            "visible": True,
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "date_joined",
            "title": "Добавлен",
            "visible": True,
            "searchable": False,
            "orderable": True,
        },
        {
            "name": "status",
            "title": "Статус",
            "visible": True,
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
            "visible": True,
            "searchable": False,
            "orderable": False,
            "width": "140px",
        },
    ]

    def get_initial_queryset(self, request=None):
        """Build the initial queryset with filtering for owners."""
        # FIX: C901, PLR0912 - Extract filter logic to separate methods
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

        queryset = self._apply_user_id_filter(request, queryset)
        queryset = self._apply_full_name_filter(request, queryset)
        queryset = self._apply_phone_filter(request, queryset)
        queryset = self._apply_email_filter(request, queryset)
        queryset = self._apply_house_filter(request, queryset)
        queryset = self._apply_apartment_filter(request, queryset)
        queryset = self._apply_date_joined_filter(request, queryset)
        queryset = self._apply_status_filter(request, queryset)
        queryset = self._apply_debt_filter(request, queryset)

        return queryset.distinct()

    def _apply_user_id_filter(self, request, queryset):
        """Apply user ID filter if present."""
        if user_id_filter := request.POST.get("user_id", "").strip():
            return queryset.filter(user_id__icontains=user_id_filter)
        return queryset

    def _apply_full_name_filter(self, request, queryset):
        """Apply full name filter if present."""
        if full_name := request.POST.get("full_name", "").strip():
            for word in full_name.split():
                queryset = queryset.filter(
                    Q(first_name__icontains=word)
                    | Q(last_name__icontains=word)
                    | Q(middle_name__icontains=word)
                )
        return queryset

    def _apply_phone_filter(self, request, queryset):
        """Apply phone filter if present."""
        if phone := request.POST.get("phone", "").strip():
            return queryset.filter(phone__icontains=phone)
        return queryset

    def _apply_email_filter(self, request, queryset):
        """Apply email filter if present."""
        if email := request.POST.get("email", "").strip():
            return queryset.filter(email__icontains=email)
        return queryset

    def _apply_house_filter(self, request, queryset):
        """Apply house filter if present."""
        if house_id := request.POST.get("house", "").strip():
            return queryset.filter(apartments__house_id=house_id)
        return queryset

    def _apply_apartment_filter(self, request, queryset):
        """Apply apartment filter if present."""
        if apartment := request.POST.get("apartment", "").strip():
            return queryset.filter(apartments__number__icontains=apartment)
        return queryset

    def _apply_date_joined_filter(self, request, queryset):
        """Apply date joined filter if present."""
        if date_joined := request.POST.get("date_joined", "").strip():
            try:
                if re.match(r"^\d{4}$", date_joined):
                    return queryset.filter(date_joined__year=int(date_joined))
                if re.match(r"^\d{4}-\d{2}$", date_joined):
                    year, month = date_joined.split("-")
                    return queryset.filter(
                        date_joined__year=int(year), date_joined__month=int(month)
                    )
                if re.match(r"^\d{4}-\d{2}-\d{2}$", date_joined):
                    return queryset.filter(date_joined__date=date_joined)
            except (ValueError, TypeError):
                pass
        return queryset

    def _apply_status_filter(self, request, queryset):
        """Apply status filter if present."""
        if status := request.POST.get("status", "").strip():
            return queryset.filter(status=status)
        return queryset

    def _apply_debt_filter(self, request, queryset):
        """Apply debt filter if present."""
        if has_debt := request.POST.get("has_debt", "").strip():
            if has_debt == "yes":
                return queryset.filter(total_balance__lt=0)
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

        all_apartments = obj.apartments.all()

        if house_filter_id:
            apartments_to_display = [
                apt
                for apt in all_apartments
                if apt.house and str(apt.house.id) == house_filter_id
            ]
        else:
            apartments_to_display = all_apartments

        if apartments_to_display:
            houses_apartments = {}
            for apt in apartments_to_display:
                if apt.house:
                    if apt.house not in houses_apartments:
                        houses_apartments[apt.house] = []
                    houses_apartments[apt.house].append(apt)

            house_html_parts = []
            apartment_html_parts = []

            for house, apt_list in houses_apartments.items():
                house_url = reverse("building:house_detail", args=[house.pk])
                # FIX: E501 - Split long line
                house_link = (
                    f'<a href="{house_url}" '
                    f'onclick="event.stopPropagation();">{house.title}</a>'
                )
                house_html_parts.append(house_link)

                apt_links = []
                for apt in apt_list:
                    apartment_url = reverse("building:apartment_detail", args=[apt.pk])
                    # FIX: E501 - Split long line
                    apt_link = (
                        f'<a href="{apartment_url}" '
                        f'onclick="event.stopPropagation();">№ {apt.number}</a>'
                    )
                    apt_links.append(apt_link)
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
                            title="Отправить сообщение"
                                onclick="event.stopPropagation();">
                            <i class="bi bi-envelope"></i>
                        </a>
                        <a href="{edit_url}" class="btn btn-sm btn-primary"
                            title="Редактировать" onclick="event.stopPropagation();">
                            <i class="bi bi-pencil"></i>
                        </a>
                        <button type="button"
                                class="btn btn-sm btn-danger delete-owner-btn"
                                data-id="{obj.pk}"
                                data-name="{full_name}"
                                title="Удалить">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                """
        return row
