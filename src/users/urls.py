"""src/users/urls.py."""

from django.urls import path

from . import views
from .datatables import OwnerAjaxDatatableView
from .datatables import UserAjaxDatatableView

app_name = "users"

urlpatterns = [
    path("adminlte/roles/", views.AdminRolesPageView.as_view(), name="admin_roles"),
    path("adminlte/users/", views.UserListView.as_view(), name="user_list"),
    path("adminlte/users/add/", views.UserCreateView.as_view(), name="user_add"),
    path(
        "adminlte/users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"
    ),
    path(
        "adminlte/users/<int:pk>/edit/",
        views.UserUpdateView.as_view(),
        name="user_edit",
    ),
    path(
        "ajax-datatable/users/",
        UserAjaxDatatableView.as_view(),
        name="ajax_datatable_users",
    ),
    path("adminlte/owners/", views.OwnerListView.as_view(), name="owner_list"),
    path("adminlte/owners/add/", views.OwnerCreateView.as_view(), name="owner_add"),
    path(
        "adminlte/owners/<int:pk>/",
        views.OwnerDetailView.as_view(),
        name="owner_detail",
    ),
    path(
        "adminlte/owners/<int:pk>/edit/",
        views.OwnerUpdateView.as_view(),
        name="owner_edit",
    ),
    path(
        "ajax-datatable/owners/",
        OwnerAjaxDatatableView.as_view(),
        name="ajax_datatable_owners",
    ),
]
