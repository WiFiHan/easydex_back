from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DexSerializer

from .models import Dex

# Create your views here.
class DexUserView(APIView):
    def get(self, request):
        dexList = Dex.objects.all()
        dexSerializer = DexSerializer(dexList, many=True)
        return Response(dexSerializer.data, status=status.HTTP_200_OK)
    
