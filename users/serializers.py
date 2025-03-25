from rest_framework import serializers
from .models import SinhVien, LichSuRaVao, LichSuNapTien, LichSuThanhToan

class SinhVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinhVien
        fields = ['ma_sv', 'mat_khau', 'ho_ten', 'id_rfid', 'so_tien_hien_co']

class LichSuRaVaoSerializer(serializers.ModelSerializer):
    sinh_vien = SinhVienSerializer(read_only=True)
    sinh_vien_id = serializers.PrimaryKeyRelatedField(
        queryset=SinhVien.objects.all(), source='sinh_vien', write_only=True
    )
    
    class Meta:
        model = LichSuRaVao
        fields = ['ma_lich_su', 'sinh_vien', 'sinh_vien_id', 'bien_so_xe', 
                 'thoi_gian_vao', 'thoi_gian_ra', 'trang_thai']

class LichSuNapTienSerializer(serializers.ModelSerializer):
    sinh_vien = SinhVienSerializer(read_only=True)
    sinh_vien_id = serializers.PrimaryKeyRelatedField(
        queryset=SinhVien.objects.all(), source='sinh_vien', write_only=True
    )
    
    class Meta:
        model = LichSuNapTien
        fields = ['ma_nap_tien', 'sinh_vien', 'sinh_vien_id', 'so_tien', 
                 'thoi_gian_nap', 'phuong_thuc', 'ma_giao_dich', 'ghi_chu']

class LichSuThanhToanSerializer(serializers.ModelSerializer):
    sinh_vien = SinhVienSerializer(read_only=True)
    sinh_vien_id = serializers.PrimaryKeyRelatedField(
        queryset=SinhVien.objects.all(), source='sinh_vien', write_only=True
    )
    
    class Meta:
        model = LichSuThanhToan
        fields = ['ma_thanh_toan', 'sinh_vien', 'sinh_vien_id', 'so_tien', 'thoi_gian']