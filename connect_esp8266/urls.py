from django.urls import path
from .views import nhan_du_lieu_mq2, nhan_du_lieu_rfid

urlpatterns = [
    path('nhan-du-lieu-mq2/', nhan_du_lieu_mq2, name='nhan_du_lieu_mq2'),
    path('nhan-du-lieu-rfid/', nhan_du_lieu_rfid, name='nhan_du_lieu_rfid'),
]