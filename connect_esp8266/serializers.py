from rest_framework import serializers
from .models import CamBienMQ2, TheTuLog
from users.serializers import SinhVienSerializer

class CamBienMQ2Serializer(serializers.ModelSerializer):
    class Meta:
        model = CamBienMQ2
        fields = ['ma_cam_bien', 'gia_tri', 'thoi_gian']

class TheTuLogSerializer(serializers.ModelSerializer):
    sinh_vien = SinhVienSerializer(read_only=True)

    class Meta:
        model = TheTuLog
        fields = ['ma_log', 'id_rfid', 'sinh_vien', 'thoi_gian', 'trang_thai']