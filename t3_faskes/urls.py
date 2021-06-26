from django.urls import path
from . import views

app_name = 't3_faskes'

urlpatterns = [
    path('', views.faskes, name='faskes'),
    path('create/', views.faskes_create, name='faskes_create'),
    path('update/<str:pk>/', views.faskes_update, name='faskes_update'),
    path('delete/<str:pk>/', views.faskes_delete, name='faskes_delete'),
    path('detail/<str:pk>/', views.faskes_detail, name='faskes_detail'),
    path('jadwal/', views.jadwal, name='jadwal'),
    path('jadwal/create/', views.jadwal_create, name='jadwal_create'),
    path('rumahsakit/', views.rumahsakit, name='rumahsakit'),
    path('rumahsakit/create/', views.rumahsakit_create, name='rumahsakit_create'),
    path('rumahsakit/update/<str:pk>/', views.rumahsakit_update, name='rumahsakit_update'),
    path('reservasi/', views.reservasi, name='reservasi'),
    path('reservasi/create/', views.reservasi_create, name='reservasi_create'),
    path('reservasi/ruangan-api/<str:koders>/', views.reservasi_ruangan_api, name='reservasi_ruangan_api'),
    path('reservasi/bed-api/<str:koders>/<str:koderuangan>/', views.reservasi_bed_api, name='reservasi_bed_api'),
    path('reservasi/update/<str:pk>/', views.reservasi_update, name='reservasi_update'),
    path('reservasi/delete/<str:pk>/', views.reservasi_delete, name='reservasi_delete'),
    path('transaksi/', views.transaksi, name='transaksi'),
    path('transaksi/update/<str:pk>/', views.transaksi_update, name='transaksi_update'),
    path('transaksi/delete/<str:pk>/', views.transaksi_delete, name='transaksi_delete'),
]
