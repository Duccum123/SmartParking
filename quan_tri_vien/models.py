from django.db import models

# Create your models here.
class QuanTriVien(models.Model):
    ma_qtv = models.CharField(max_length=50, primary_key=True)
    ho_ten = models.CharField(max_length=255)
    so_dien_thoai = models.IntegerField()
    mat_khau = models.CharField(max_length=255)
    vai_tro = models.CharField(max_length=100)

    def __str__(self):
        return self.ho_ten
