"""src/building/urls.py."""

from django.urls import path

from . import views
from .datatables import ApartmentAjaxDatatableView
from .datatables import HouseAjaxDatatableView
from .datatables import PersonalAccountAjaxDatatableView

app_name = "building"


urlpatterns = [
    path("adminlte/houses/", views.HouseListView.as_view(), name="house_list"),
    path("adminlte/house/add/", views.HouseCreateView.as_view(), name="house_add"),
    path(
        "adminlte/house/<int:pk>/", views.HouseDetailView.as_view(), name="house_detail"
    ),
    path(
        "adminlte/house/<int:pk>/edit/",
        views.HouseUpdateView.as_view(),
        name="house_edit",
    ),
    path(
        "ajax-datatable/houses/",
        HouseAjaxDatatableView.as_view(),
        name="ajax_datatable_houses",
    ),
    path(
        "adminlte/apartments/", views.ApartmentListView.as_view(), name="apartment_list"
    ),
    path(
        "adminlte/apartments/add/",
        views.ApartmentCreateView.as_view(),
        name="apartment_add",
    ),
    path(
        "adminlte/apartments/<int:pk>/",
        views.ApartmentDetailView.as_view(),
        name="apartment_detail",
    ),
    path(
        "adminlte/apartments/<int:pk>/edit/",
        views.ApartmentUpdateView.as_view(),
        name="apartment_edit",
    ),
    path(
        "ajax-datatable/apartments/",
        ApartmentAjaxDatatableView.as_view(),
        name="ajax_datatable_apartments",
    ),
    path(
        "adminlte/personal-accounts/",
        views.PersonalAccountListView.as_view(),
        name="personal_account_list",
    ),
    path(
        "adminlte/personal-accounts/add/",
        views.PersonalAccountCreateView.as_view(),
        name="personal_account_add",
    ),
    path(
        "adminlte/personal-accounts/<int:pk>/",
        views.PersonalAccountDetailView.as_view(),
        name="personal_account_detail",
    ),
    path(
        "adminlte/personal-accounts/<int:pk>/edit/",
        views.PersonalAccountUpdateView.as_view(),
        name="personal_account_edit",
    ),
    path(
        "ajax-datatable/personal-accounts/",
        PersonalAccountAjaxDatatableView.as_view(),
        name="ajax_datatable_personal_accounts",
    ),
]
