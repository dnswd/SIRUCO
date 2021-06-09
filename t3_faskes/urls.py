from django.urls import path
from . import views

app_name = 't3_faskes'

urlpatterns = [
    path('', views.index, name='index')
]
