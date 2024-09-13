from rest_framework import serializers
from adrf.serializers import Serializer, ModelSerializer
from app.models import *

class DrugListSerializer(ModelSerializer):
    class Meta:
        model = Drug
        fields = ('title', 'title_en', 'term', 'atc')

class DrugFilterSerializer(Serializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)