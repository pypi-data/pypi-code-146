from django.core.exceptions import SuspiciousOperation
from djangoldp.serializers import LDPSerializer
from djangoldp.views import LDPViewSet
from rest_framework import serializers

from ..models import AnnotationTarget, Annotation


class AnnotationIntersectionsSerializer(LDPSerializer):
    annotation = serializers.SerializerMethodField()
    annotations_before = serializers.SerializerMethodField()
    annotations_after = serializers.SerializerMethodField()

    @property
    def with_cache(self):
        return False

    class Meta:
        fields = ['annotation_id', 'annotation', 'annotations_before', 'annotations_after']

    def get_annotations_before(self, obj):
        return Annotation.objects.filter(creation_date__lt=self.get_annotation_date()).exclude(
            id=self.get_annotation_id()).select_related('target').get(id=self.get_annotation_target_id()).order_by("-creation_date")

    def get_annotations_after(self, obj):
        return Annotation.objects.filter(creation_date__gte=self.get_annotation_date()).exclude(
            id=self.get_annotation_id()).select_related('target').get(id=self.get_annotation_target_id()).order_by("creation_date")

    def get_annotation(self, obj):
        annotation_id = self.get_annotation_id()
        try:
            annotation = Annotation.objects.get(id=annotation_id)
            return annotation
        except Annotation.ObjectDoesNotExist:
            raise SuspiciousOperation('Invalid request')

    def get_annotation_date(self, obj):
        annotation = self.get_annotation()
        return annotation.creation_date

    def get_annotation_id(self):
        if 'annotation_id' not in self.context['request'].query_params:
            raise SuspiciousOperation('Invalid request')
        return self.request.query_params['annotation_id']

    def get_annotation_target_id(self, obj):
        annotation = self.get_annotation()
        return annotation.target.id


class AnnotationIntersectionsViewset(LDPViewSet):
    model = AnnotationTarget
    serializer_class = AnnotationIntersectionsSerializer

    def get_queryset(self, *args, **kwargs):
        if 'annotation_id' not in self.request.query_params:
            raise SuspiciousOperation('Invalid request')

        annotation_id = self.request.query_params['annotation_id']

        return Annotation.objects.filter(id=annotation_id)
