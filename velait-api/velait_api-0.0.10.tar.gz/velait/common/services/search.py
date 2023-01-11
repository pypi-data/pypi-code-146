import json
from enum import Enum
from abc import abstractmethod, ABC
from typing import Optional, Any


class SearchError(ValueError):
    def __init__(self, name: str, description: str):
        super(SearchError, self).__init__(description)
        self.description = description
        self.name = name


class SearchOperator(Enum):
    LESS = "less"
    EQUAL = "equal"
    GREATER = "greater"
    CONTAINS = "contains"
    LESS_OR_EQUAL = "lessOrEqual"
    GREATER_OR_EQUAL = "greaterOrEqual"


class Search(ABC):
    DEFAULT_PAGE_SIZE: int = None

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
            raise SearchError(
                name='query',
                description="'query' cannot be parsed as JSON",
            )

        self._search = search
        self._page = {
            'offset': page.get('offset', 0) if page else 0,
            'size': page.get('size', self.DEFAULT_PAGE_SIZE) if page else self.DEFAULT_PAGE_SIZE,
        }
        self._ordering = ordering.split(",") if ordering else None
        self.validate()

    def _validate_query_part(self, query_part: dict):
        name = query_part.get('fn')
        operation = query_part.get('op')

        if (name is None) or (operation is None):
            raise SearchError(
                name='query',
                description="All items in 'query' must have 'fn', 'op', 'fv' keys",
            )

    def validate(self):
        if self._query is not None:
            for query_part in self._query:
                self._validate_query_part(query_part)

        if not isinstance(self._page.get('offset'), int):
            raise SearchError(
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
