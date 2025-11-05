"""src/finance/urls.py."""

from django.urls import path

from . import views
from .datatables import ArticleAjaxDatatableView
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
]
