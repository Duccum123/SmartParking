from rest_framework import viewsets
from .models import BaiDoXe, KhuVuc
from .serializers import BaiDoXeSerializer, KhuVucSerializer
from rest_framework.permissions import IsAuthenticated

class BaiDoXeViewSet(viewsets.ModelViewSet):
    queryset = BaiDoXe.objects.all()
    serializer_class = BaiDoXeSerializer

class KhuVucViewSet(viewsets.ModelViewSet):
    queryset = KhuVuc.objects.all()
    serializer_class = KhuVucSerializer
