from django.db import models

# Create your models here.

class BaiDoXe(models.Model):
    ma_bai = models.CharField(max_length=50, primary_key=True)
    ten_bai = models.CharField(max_length=255)
    vi_tri = models.CharField(max_length=255)
    suc_chua = models.IntegerField()

    def __str__(self):
        return self.ten_bai


class KhuVuc(models.Model):
    ma_khu_vuc = models.CharField(max_length=50, primary_key=True)
    bai_do_xe = models.ForeignKey(BaiDoXe, on_delete=models.CASCADE)
    ten_khu_vuc = models.CharField(max_length=255)
    suc_chua = models.IntegerField()

    def __str__(self):
        return self.ten_khu_vuc
