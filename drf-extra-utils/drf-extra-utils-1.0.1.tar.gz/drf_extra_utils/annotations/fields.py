from rest_framework import serializers

from drf_extra_utils.annotations.utils import get_serializer_field_from_annotation


class AnnotationListField(serializers.Field):
    """
    The AnnotationListField is a serializer field that can be used to represent a list of annotated fields.
    """

    def __init__(self, *args, **kwargs):
        self.annotations = kwargs.pop('annotations')
        kwargs['read_only'] = True

        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        ret = {}
        for name, val in value.items():
            serializer = get_serializer_field_from_annotation(self.annotations[name])
            ret[name] = serializer.to_representation(val) if val is not None else None
        return ret
