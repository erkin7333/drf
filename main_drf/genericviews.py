from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from .models import (Kino, Actyor)
from .serializers import (KinoListSerializer,
                          KinoDetailSerializer,
                          ReviewCreateSerializer, CreateReytingSerializer,
                          AktyorListSerializer, AktyorDetaileSerializer)
from .serve import get_client_ip, KinoFilter
from django.db import models


# GENERIC VIEW YORDAMIDA BAZADAN MALUMOTLARNI LIST KO'RINISHIDA OLISH USULU LISTAPIVIEW DAN FOYDALANIP
class KinoListView(generics.ListAPIView):
    serializer_class = KinoListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = KinoFilter
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        kinolar = Kino.objects.filter(draft=False).annotate(
            reting_user=models.Count("retings", filter=models.Q(retings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F("retings__star")) / models.Count(models.F('retings'))
        )
        return kinolar

# GENERIC VIEW RetrieveAPIView yordamida bazadagi malumotni har birini Tafsilotlarini ko'rish
class KinoDetailetView(generics.RetrieveAPIView):
    queryset = Kino.objects.filter(draft=False)
    serializer_class = KinoDetailSerializer



# GENERIC VIEW CreateAPIView yordamida ko'rishlar soninii bazaga yozish usuli
class ReviewCreateView(generics.CreateAPIView):

    serializer_class = ReviewCreateSerializer


# CreateAPIView Yordamida bazda baholash mezonini kiritish usuli
class AddStarReytingView(generics.CreateAPIView):
    serializer_class = CreateReytingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
