from typing import Type, Optional, Any
from django.utils.translation import gettext_lazy as _

from velait.velait_django.main.models import BaseModel
from velait.common.pagination import get_page_limits
from velait.common.services.search import SearchOperator, Search, SearchError
from velait.velait_django.main.services.services import filter_objects


class DjangoSearch(Search):
    def __init__(
        self,
        model: Type['BaseModel'],
        search_: Optional[str] = None,
        query: str = None,
        page: Optional[Any] = None,
        ordering: Optional[str] = None,
    ):
        self.model = model
        super(DjangoSearch, self).__init__(search=search_, query=query, page=page, ordering=ordering)

    def search(self):
        try:
            offset, limit = get_page_limits(page=self._page['offset'], page_size=self._page['size'])

            return filter_objects(
                objects=self.model.objects,
                ordering=self._ordering,
                offset=offset,
                limit=limit,
                **self.parse_query_filters(),
            )
        except Exception:
            raise SearchError(
                name="search",
                description=_("Поиск не может быть выполнен"),
            )

    def _validate_query_part(self, query_part: dict):
        super(DjangoSearch, self)._validate_query_part(query_part)
        name, value = query_part.get('fn'), query_part.get('fv')

        column = getattr(self.model, name, None)
        if column is None:
            raise SearchError(
                name="query",
                description=f"{name} {_('не найден как значение')}",
            )

    def parse_query_filters(self):
        if self._query is None:
            return {}

        parsed_operators = (self._parse_operator(
            field_name=query_part.get('fn'),
            operator=query_part.get('op'),
            field_value=query_part.get('fv'),
        ) for query_part in self._query)

        return {field: field_filter for field, field_filter in parsed_operators}

    def _parse_operator(self, field_name: str, operator: str, field_value: str):
        """
        Creates an expression object if all input operators are valid.
        If they are not, raises op an exception
        """

        if operator == SearchOperator.LESS.value:
            return [f"{field_name}__lt", field_value]
        elif operator == SearchOperator.EQUAL.value:
            return [field_name, field_value]
        elif operator == SearchOperator.GREATER.value:
            return [f"{field_name}__gt", field_value]
        elif operator == SearchOperator.CONTAINS.value:
            return [f"{field_name}__in", field_value]
        elif operator == SearchOperator.LESS_OR_EQUAL.value:
            return [f"{field_name}__lte", field_value]
        elif operator == SearchOperator.GREATER_OR_EQUAL.value:
            return [f"{field_name}__gte", field_value]
        else:
            raise SearchError(name="query", description=_("Операция не найдена"))


def search(search_, query, page, ordering, model: Type['BaseModel']):
    search_obj = DjangoSearch(
        model=model,
        search_=search_,
        query=query,
        page=page,
        ordering=ordering,
    )
    return search_obj.search()


__all__ = [
    'search',
    'SearchOperator',
    'SearchError',
    'DjangoSearch',
]
