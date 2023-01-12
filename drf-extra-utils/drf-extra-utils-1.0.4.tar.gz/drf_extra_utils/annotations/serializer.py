from drf_extra_utils.annotations.handler import ModelAnnotationFieldHandler


class AnnotationSerializerMixin:
    """
    The AnnotationSerializerMixin class is a mixin for serializers that allows adding fields to the serializer based on
    the annotations of a model.
    """

    def get_fields(self):
        fields = super().get_fields()

        annotation_handler = ModelAnnotationFieldHandler(model=self.Meta.model)
        if annotation_handler.annotations:
            fields.update(annotation_handler.get_annotation_serializer_fields())

        return fields
