"""src/cabinet/urls.py."""

from django.urls import path

from . import views
from .datatables import CabinetMessageAjaxDatatableView
from .datatables import CabinetReceiptAjaxDatatableView
from .datatables import CabinetTicketAjaxDatatableView

app_name = "cabinet"

urlpatterns = [
    path("cabinet/", views.CabinetView.as_view(), name="cabinet"),
    path("cabinet/edit/", views.CabinetUpdateView.as_view(), name="cabinet_edit"),
    path(
        "cabinet/messages/",
        views.CabinetMessageListView.as_view(),
        name="cabinet_message_list",
    ),
    path(
        "cabinet/messages/<int:pk>/",
        views.CabinetMessageDetailView.as_view(),
        name="cabinet_message_detail",
    ),
    path(
        "ajax-datatable/cabinet/messages/",
        CabinetMessageAjaxDatatableView.as_view(),
        name="ajax_datatable_cabinet_messages",
    ),
    path(
        "cabinet/tariffs/<int:apartment_id>/",
        views.CabinetTariffDetailView.as_view(),
        name="cabinet_tariff_detail",
    ),
    path(
        "cabinet/receipts/",
        views.CabinetReceiptListView.as_view(),
        name="cabinet_receipt_list",
    ),
    path(
        "cabinet/receipts/apartment/<int:apartment_id>/",
        views.CabinetReceiptListView.as_view(),
        name="cabinet_receipt_list_apartment",
    ),
    path(
        "cabinet/receipts/<int:pk>/",
        views.CabinetReceiptDetailView.as_view(),
        name="cabinet_receipt_detail",
    ),
    path(
        "ajax-datatable/cabinet/receipts/",
        CabinetReceiptAjaxDatatableView.as_view(),
        name="ajax_datatable_cabinet_receipts",
    ),
    path(
        "cabinet/tickets/",
        views.CabinetTicketListView.as_view(),
        name="cabinet_ticket_list",
    ),
    path(
        "cabinet/tickets/add/",
        views.CabinetTicketCreateView.as_view(),
        name="cabinet_ticket_add",
    ),
    path(
        "ajax-datatable/cabinet/tickets/",
        CabinetTicketAjaxDatatableView.as_view(),
        name="ajax_datatable_cabinet_tickets",
    ),
]
