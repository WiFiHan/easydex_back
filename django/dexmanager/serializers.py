from rest_framework.serializers import ModelSerializer
from .models import Dex

class DexSerializer(ModelSerializer):
    class Meta:
        model = Dex
        fields = "__all__"