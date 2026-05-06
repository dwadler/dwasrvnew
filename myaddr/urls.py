from django.urls import path

from . import views

app_name = 'myaddr'

urlpatterns = [
    path('', views.start_page, name='index'),
    path('logout', views.logout_request, name='logout'),

    path('movielist', views.MovieList.as_view(), name='movie_list'),
    path('moviecreate', views.MovieCreate.as_view(), name='movie_create'),
    path('<int:pk>/updatemovie/', views.MovieUpdate.as_view(), name='movie_update'),
    path('<int:pk>/deletemovie', views.MovieDelete.as_view(), name='movie_delete'),

    path('list', views.CreateAddressList.as_view(), name='myaddr_list'),
    path('exportall', views.export_all_addresses, name='export_all'),
    path('exportxmas', views.export_xmas, name='export_xmas'),
    path('exportstatus', views.export_status_addresses, name='export_status'),
    path('create', views.AddrCreate.as_view(), name='myaddr_create'),
    path('<int:pk>/', views.AddrDetailView.as_view(), name='myaddr_detail'),
    path('<int:pk>/update/', views.AddrUpdate.as_view(), name='myaddr_update'),
    path('<int:pk>/delete', views.AddrDelete.as_view(), name='myaddr_delete'),
    path('load-addresses/', views.load_addresses, name='ajax_load_addresses'),
]
