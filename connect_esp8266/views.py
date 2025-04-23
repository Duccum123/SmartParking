from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import CamBienMQ2, TheTuLog
from .serializers import CamBienMQ2Serializer, TheTuLogSerializer
from users.models import SinhVien
from django.utils import timezone
from users.models import LichSuRaVao
from modelAI.empty_space.emptySpace import scanEmptySpace
import json
import requests

@api_view(['POST'])
def nhan_du_lieu_mq2(request):
    # Lấy dữ liệu cảm biến gas từ ESP8266
    gia_tri_mq2 = request.data.get('gia_tri_mq2')

    # Kiểm tra dữ liệu đầu vào
    if gia_tri_mq2 is None:
        return Response(
            {"error": "Vui lòng cung cấp giá trị cảm biến MQ2"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Lưu giá trị cảm biến MQ2
    try:
        cam_bien = CamBienMQ2(gia_tri=float(gia_tri_mq2))
        cam_bien.save()
    except ValueError:
        return Response(
            {"error": "Giá trị cảm biến phải là số hợp lệ"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Serialize và trả về kết quả
    serializer = CamBienMQ2Serializer(cam_bien)
    return Response({
        "message": "Dữ liệu cảm biến gas đã được lưu",
        "cam_bien_mq2": serializer.data
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def nhan_du_lieu_rfid(request):
    # Lấy dữ liệu thẻ từ từ ESP8266
    id_rfid = request.data.get('id_rfid')

    # Kiểm tra dữ liệu đầu vào
    if not id_rfid:
        return Response(
            {"error": "Vui lòng cung cấp id_rfid"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Tìm sinh viên dựa trên id_rfid
    try:
        sinh_vien = SinhVien.objects.get(id_rfid=id_rfid)
    except SinhVien.DoesNotExist:
        return Response(
            {"message": "Không tìm thấy sinh viên"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Lưu log thẻ từ
    the_tu_log = TheTuLog.objects.create(
        id_rfid=id_rfid,
        sinh_vien=sinh_vien,
        trang_thai="Đã đọc"
    )

    action = "null"
    if sinh_vien:
        # đi vào
        if sinh_vien.trang_thai != "Đang đỗ":
            lich_su_ra_vao = LichSuRaVao.objects.create(
                sinh_vien=sinh_vien,
                bien_so_xe="Chưa xác định",
                thoi_gian_vao=timezone.now(),
                thoi_gian_ra=None,
                trang_thai="Đang đỗ"
            )
            sinh_vien.trang_thai = "Đang đỗ"
            action = "vao"
        # đi ra
        else:
            lich_su_ra_vao = LichSuRaVao.objects.filter(
                sinh_vien=sinh_vien, 
                trang_thai="Đang đỗ"
            ).order_by('-thoi_gian_vao').first()

            if not lich_su_ra_vao:
                return Response(
                    {"error": "Không tìm thấy bản ghi đang đỗ"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            lich_su_ra_vao.trang_thai = "Đã ra"
            sinh_vien.trang_thai = "Đã ra"
            lich_su_ra_vao.thoi_gian_ra = timezone.now()
            action = "ra"

            # Lưu thay đổi
            lich_su_ra_vao.save()
        
        sinh_vien.save()

    # Quét bãi đỗ xe tìm chỗ trống
    emptySpace = None
    try:
        emptySpace = scanEmptySpace()
    except Exception as e:
        print(f"Lỗi khi quét dữ liệu chỗ trống: {e}")
        emptySpace = -1  # Gán giá trị báo lỗi

    # Serialize và trả về kết quả
    serializer = TheTuLogSerializer(the_tu_log)
    return Response({
        "message": "Dữ liệu thẻ từ đã được xử lý",
        "emptySpace": emptySpace,
        "action": action
    }, status=status.HTTP_201_CREATED)