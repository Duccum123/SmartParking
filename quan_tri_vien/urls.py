from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuanTriVienViewSet

router = DefaultRouter()
router.register(r'quantrivien', QuanTriVienViewSet)

urlpatterns = [
    path('', include(router.urls)),
]