"""src/finance/datatables.py."""

from ajax_datatable.views import AjaxDatatableView
from django.urls import reverse

from .models import Article
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
    """Provides server-side processing for the Tariff list DataTable."""

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
        """Build the initial queryset with custom filtering."""
        queryset = Tariff.objects.all()
        if request:
            name = request.POST.get("name", "").strip()
            description = request.POST.get("description", "").strip()
            if name:
                queryset = queryset.filter(name__icontains=name)
            if description:
                queryset = queryset.filter(description__icontains=description)
        return queryset

    def customize_row(self, row, obj):
        """Customize each row of the DataTable."""
        row["updated_at"] = obj.updated_at.strftime("%d.%m.%Y - %H:%M")
        edit_url = reverse("finance:tariff_edit", args=[obj.pk])

        row["actions"] = f"""
            <div class="text-end" style="white-space: nowrap;">
                <a href="{edit_url}" class="btn btn-sm btn-primary"
                    title="Редактировать" onclick="event.stopPropagation();">
                    <i class="bi bi-pencil"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger delete-tariff-btn"
                        data-id="{obj.pk}"
                        data-name="{obj.name}"
                        title="Удалить">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        """
        return row
