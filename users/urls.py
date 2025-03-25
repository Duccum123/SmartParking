from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SinhVienViewSet, LichSuRaVaoViewSet, 
                   LichSuNapTienViewSet, LichSuThanhToanViewSet)

router = DefaultRouter()
router.register(r'sinhvien', SinhVienViewSet)
router.register(r'lichsuravao', LichSuRaVaoViewSet)
router.register(r'lichsunaptien', LichSuNapTienViewSet)
router.register(r'lichsuthanhtoan', LichSuThanhToanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]