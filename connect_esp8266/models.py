from django.db import models
from users.models import SinhVien

class CamBienMQ2(models.Model):
    ma_cam_bien = models.BigAutoField(primary_key=True)
    gia_tri = models.FloatField()  
    thoi_gian = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Cảm biến MQ2 - {self.ma_cam_bien} - {self.gia_tri}"

class TheTuLog(models.Model):
    ma_log = models.BigAutoField(primary_key=True)
    id_rfid = models.CharField(max_length=255)
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.SET_NULL, null=True, blank=True)
    thoi_gian = models.DateTimeField(auto_now_add=True)
    trang_thai = models.CharField(max_length=50, default="Đã đọc")  

    def __str__(self):
        return f"Thẻ từ {self.id_rfid} - {self.thoi_gian}"