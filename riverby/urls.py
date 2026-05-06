from django.urls import path

from . import views

app_name = 'riverby'

urlpatterns = [
    path('', views.start_page, name='index'),

    path('address', views.AddrList.as_view(), name='address_list'),
    path('address/rhha', views.RhhaList.as_view(), name='rhha_list'),
    path('address/create', views.AddrCreate.as_view(), name='address_create'),
    path('address/<int:pk>/newowner/', views.AddrNewOwner.as_view(), name='address_new_owner'),
    path('address/<int:pk>/', views.AddrDetailView.as_view(), name='address_detail'),
    path('address/<int:pk>/update/', views.AddrUpdate.as_view(), name='address_update'),
    path('address/<int:pk>/delete', views.AddrDelete.as_view(), name='address_delete'),
    path('address/export_rhha', views.export_rhha_addresses, name='export_rhha'),
]
