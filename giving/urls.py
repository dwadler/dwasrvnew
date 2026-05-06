from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'giving'

urlpatterns = [
                  path('', views.start_page, name='index'),
                  path('login', views.login, name='login'),
                  path('logout', views.logout_request, name='logout'),
                  path('test1', views.test1, name='test1'),

                  path('donor', views.DonorList.as_view(), name='donor_list'),
                  path('donor/<int:pk>/update/', views.DonorUpdateView.as_view(), name='donor_update'),
                  path('donor/create/', views.DonorCreateView.as_view(), name='donor_create'),
                  path('donor/<int:pk>/delete/', views.DonorDeleteView.as_view(), name='delete_donor'),

                  path('donation/create', views.DonationCreateView.as_view(), name='donation_create'),
                  path('donation/<int:pk>/update/', views.DonationUpdateView.as_view(), name='donation_update'),
                  path('donation/<int:pk>/delete', views.DonationDeleteView.as_view(), name='donation_delete'),
                  path('donation/export_donations_csv', views.export_donations, name='export_donations'),
                  path('donation/export_donation_summary_csv', views.export_donation_summary,
                       name='export_donation_summary'),
                  path('donation/export_donation_summary_yr_csv', views.export_donation_summary_yr,
                       name='export_donation_summary_yr'),
                  path('donation', views.CreateDonationList.as_view(), name='donate_list'),
                  path('donationbatch', views.DonationBatch.as_view(), name='donation_batch'),
                  path('donationbatchsave', views.donation_batch_save, name='donation_batch_save'),
                  path('donationbatchlist', views.DonationBatchList.as_view(), name='donation_batch_list'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
