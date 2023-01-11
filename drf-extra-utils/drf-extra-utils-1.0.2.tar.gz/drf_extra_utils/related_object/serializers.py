from collections import OrderedDict

from django.db.models import Prefetch
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

from rest_framework.exceptions import PermissionDenied

from drf_extra_utils.annotations.handler import ModelAnnotationHandler
from drf_extra_utils.fields import PaginatedListSerializer
from drf_extra_utils.related_object.paginator import RelatedObjectPaginator
from drf_extra_utils.serializers import DynamicModelFieldsMixin


class RelatedObjectAnnotations:
    """
    A class to handle with related object annotations.
    """

    def get_related_object_annotations(self, field_name):
        fields = self.related_objects.get(field_name)

        # pass fields to serializer to handle if there are a field type in fields like @min,@default or @all
        Serializer = self.get_related_object_serializer(field_name)
        fields = Serializer(fields=fields).fields.keys()

        annotation_handler = self.get_related_object_annotation_handler(field_name)

        return annotation_handler.get_annotations(*fields)

    def get_related_object_annotation_handler(self, field_name):
        model = self.get_related_object_model(field_name)
        return ModelAnnotationHandler(model=model)


class RelatedObjectMixin(DynamicModelFieldsMixin, RelatedObjectAnnotations):
    """
    Related object is any field that is related with the model, like ForeignKeys and [One/Many]ToMany fields.

    You can "expand" this fields by passing fields[related_object_name]=id,name,test in url query params.

    The related objects should be declared within the serializer's Meta class, as a dictionary, where:

        * The keys must be the name of the reverse relation of this model.
        * The values are the related object options, which are:
            - serializer: The serializer of the related model. (to avoid circular import you can use string reference to
            the serializer like 'myapp.serializer.MySerializer')
            - many (Optional[Boolean]): Whether the related object is a [one/many]-to-many field.
            - filter (Optional[Dict]): A filtering option to related object queryset (Only take if many option is True).
            - permissions (Optional[Dict]): Permission list to check if user is able to access the related object.

    example:

        class TestSerializer(serializers.ModelSerializer):
            class Meta:
                model = Test
                fields = ('id', 'test')
                related_objects = {
                    'model': {
                        'serializer': ModelSerializer,
                        'many': True,
                        'filter': {'is_published': True, 'name__startswith': 'test'},
                        'permissions': [IsAuthenticated]
                    }
                }
    """

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = cls(fields=kwargs.pop('fields', None))
        return PaginatedListSerializer(*args, **kwargs)

    @cached_property
    def related_objects(self):
        related_objects = {}
        model_related_objects = self.get_related_objects()
        for field_name, fields in self.context.get('related_objects', {}).items():
            if field_name in model_related_objects:
                related_objects[field_name] = fields
        return related_objects

    def get_related_objects(self):
        return getattr(self.Meta, 'related_objects', {})

    def _get_related_object_option(self, related_object, option_name, default=None):
        options = self.get_related_objects().get(related_object)
        return options.get(option_name, default)

    def get_related_object_serializer(self, related_object):
        serializer = self._get_related_object_option(related_object, 'serializer')
        if isinstance(serializer, str):
            serializer = import_string(serializer)
        return serializer

    def get_related_object_model(self, field_name):
        serializer = self.get_related_object_serializer(field_name)
        return serializer.Meta.model

    def related_object_is_many(self, field_name):
        return self._get_related_object_option(field_name, 'many', False)

    def check_related_object_permission(self, obj, related_object_name):
        permissions = self._get_related_object_option(related_object_name, 'permissions', [])

        request = self.context.get('request')
        view = self.context.get('view')
        for permission in [permission() for permission in permissions]:
            if not permission.has_object_permission(request, view, obj):
                raise PermissionDenied(
                    detail=f'You do not have permission to access the related object `{related_object_name}`.'
                )

    def optimize_related_object(self, queryset, field_name):
        annotations = self.get_related_object_annotations(field_name)
        if annotations:
            queryset = queryset.prefetch_related(
                Prefetch(field_name, self.get_related_object_model(field_name).objects.annotate(**annotations))
            )
        else:
            if self.related_object_is_many(field_name):
                queryset = queryset.prefetch_related(field_name)
            else:
                queryset = queryset.select_related(field_name)
        return queryset

    def auto_optimize_related_objects(self, queryset):
        for field_name in self.related_objects.keys():
            queryset = self.optimize_related_object(queryset, field_name)
        return queryset

    def _get_related_objects_fields(self):
        related_objects_fields = OrderedDict()

        for field_name, fields in self.related_objects.items():
            self.check_related_object_permission(self.instance, field_name)

            Serializer = self.get_related_object_serializer(field_name)
            serializer_kwargs = {'fields': fields}

            if self.related_object_is_many(field_name):
                serializer_kwargs.update({
                    'many': True,
                    'filter': self._get_related_object_option(field_name, 'filter'),
                    'paginator': RelatedObjectPaginator(
                        related_object_name=field_name,
                        related_object_fields=fields,
                        request=self.context.get('request')
                    )
                })

            related_objects_fields[field_name] = Serializer(**serializer_kwargs)

        return related_objects_fields

    def get_fields(self):
        fields = super().get_fields()

        fields.update(self._get_related_objects_fields())

        return fields
