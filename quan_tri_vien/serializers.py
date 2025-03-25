from rest_framework import serializers
from .models import QuanTriVien

class QuanTriVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuanTriVien
        fields = ['ma_qtv', 'ho_ten', 'so_dien_thoai', 'mat_khau', 'vai_tro']