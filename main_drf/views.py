from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import (Kino, Actyor)
from .serializers import (KinoListSerializer,
                          KinoDetailSerializer,
                          ReviewCreateSerializer, CreateReytingSerializer,
                          AktyorListSerializer, AktyorDetaileSerializer)
from .serve import get_client_ip
from django.db import models

# APIView yordamida bazadagi malumotni List ko'rinda chiqarish
class KinoListView(APIView):

    def get(self, request):
        kinolar = Kino.objects.filter(draft=False).annotate(
            reting_user=models.Count("retings", filter=models.Q(retings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F("retings__star")) / models.Count(models.F('retings'))
        )
        serializer = KinoListSerializer(kinolar, many=True)
        return Response(serializer.data)

# APIView yordamida bazadagi malumotni har birini Tafsilotlarini ko'rish
class KinoDetailetView(APIView):

    def get(self, request, pk):
        kino = Kino.objects.get(id=pk, draft=False)
        serializer = KinoDetailSerializer(kino)
        return Response(serializer.data)

# APIView yordamida ko'rishlar soninii mazaga yozish usuli
class ReviewCreateView(APIView):

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarReytingView(APIView):

    def post(self, request):
        serializer = CreateReytingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class AktiyorListView(generics.ListAPIView):
    queryset = Actyor.objects.all()
    serializer_class = AktyorListSerializer


class AktiyorDetailtView(generics.RetrieveAPIView):
    queryset = Actyor.objects.all()
    serializer_class = AktyorDetaileSerializer