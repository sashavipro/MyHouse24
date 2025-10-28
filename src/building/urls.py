"""src/building/urls.py."""

from django.urls import path

from . import views

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
]
