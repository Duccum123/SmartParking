from rest_framework import viewsets, status
from .models import SinhVien, LichSuRaVao, LichSuNapTien, LichSuThanhToan
from .serializers import (SinhVienSerializer, LichSuRaVaoSerializer, 
                         LichSuNapTienSerializer, LichSuThanhToanSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

class SinhVienViewSet(viewsets.ModelViewSet):
    queryset = SinhVien.objects.all()
    serializer_class = SinhVienSerializer

class LichSuRaVaoViewSet(viewsets.ModelViewSet):
    queryset = LichSuRaVao.objects.all()
    serializer_class = LichSuRaVaoSerializer

class LichSuNapTienViewSet(viewsets.ModelViewSet):
    queryset = LichSuNapTien.objects.all()
    serializer_class = LichSuNapTienSerializer

class LichSuThanhToanViewSet(viewsets.ModelViewSet):
    queryset = LichSuThanhToan.objects.all()
    serializer_class = LichSuThanhToanSerializer
class NapTienAPIView(APIView):
    def post(self, request):
        serializer = LichSuNapTienSerializer(data=request.data)
        if serializer.is_valid():
            sinh_vien = serializer.validated_data['sinh_vien']
            so_tien = serializer.validated_data['so_tien']
            
            # Cập nhật số dư
            sinh_vien.so_tien_hien_co += so_tien
            sinh_vien.save()

            # Lưu lịch sử nạp tiền
            serializer.save()

            return Response({
                "message": "Nạp tiền thành công.",
                "so_du_moi": sinh_vien.so_tien_hien_co
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)