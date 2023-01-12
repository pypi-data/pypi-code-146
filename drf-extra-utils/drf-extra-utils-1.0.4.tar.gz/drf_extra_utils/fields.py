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
