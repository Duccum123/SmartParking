from rest_framework import viewsets
from .models import QuanTriVien
from .serializers import QuanTriVienSerializer
from rest_framework.permissions import IsAuthenticated

class QuanTriVienViewSet(viewsets.ModelViewSet):
    queryset = QuanTriVien.objects.all()
    serializer_class = QuanTriVienSerializer
