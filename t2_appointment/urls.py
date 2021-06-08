from django.urls import path
from . import views

app_name = 't2_appointment'

urlpatterns = [
    path('jadwal-dokter', views.read_jadwal, name="read_jadwal"),
]