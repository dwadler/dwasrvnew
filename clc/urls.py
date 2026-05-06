from django.urls import path

from . import views

app_name = 'clc'

urlpatterns = [
    path('', views.start_page, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout_request, name='logout'),

    path('address/create_directory', views.create_directory, name='create_directory'),
    path('address/export_members_csv', views.export_members_csv, name='export_members'),
    path('address/export_envelope_list', views.export_envelope_list, name='export_envelope_list'),
    path('address/export_advent_list', views.export_advent_list, name='export_advent_list'),
    path('address', views.ListByType.as_view(), name='address_list'),
    path('address/create', views.AddressCreate.as_view(), name='address_create'),

    path('address/<int:pk>/update/', views.AddressUpdate.as_view(), name='address_update'),
    path('address/<int:pk>/delete', views.AddressDelete.as_view(), name='address_delete'),
    path('address/<int:pk>/create', views.AddressCreate.as_view(), name='address_create'),
]
