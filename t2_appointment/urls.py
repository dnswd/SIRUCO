from django.urls import path
from . import views

app_name = 't2_appointment'

urlpatterns = [
    path('', views.index, name="index"),
    path('jadwal-dokter', views.read_jadwal, name="read_jadwal"),
    path('create-jadwal', views.create_jadwal, name="create_jadwal"),
    path('post-jadwal/<str:faskes>/<str:shift>/<str:tanggal>', views.post_jadwal, name="post_jadwal"),
    path('create-appointment', views.create_appointment, name="create_appointment"),
    path('form-appointment/<str:email>/<str:faskes>/<str:tanggal>/<str:shift>', views.form_appointment, name="form_appointment"),
    path('read-appointment', views.read_appointment, name="read_appointment"),
    path('update-appointment/<str:nik>/<str:email>/<str:shift>/<str:tanggal>/<str:faskes>', views.update_appointment, name="update_appointment"),
    path('delete-appointment/<str:nik>/<str:email>/<str:shift>/<str:tanggal>/<str:faskes>', views.delete_appointment, name="delete_appointment"),
    path('create-ruangan-rs', views.create_ruangan_rs, name="create_ruangan_rs"),
    path('get-next-ruang/<str:kodeRS>', views.get_next_ruang, name="get_next_ruang"),
    path('create-bed-rs', views.create_bed_rs, name="create_bed_rs"),
    path('get-next-bed/<str:kodeRS>/<str:kodeRuangan>', views.get_next_bed, name="get_next_bed"),
    path('get-ruang-rs/<str:kodeRS>', views.get_ruang_rs, name="get_ruang_rs"),
    path('read-ruangan-rs', views.read_ruangan_rs, name="read_ruangan_rs"),
    path('read-bed-rs', views.read_bed_rs, name="read_bed_rs"),
    path('update-ruangan-rs/<str:kodeRS>/<str:kodeRuangan>', views.update_ruangan_rs, name="update_ruangan_rs"),
    path('delete-bed-rs/<str:kodeRS>/<str:kodeRuangan>/<str:kodeBed>', views.delete_bed_rs, name="delete_bed_rs"),
]