from functools import wraps


def only_decorator(func: callable):

    @wraps(func)
    def only_wrapper(objects, only=(), *args, **kwargs):
        return func(objects, *args, **kwargs).only(*only)

    return only_wrapper


def get_related_decorator(func: callable):

    @wraps(func)
    def get_related_wrapper(objects, select_related=(), prefetch_related=(), *args, **kwargs):
        return func(objects, *args, **kwargs).select_related(*select_related).prefetch_related(*prefetch_related)

    return get_related_wrapper


def first_object_decorator(func: callable):

    @wraps(func)
    def first_object_wrapper(objects, first=False, *args, **kwargs):
        service_result = func(objects, *args, **kwargs)

        if first:
            return service_result.first()

        return service_result

    return first_object_wrapper


def ordering_decorator(func: callable):

    @wraps(func)
    def ordering_wrapper(objects, ordering=None, *args, **kwargs):
        service_result = func(objects, *args, **kwargs)

        if ordering is None:
            return service_result

        return service_result.order_by(*ordering)

    return ordering_wrapper


def pagination_decorator(func: callable):

    @wraps(func)
    def pagination_wrapper(objects, limit=None, offset=None, *args, **kwargs):
        service_result = func(objects, *args, **kwargs)

        if offset is not None:
            service_result = service_result[offset:]
        if limit is not None:
            service_result = service_result[:limit]

        return service_result

    return pagination_wrapper


__all__ = [
    'only_decorator',
    'get_related_decorator',
    'first_object_decorator',
    'ordering_decorator',
    'pagination_decorator'
]
