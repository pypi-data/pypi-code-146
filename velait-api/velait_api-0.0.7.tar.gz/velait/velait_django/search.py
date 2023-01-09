from enum import Enum
from typing import Iterable, Type

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from velait.velait_django.models import BaseModel


class SearchError(ValueError):
    def __init__(self, message=None):
        super(SearchError, self).__init__(message)
        self.message = message or _("Неизвестная ошибка поиска")


class SearchOperator(Enum):
    LESS = "less"
    EQUAL = "equal"
    GREATER = "greater"
    CONTAINS = "contains"
    LESS_OR_EQUAL = "lessOrEqual"
    GREATER_OR_EQUAL = "greaterOrEqual"


def _get_operation(field: str, operator: str):
    if operator == SearchOperator.LESS.value:
        return f"{field}__lt"
    elif operator == SearchOperator.EQUAL.value:
        return field
    elif operator == SearchOperator.GREATER.value:
        return f"{field}__gt"
    elif operator == SearchOperator.CONTAINS.value:
        return f"{field}__in"
    elif operator == SearchOperator.LESS_OR_EQUAL.value:
        return f"{field}__lte"
    elif operator == SearchOperator.GREATER_OR_EQUAL.value:
        return f"{field}__gte"
    else:
        raise SearchError(_("Операция не найдена"))


def _create_search(objects, searched_fields, search_data: Iterable[dict]):
    search_fields = {}

    for search in search_data:
        try:
            field, value, operator = search['fn'], search['fv'], search['op']
        except KeyError:
            raise SearchError(_("Неправильные данные для поиска"))

        if field not in searched_fields:
            raise SearchError(_("Поле для поиска не найдено"))

        parsed_operation = _get_operation(field=field, operator=operator)
        search_fields[parsed_operation] = value

    try:
        return objects.filter(**search_fields)
    except ValidationError as exc:
        raise SearchError(exc.messages)


def search_objects(model: Type[BaseModel], ordering: str, search_data):
    query = model.objects

    if ordering is not None:
        if ordering not in model.ordering_fields:
            raise SearchError(_("Поле сортировки не найдено"))

        query = query.order_by(*ordering)

    return _create_search(objects=query, searched_fields=model.searched_fields, search_data=search_data)


__all__ = [
    'search_objects',
    'SearchOperator',
    'SearchError',
]
