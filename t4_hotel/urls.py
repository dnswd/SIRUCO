from django.urls import path
from . import views

app_name = 't4_hotel'

urlpatterns = [
    path('', views.index, name='hotel_index'),
    path('ruangan/', views.ruangan_hotel, name='ruangan_hotel'),
    path('rsvp/', views.reservasi_hotel, name='reservasi_hotel'),
    path('transaction/', views.transaksi_hotel, name='transaksi_hotel'),
    path('transaction/booking/', views.transaksi_booking_hotel,
         name='transaksi_booking_hotel'),
]
