from django.urls import path
from . import views

app_name = 't1_auth'

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
]
