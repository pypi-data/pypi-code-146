from django.utils.functional import cached_property


class RelatedObjectViewMixin:
    """
    Mixin for API View that optimize queryset with related objects and update the serializer context with related
    objects fields get by query_params.

    Example:
          https://example.com/resource/?fields[related_object_name]=@min,image
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = self.get_auto_optimized_queryset(queryset)

        return queryset

    @cached_property
    def related_objects(self):
        nested_fields = {}
        for field_name, fields in self.request.query_params.items():
            if field_name.startswith('fields[') and field_name.endswith(']'):
                field_name = field_name.rpartition('[')[2][:-1]
                nested_fields[field_name] = fields.split(',')
        return nested_fields

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['related_objects'] = self.related_objects
        return context

    def get_auto_optimized_queryset(self, queryset):
        serializer = self.get_serializer_class()(context={'related_objects': self.related_objects})
        queryset = serializer.auto_optimize_related_objects(queryset)
        return queryset
