import json
from abc import abstractmethod, ABC
from typing import Any, Optional, Type

from fastapi import Query
from assimilator.core.database import BaseRepository
from assimilator.core.database.exceptions import InvalidQueryError

import settings
from velait.velait_fastapi.database.exceptions import InvalidSearchData


class Search(ABC):
    def __init__(
        self,
        search: Optional[str],
        query: str,
        page: Optional[Any],
        ordering: Optional[str],
    ):
        try:
            self._query = json.loads(query)
        except json.JSONDecodeError:
            raise InvalidSearchData(
                name='query',
                description="'query' cannot be parsed as JSON",
            )

        self._search = search
        self._page = {
            'offset': page.get('offset', 0) if page else 0,
            'size': page.get('size', settings.API_PAGE_SIZE) if page else settings.API_PAGE_SIZE,
        }
        self._ordering = ordering.split(",") if ordering else None

    def _validate_query_part(self, query_part: dict):
        name = query_part.get('fn')
        operation = query_part.get('op')

        if (name is None) or (operation is None):
            raise InvalidSearchData(
                name='query',
                description="All items in 'query' must have 'fn', 'op', 'fv' keys",
            )

    def validate(self):
        if self._query is not None:
            for query_part in self._query:
                self._validate_query_part(query_part)

        if not isinstance(self._page.get('offset'), int):
            raise InvalidSearchData(
                name='page',
                description="'offset' key must be a number in 'page' parameter",
            )

    @abstractmethod
    def _parse_operator(self, field_name: str, operator: str, field_value: str):
        raise NotImplementedError("_parse_operator() is not implemented")

    @abstractmethod
    def search(self):
        raise NotImplementedError("search() is not implemented")

    def parse_query_filters(self):
        if self._query is None:
            return []

        return [self._parse_operator(
            field_name=query_part.get('fn'),
            operator=query_part.get('op'),
            field_value=query_part.get('fv'),
        ) for query_part in self._query]


class AlchemyRepositorySearch(Search):
    def __init__(
        self,
        model: Type['BaseModel'],
        repository: BaseRepository,
        search_obj: Optional[str] = None,
        query: str = Query(default=None),
        page: Optional[Any] = None,
        ordering: Optional[str] = None,
    ):
        super(AlchemyRepositorySearch, self).__init__(search=search_obj, query=query, page=page, ordering=ordering)
        self.model = model
        self.repository = repository

    def search(self):
        try:
            filter_spec = self.repository.specifications.filter(*self.parse_query_filters())

            if self._ordering:
                return self.repository.filter(
                    filter_spec,
                    self.repository.specifications.order(*self._ordering),
                    lazy=True,
                )

            return self.repository.filter(filter_spec, lazy=True)
        except Exception:
            raise InvalidSearchData(
                name="search",
                description="Search could not be conducted",
            )

    def _validate_query_part(self, query_part: dict):
        super(AlchemyRepositorySearch, self)._validate_query_part(query_part)
        name, value = query_part.get('fn'), query_part.get('fv')

        column = getattr(self.model, name, None)
        if column is None:
            raise InvalidSearchData(
                name="query",
                description=f"{name} was not found as a value",
            )

    def _parse_operator(self, field_name: str, operator: str, field_value: str):
        """
        Creates an expression object if all input operators are valid.
        If they are not, raises op an exception
        """

        if operator == "equals":
            return getattr(self.model, field_name) == field_value
        elif operator == "lessOrEqual":
            return getattr(self.model, field_name) <= field_value
        elif operator == "greaterOrEqual":
            return getattr(self.model, field_name) >= field_value
        elif operator == "greater":
            return getattr(self.model, field_name) > field_value
        elif operator == "less":
            return getattr(self.model, field_name) < field_value
        elif operator == "contains":
            return getattr(self.model, field_name).in_(field_value)
        else:
            raise InvalidQueryError()


def search(search_field, query, page, ordering, repository: BaseRepository, model: Type['BaseModel']):
    search_obj = AlchemyRepositorySearch(
        model=model,
        repository=repository,
        search_obj=search_field,
        query=query,
        page=page,
        ordering=ordering,
    )

    search_obj.validate()
    return search_obj.search()


__all__ = [
    'search',
]
