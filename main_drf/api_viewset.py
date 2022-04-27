from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serve import get_client_ip, KinoFilter
from django.db import models

from .models import Actyor, Kino

from .serializers import (AktyorListSerializer, AktyorDetaileSerializer,
                          KinoListSerializer, KinoDetailSerializer,
                          ReviewCreateSerializer, CreateReytingSerializer)


# VIEWSET YORDAMIDA GET ZAPROSI BN BAZADAN MALUMOTLARNI LIST KO'RINNISHIDA CHIQARISH VA
# BITTA MALUMOTNI TAVSILOTINI KO'RISH USULI

class AktyroViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Actyor.objects.all()
        serializer = AktyorListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Actyor.objects.all()
        actor = get_object_or_404(queryset, pk=pk)
        serializer = AktyorDetaileSerializer(actor)
        return Response(serializer.data)


class KinoViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, )
    filterset_class = KinoFilter

    def get_queryset(self):
        kinolar = Kino.objects.filter(draft=False).annotate(
            reting_user=models.Count("retings", filter=models.Q(retings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F("retings__star")) / models.Count(models.F('retings'))
        )
        return kinolar
# GET Zapros
    def get_serializer_class(self):
        if self.action == 'list':
            return KinoListSerializer
        elif self.action == "retrieve":
            return KinoDetailSerializer

# POST Zapros
class ReviewCreateViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewCreateSerializer



# POST Zapros
class AddStarReytingViewSet(viewsets.ModelViewSet):

    serializer_class = CreateReytingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

# GET Zapros
class AktyorViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Actyor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AktyorListSerializer
        elif self.action == 'retrieve':
            return AktyorDetaileSerializer