from rest_framework import viewsets, status
from .models import SinhVien, LichSuRaVao, LichSuNapTien, LichSuThanhToan
from .serializers import (SinhVienSerializer, LichSuRaVaoSerializer, 
                         LichSuNapTienSerializer, LichSuThanhToanSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

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
