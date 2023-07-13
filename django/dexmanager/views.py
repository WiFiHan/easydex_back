from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DexSerializer

from .models import SrcDex, UserDex

# Create your views here.
class DexListView(APIView):
    #This is the View FOR USERS to get all Dexes
    def get(self, request):
        srcDexList = SrcDex.objects.all()
        srcDexSerializer = DexSerializer(srcDexList, many=True)
        return Response(srcDexSerializer.data, status=status.HTTP_200_OK)

    def post(self, request):
    #This is the View FOR DEVELOPERS to add new dex
        title = request.data.get("title")
        values = request.data.get("values")

        if not title or not values:
            return Response({"detail": "[title, values] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
	    
        srcDex = SrcDex.objects.create(title=title, values=values)
        serializer = DexSerializer(srcDex)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DexDetailView(APIView):
    def get(self, request, dex_id):
        try:
            srcDex = SrcDex.objects.get(id=dex_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DexSerializer(srcDex)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDexView(APIView):
    def post(self, request, dex_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        ### 1 ###
        try:
            srcDex = SrcDex.objects.get(id=dex_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        ### 2 ###
        userDex_list = srcDex.userdex_set.filter(user=request.user)

        ### 3 ###
        if userDex_list.count() > 0:
            srcDex.userdex_set.get(user=request.user).delete()
        else:
            UserDex.objects.create(user=request.user, srcDex=srcDex)

        serializer = DexSerializer(instance=srcDex)
        return Response(serializer.data, status=status.HTTP_200_OK)
