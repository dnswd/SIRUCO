from django.urls import path
from . import views

app_name = 't2_appointment'

urlpatterns = [
    path('jadwal', views.get_jadwal, name="get_jadwal"),
]