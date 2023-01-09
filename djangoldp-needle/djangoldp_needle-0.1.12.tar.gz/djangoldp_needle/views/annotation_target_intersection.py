from django.core.exceptions import SuspiciousOperation
from djangoldp.serializers import LDPSerializer
from djangoldp.views import LDPViewSet
from rest_framework import serializers
import base64

from ..models import AnnotationTarget, Annotation


class AnnotationTargetIntersectionSerializer(LDPSerializer):
    intersection_total = serializers.SerializerMethodField()
    intersection_total_before = serializers.SerializerMethodField()
    intersection_total_after = serializers.SerializerMethodField()

    @property
    def with_cache(self):
        return False

    class Meta:
        fields = ['urlid', 'intersection_total', 'intersection_total_before', 'intersection_total_after']

    def get_intersection_total(self, obj):
        return obj.annotations.exclude(creator=self.context['request'].user).count()

    def get_intersection_total_before(self, obj):
        return obj.annotations.exclude(creator=self.context['request'].user).filter(creation_date__lte=self.get_annotation_date()).count()

    def get_intersection_total_after(self, obj):
        return obj.annotations.exclude(creator=self.context['request'].user).filter(creation_date__gte=self.get_annotation_date()).count()

    def get_annotation_date(self):
        return self.context['view'].kwargs['date']


class AnnotationTargetIntersectionViewset(LDPViewSet):
    model = AnnotationTarget
    serializer_class = AnnotationTargetIntersectionSerializer

    def get_queryset(self, *args, **kwargs):
        url_encoded = self.kwargs['url'];
        url = base64.b64decode(url_encoded).decode('UTF-8')
        return AnnotationTarget.objects.filter(target=url)
