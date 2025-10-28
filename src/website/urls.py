"""src/website/urls.py."""

from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("adminlte/website/home", views.AdminHomePageView.as_view(), name="admin_home"),
    path(
        "adminlte/website/about", views.AdminAboutPageView.as_view(), name="admin_about"
    ),
    path(
        "adminlte/website/services",
        views.AdminServicesPageView.as_view(),
        name="admin_services",
    ),
    path(
        "adminlte/website/contacts",
        views.AdminContactsPageView.as_view(),
        name="admin_contacts",
    ),
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("contacts/", views.ContactsPageView.as_view(), name="contacts"),
    path("services/", views.ServicesPageView.as_view(), name="services"),
    path(
        "adminlte/gallery/image/delete/<int:image_id>/",
        views.DeleteGalleryImageView.as_view(),
        name="delete_gallery_image",
    ),
    path(
        "adminlte/document/delete/<int:doc_id>/",
        views.DeleteDocumentView.as_view(),
        name="delete_document",
    ),
]
