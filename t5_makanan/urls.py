from t5_makanan.views import *
from django.urls import path

app_name = 't5_makanan'
urlpatterns = [
    path('tr-makan/create', tr_makan_create, name='tr_makan_create'),
    path('tr-makan/detail/<str:id_t>/<str:id_tm>',
         tr_makan_detail, name='tr_makan_detail'),
    path('tr-makan/getKode/<str:id_t>', getKode, name='tr_makan_getKode'),
    path('tr-makan/update/<str:id_t>/<str:id_tm>',
         tr_makan_update, name='tr_makan_update'),
    path('tr-makan/delete/<str:id_t>/<str:id_tm>',
         tr_makan_delete, name='tr_makan_delete'),

    path('paket-makan/create', pm_create, name="pm_create"),
    path('paket-makan/update/<str:kh>/<str:kp>', pm_update, name="pm_update"),
    path('paket-makan/delete/<str:kh>/<str:kp>', pm_delete, name="pm_delete"),

    path('hotel/create', hotel_create, name="hotel_create"),
    path('hotel/update/<str:kode>', hotel_update, name="hotel_update"),

    path('', makanan_index, name="makanan_index"),
]
