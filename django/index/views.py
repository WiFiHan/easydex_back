from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Index
from .serializers import IndexSerializer
import subprocess
# Create your views here.

class IndexListView(APIView):
    
    def get(self, request):
        subprocess.run("cd scraper && scrapy crawl indexinfo --nolog -O data.json", shell=True)
    
class IndexDetailView(APIView):
    pass