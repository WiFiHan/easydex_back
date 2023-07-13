from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Index
from .serializers import IndexSerializer
# Create your views here.

class IndexListView(APIView):
    
    def get(self, request):
        indicators = Index.objects.all()
        return Response(indicators.values())
    
    def post(self, request):
        indicator = Index.objects.create(title=request.data['title'], content=request.data['content'])
        return Response(indicator.values())
    
class IndexDetailView(APIView):
    
    def get(self, request, pk):
        indicator = Index.objects.get(pk=pk)
        return Response(indicator.values())
    
    def put(self, request, pk):
        indicator = Index.objects.get(pk=pk)
        indicator.title = request.data['title']
        indicator.content = request.data['content']
        indicator.save()
        return Response(indicator.values())
    
    def delete(self, request, pk):
        indicator = Index.objects.get(pk=pk)
        indicator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)