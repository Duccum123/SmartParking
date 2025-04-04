from rest_framework import viewsets
from .models import SinhVien, LichSuRaVao, LichSuNapTien, LichSuThanhToan
from .serializers import (SinhVienSerializer, LichSuRaVaoSerializer, 
                         LichSuNapTienSerializer, LichSuThanhToanSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny

class SinhVienViewSet(viewsets.ModelViewSet):
    queryset = SinhVien.objects.all()
    serializer_class = SinhVienSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Lấy mật khẩu riêng ra và loại bỏ khỏi dict
        mat_khau = data.pop('mat_khau', None)

        # Tạo user bằng create_user() nếu có mật khẩu
        if mat_khau:
            sinh_vien = SinhVien.objects.create_user(mat_khau=mat_khau, **data)
        else:
            sinh_vien = SinhVien.objects.create(**data)  # Nếu không có mật khẩu

        serializer = self.get_serializer(sinh_vien)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_permissions(self):
        if self.action == "create":  # Nếu là API đăng ký tài khoản
            return [AllowAny()]  # Không yêu cầu đăng nhập
        return [IsAuthenticated()]  # Các API khác cần đăng nhập

class LichSuRaVaoViewSet(viewsets.ModelViewSet):
    queryset = LichSuRaVao.objects.all()
    serializer_class = LichSuRaVaoSerializer
    permission_classes = [IsAuthenticated]

class LichSuNapTienViewSet(viewsets.ModelViewSet):
    queryset = LichSuNapTien.objects.all()
    serializer_class = LichSuNapTienSerializer
    permission_classes = [IsAuthenticated]

class LichSuThanhToanViewSet(viewsets.ModelViewSet):
    queryset = LichSuThanhToan.objects.all()
    serializer_class = LichSuThanhToanSerializer
    permission_classes = [IsAuthenticated]