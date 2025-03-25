from rest_framework import serializers
from .models import BaiDoXe, KhuVuc

class BaiDoXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaiDoXe
        fields = ['ma_bai', 'ten_bai', 'vi_tri', 'suc_chua']

class KhuVucSerializer(serializers.ModelSerializer):
    bai_do_xe = BaiDoXeSerializer(read_only=True)
    bai_do_xe_id = serializers.PrimaryKeyRelatedField(
        queryset=BaiDoXe.objects.all(), source='bai_do_xe', write_only=True
    )
    
    class Meta:
        model = KhuVuc
        fields = ['ma_khu_vuc', 'bai_do_xe', 'bai_do_xe_id', 'ten_khu_vuc', 'suc_chua']