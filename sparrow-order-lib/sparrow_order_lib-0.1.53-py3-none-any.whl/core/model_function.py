import logging

from django.shortcuts import _get_queryset

logger = logging.getLogger(__name__)


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.
    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    try:
        queryset = _get_queryset(klass)
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
    except Exception as e:
        logger.error(e.__str__())
        return None
