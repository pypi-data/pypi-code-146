from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class BaseModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    identifier = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)
