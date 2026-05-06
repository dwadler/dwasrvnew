from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
                  path('', views.start_page, name='index'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
