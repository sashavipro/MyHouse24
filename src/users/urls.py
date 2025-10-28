"""src/users/urls.py."""

from django.urls import path

from . import views

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
        "api/get-user-role/",
        views.GetUserRoleApiView.as_view(),
        name="get_user_role_api",
    ),
]
