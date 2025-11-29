"""src/finance/urls.py."""

from django.urls import path

from . import views
from .datatables import ArticleAjaxDatatableView
from .datatables import CashBoxAjaxDatatableView
from .datatables import CounterAjaxDatatableView
from .datatables import CounterReadingAjaxDatatableView
from .datatables import ReceiptAjaxDatatableView
from .datatables import TariffAjaxDatatableView

app_name = "finance"


urlpatterns = [
    path("adminlte/", views.AdminStatsView.as_view(), name="admin_stats"),
    path(
        "adminlte/services/", views.ManageServicesView.as_view(), name="manage_services"
    ),
    path("adminlte/tariffs/", views.TariffListView.as_view(), name="tariff_list"),
    path("adminlte/tariffs/add/", views.TariffCreateView.as_view(), name="tariff_add"),
    path(
        "adminlte/tariffs/<int:pk>/",
        views.TariffDetailView.as_view(),
        name="tariff_detail",
    ),
    path(
        "adminlte/tariffs/<int:pk>/edit/",
        views.TariffUpdateView.as_view(),
        name="tariff_edit",
    ),
    path(
        "ajax-datatable/tariffs/",
        TariffAjaxDatatableView.as_view(),
        name="ajax_datatable_tariffs",
    ),
    path("adminlte/articles/", views.ArticleListView.as_view(), name="article_list"),
    path(
        "adminlte/articles/add/", views.ArticleCreateView.as_view(), name="article_add"
    ),
    path(
        "adminlte/articles/<int:pk>/edit/",
        views.ArticleUpdateView.as_view(),
        name="article_edit",
    ),
    path(
        "ajax-datatable/articles/",
        ArticleAjaxDatatableView.as_view(),
        name="ajax_datatable_articles",
    ),
    path(
        "adminlte/payment-details/",
        views.PaymentDetailsUpdateView.as_view(),
        name="payment_details",
    ),
    path("adminlte/counters/", views.CounterListView.as_view(), name="counter_list"),
    path(
        "ajax-datatable/counters/",
        CounterAjaxDatatableView.as_view(),
        name="ajax_datatable_counters",
    ),
    path(
        "adminlte/counters/readings/",
        views.CounterReadingListView.as_view(),
        name="counter_reading_list",
    ),
    path(
        "ajax-datatable/counter-readings/",
        CounterReadingAjaxDatatableView.as_view(),
        name="ajax_datatable_counter_readings",
    ),
    path(
        "adminlte/counters/readings/add/",
        views.CounterReadingCreateView.as_view(),
        name="counter_reading_add",
    ),
    path(
        "adminlte/counters/readings/<int:pk>/edit/",
        views.CounterReadingUpdateView.as_view(),
        name="counter_reading_edit",
    ),
    path("adminlte/receipts/", views.ReceiptListView.as_view(), name="receipt_list"),
    path(
        "adminlte/receipts/add/", views.ReceiptCreateView.as_view(), name="receipt_add"
    ),
    path(
        "adminlte/receipts/<int:pk>/",
        views.ReceiptDetailView.as_view(),
        name="receipt_detail",
    ),
    path(
        "adminlte/receipts/<int:pk>/edit/",
        views.ReceiptUpdateView.as_view(),
        name="receipt_edit",
    ),
    path(
        "ajax-datatable/receipts/",
        ReceiptAjaxDatatableView.as_view(),
        name="ajax_datatable_receipts",
    ),
    path(
        "adminlte/receipts/<int:pk>/print/",
        views.ReceiptPrintFormView.as_view(),
        name="receipt_print_form",
    ),
    path(
        "adminlte/receipts/templates/",
        views.ReceiptTemplateSettingsView.as_view(),
        name="receipt_template_settings",
    ),
    path("adminlte/cashbox/", views.CashBoxListView.as_view(), name="cashbox_list"),
    path(
        "adminlte/cashbox/income/add/",
        views.CashBoxIncomeCreateView.as_view(),
        name="cashbox_income_add",
    ),
    path(
        "adminlte/cashbox/expense/add/",
        views.CashBoxExpenseCreateView.as_view(),
        name="cashbox_expense_add",
    ),
    path(
        "adminlte/cashbox/<int:pk>/edit/",
        views.CashBoxUpdateView.as_view(),
        name="cashbox_update",
    ),
    path(
        "ajax-datatable/cashbox/",
        CashBoxAjaxDatatableView.as_view(),
        name="ajax_datatable_cashbox",
    ),
    path(
        "adminlte/cashbox/<int:pk>/",
        views.CashBoxDetailView.as_view(),
        name="cashbox_detail",
    ),
    path(
        "adminlte/cashbox/export/",
        views.ExportCashBoxExcelView.as_view(),
        name="cashbox_export",
    ),
]
