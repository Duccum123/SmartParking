from django.db import models
from django.contrib.auth.models import AbstractUser

class SinhVien(models.Model):
    ma_sv = models.IntegerField(unique=True, primary_key=True)
    mat_khau = models.CharField(max_length=255 ,default="cntt123")
    ho_ten = models.CharField(max_length=255)
    id_rfid = models.CharField(max_length=255, unique=True)
    so_tien_hien_co = models.FloatField(default=0)
    trang_thai = models.CharField(max_length=50, default="Chưa đỗ")

    def __str__(self):
        return self.ho_ten


class LichSuRaVao(models.Model):
    ma_lich_su = models.BigAutoField(primary_key=True)
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    bien_so_xe = models.CharField(max_length=50)
    thoi_gian_vao = models.DateTimeField()
    thoi_gian_ra = models.DateTimeField(null=True, blank=True)
    trang_thai = models.CharField(max_length=50)

    def __str__(self):
        return f"Lịch sử ra vào {self.ma_lich_su}"


class LichSuNapTien(models.Model):
    ma_nap_tien = models.BigAutoField(primary_key=True)
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    so_tien = models.FloatField()
    thoi_gian_nap = models.DateTimeField(auto_now_add=True)
    phuong_thuc = models.CharField(max_length=255)
    ma_giao_dich = models.CharField(max_length=255, unique=True)
    ghi_chu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Nạp tiền {self.so_tien} - {self.sinh_vien.ma_sv}"


class LichSuThanhToan(models.Model):
    ma_thanh_toan = models.BigAutoField(primary_key=True)
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    so_tien = models.FloatField()
    thoi_gian = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thanh toán {self.so_tien} - {self.sinh_vien.ma_sv}"
