import logging

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from ...models import Category, Tag
from . import serializers

logger = logging.getLogger(__name__)

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filter_backends = [SearchFilter]
    search_fields = ["@name"]


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ["@name"]
