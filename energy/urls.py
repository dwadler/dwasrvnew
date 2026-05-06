from django.urls import path

from . import views, viewsenergydata

app_name = 'energy'

urlpatterns = [
    path('', views.start_page, name='index'),

    path('energydata', viewsenergydata.FileFieldFormView.as_view(), name='energy_data'),
    path('energydatamonth', viewsenergydata.EnergyDisplayMonth.as_view(), name='energy_data_month'),
    path('chart', viewsenergydata.EnergyDisplay.as_view(), name='chart'),
    path('solarmax', viewsenergydata.SolarMaxMonth.as_view(), name='solar_max_month'),
    path('ev6', views.EV6List.as_view(), name='ev6_list'),
    path('ev6/mpg', views.EV6ListMPG.as_view(), name='ev6mpg_list'),
    path('ev6/create', views.EV6Create.as_view(), name='ev6_create'),
    path('ev6/<int:pk>/update/', views.EV6Update.as_view(), name='ev6_update'),

    path('cenhud', views.ElectricalList.as_view(), name='electrical_list'),
    path('cenhud/create', views.ElectricalCreate.as_view(), name='electrical_create'),
    path('cenhud/<int:pk>/', views.ElectricalDetailView.as_view(), name='electrical_detail'),
    path('cenhud/<int:pk>/update/', views.ElectricalUpdate.as_view(), name='electrical_update'),
    path('cenhud/<int:pk>/delete', views.ElectricalDelete.as_view(), name='electrical_delete'),
]
