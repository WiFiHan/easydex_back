from rest_framework.serializers import ModelSerializer
from .models import SrcDex

class DexSerializer(ModelSerializer):
    class Meta:
        model = SrcDex
        fields = "__all__"