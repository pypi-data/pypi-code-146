from inspect import isfunction

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from django.db.models import Manager


class PaginatedListSerializer(serializers.ListSerializer):
    """
    The PaginatedListSerializer class is a subclass of Django Rest Framework's ListSerializer class that adds pagination
    functionality to the serializer. It takes in two optional arguments: filter and paginator.

    The filter argument can be used to apply filters to the list of data being serialized. If the filter argument is
    provided, it is applied to the data using either the filter() method (if is a QuerySet) or the built-in filter()
    function.

    The paginator to this class must follow pattern.

    class MyPaginator:
        def paginate_data(data):
            paginate and return the paginated data.

        @property
        def num_pages():
            return paginator num of pages.

        def get_paginated_data(data):
            return paginated data.
    """

    def __init__(self, *args, **kwargs):
        self.filter = kwargs.pop('filter', None)
        self.paginator = kwargs.pop('paginator', None)

        super().__init__(*args, **kwargs)

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, Manager) else data

        if self.filter is not None:
            if hasattr(iterable, 'filter'):
                iterable = iterable.filter(**self.filter)
            elif isfunction(self.filter):
                iterable = list(filter(self.filter, iterable))

        if self.paginator is not None:
            iterable = self.paginator.paginate_data(iterable)

        ret = [self.child.to_representation(item) for item in iterable]

        if self.paginator and self.paginator.num_pages > 1:
            return self.paginator.get_paginated_data(ret)

        return ret


class GenericField(serializers.Field):
    """
    Represents a generic relation / foreign key. It's actually more of a wrapper, that delegates the logic to registered
    serializers based on the `Model` class.
    """
    default_error_messages = {
        'no_model_match': _('Invalid model - model not available.'),
        'no_url_match': _('Invalid hyperlink - No URL match'),
        'incorrect_url_match': _(
            'Invalid hyperlink - view name not available'),
    }

    def __init__(self, serializers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializers = serializers

        for serializer in serializers.values():
            if serializer.source is not None:
                msg = '{}() cannot be re-used. Create a new instance.'
                raise RuntimeError(msg.format(type(serializer).__name__))
            serializer.bind('', self)

    def to_internal_value(self, data):
        serializer, Model = self.get_serializer_for_data(data)
        try:
            ret = serializer.to_internal_value(data)
        except AttributeError:
            raise serializers.ValidationError(self.error_messages['no_model_match'])

        model_object = Model.objects.create(**ret)

        return model_object

    def to_representation(self, instance):
        serializer = self.get_serializer_for_instance(instance)
        return serializer.to_representation(instance)

    def get_serializer_for_instance(self, instance):
        for klass in instance.__class__.mro():
            if klass in self.serializers:
                return self.serializers[klass]
        raise serializers.ValidationError(self.error_messages['no_model_match'])

    def get_serializer_for_data(self, value):
        serializer = model = None
        for Model, model_serializer in self.serializers.items():
            try:
                result = model_serializer.to_internal_value(value)
                if bool(result):
                    serializer = model_serializer
                    model = Model
            except Exception:
                pass
        return serializer, model
