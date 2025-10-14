from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('adminlte/', views.admin_stats, name='admin_stats'),
    path('adminlte/home', views.admin_home_page, name='admin_home'),

    path('', views.home_page, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('services/', views.services, name='services'),

]