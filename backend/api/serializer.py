from rest_framework import serializers
from .models import Game, Tag

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    name = serializers.CharField(required=True)
    platform = serializers.CharField(required=True)
    link = serializers.CharField(required=True)
    min_party_size = serializers.IntegerField(required=True)
    max_party_size = serializers.IntegerField(required=True)
    tags = serializers.JSONField(required=True)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    tag = serializers.CharField(required=True)
