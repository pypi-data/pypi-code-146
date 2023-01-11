from drf_extra_utils.annotations.handler import ModelAnnotationHandler


class AnnotationViewMixin:
    """
    Mixin to include model annotations in a queryset.
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        Serializer = self.get_serializer_class()
        model = Serializer.Meta.model

        annotation_handler = ModelAnnotationHandler(model=model)
        if annotation_handler.annotations:
            annotations = None

            # optimize annotations
            fields = self.request.query_params.get('fields')
            if fields:
                try:
                    # pass fields to serializer to handle if there are a field type in fields like @min,@default or @all
                    fields = Serializer(fields=fields.split(',')).fields.keys()
                    annotations = annotation_handler.get_annotations(*fields)
                except TypeError:
                    # if the serializer don't inherit DynamicModelFieldsMixin
                    pass

            if annotations is None:
                annotations = annotation_handler.get_annotations('*')

            queryset = queryset.annotate(**annotations)

        return queryset
