from django.urls import path
from . import views

app_name = 't1_auth'

urlpatterns = [
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('register-admin-sistem', views.register_admin_sistem,
         name='register_admin_sistem'),
    path('register-user', views.register_user, name='register_user'),
    path('register-admin-satgas', views.register_admin_satgas,
         name='register_admin_satgas'),
    path('register-dokter', views.register_dokter, name='register_dokter'),
    path('logout', views.logout, name='logout'),

    path('pasien', views.pasien, name='pasien'),
    path('pasien/create', views.pasien_create, name='pasien_create'),
    path('pasien/update/<str:nik>', views.pasien_update, name="pasien_update"),
    path('pasien/delete/<str:nik>', views.pasien_delete, name="pasien_delete"),
    path('pasien/detail/<str:nik>', views.pasien_detail, name="pasien_detail")
]
