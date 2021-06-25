from django.urls import path
from . import views

app_name = 't4_hotel'

urlpatterns = [
    path('', views.index, name='hotel_index'),
    path('ruangan/', views.ruangan_hotel, name='ruangan_hotel'),
    path('ruangan/<str:koderoom>/', views.ubah_ruangan_hotel,
         name='ruangan_hotel_update'),
    path('ruangan/<str:koderoom>/delete', views.remove_ruangan_hotel,
         name='ruangan_hotel_delete'),

    path('rsvp/', views.index_reservasi, name='reservasi_index'),
    path('rsvp/create', views.reservasi_hotel, name='reservasi_hotel'),
    path('rsvp/<str:nik>/<str:tglmasuk>/delete', views.remove_reservasi_hotel,
         name='delete_reservasi_hotel'),
    path('rsvp/<str:nik>/<str:tglmasuk>/update', views.edit_reservasi_hotel,
         name='update_reservasi_hotel'),
    path('rsvp/api/<str:hotel>', views.fetch_hotel_room, name='api_fetch_room'),

    path('transaction/', views.transaksi_hotel, name='transaksi_hotel'),
    path('transaction/booking/', views.transaksi_booking_hotel,
         name='transaksi_booking_hotel'),
]
