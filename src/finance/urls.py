"""src/finance/urls.py."""

from django.urls import path

from . import views

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
]
