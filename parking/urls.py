from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BaiDoXeViewSet, KhuVucViewSet

router = DefaultRouter()
router.register(r'baidoxe', BaiDoXeViewSet)
router.register(r'khuvuc', KhuVucViewSet)

urlpatterns = [
    path('', include(router.urls)),
]