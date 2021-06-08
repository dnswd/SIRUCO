from t5_makanan.views import *
from django.urls import path

app_name = 't5_makanan'
urlpatterns = [
    path('tr-makan', tr_makan, name='tr_makan'),
    path('tr-makan/create', tr_makan_create, name='tr_makan_create'),
    path('tr-makan/detail/<str:id_t>/<str:id_tm>', tr_makan_detail, name='tr_makan_detail'),
    path('tr-makan/getKodeHotel/<str:id_t>', getKodeHotel, name='tr_makan_getKodeHotel'),
    path('tr-makan/getKodePaket/<str:kode>', getKodePaket, name='tr_makan_getKodePaket'),
    path('tr-makan/saveTransaksiMakan', save_tr_makan, name='tr_makan_saveTransaksiMakan'),
    path('tr-makan/update/<str:id_t>/<str:id_tm>', tr_makan_update, name='tr_makan_update'),
    path('tr-makan/updateTransaksiMakan', update_tr_makan, name='update_tr_makan'),
    path('tr-makan/delete/<str:id_t>/<str:id_tm>', tr_makan_delete, name='tr_makan_delete')
]
