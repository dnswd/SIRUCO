from django.urls import path
from . import views

app_name = 't1_auth'

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('register-admin-sistem', views.register_admin_sistem, name='register_admin_sistem'),
    path('register-user', views.register_user, name='register_user'),
    path('register-admin-satgas', views.register_admin_satgas, name='register_admin_satgas'),
    path('register-dokter', views.register_dokter, name='register_dokter'),
]
