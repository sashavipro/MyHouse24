from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('adminlte/', views.admin_stats, name='admin_stats'),
    path('adminlte/website/home', views.admin_home_page, name='admin_home'),
    path('adminlte/website/about', views.admin_about_page, name='admin_about'),
    path('adminlte/website/services', views.admin_services_page, name='admin_services'),
    path('adminlte/website/contacts', views.admin_contacts_page, name='admin_contacts'),


    path('adminlte/gallery/image/delete/<int:image_id>/', views.delete_gallery_image, name='delete_gallery_image'),
    path('adminlte/document/delete/<int:doc_id>/', views.delete_document, name='delete_document'),


    path('', views.home_page, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('services/', views.services, name='services'),

]