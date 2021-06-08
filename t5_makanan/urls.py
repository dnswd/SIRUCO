from t5_makanan.views import *
from django.urls import path

app_name = 't5_makanan'
urlpatterns = [
    path('tr-makan', tr_makan, name='tr_makan'),
    path('tr-makan/create', tr_makan_create, name='tr_makan_create'),
    path('tr-makan/detail/<str:id_t>/<str:id_tm>', tr_makan_detail, name='tr_makan_detail'),
    path('tr-makan/getKode/<str:id_t>', getKode, name='tr_makan_getKode'),
    path('tr-makan/update/<str:id_t>/<str:id_tm>', tr_makan_update, name='tr_makan_update'),
    path('tr-makan/delete/<str:id_t>/<str:id_tm>', tr_makan_delete, name='tr_makan_delete')
]
