from dataclasses import field
from re import T
from rest_framework import serializers

from core.models import Tag

class TagSerializer(serializers.ModelSerializer):
    """ Tag model serializer"""
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)