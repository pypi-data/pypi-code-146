from typing import Any, Optional, Type

from fastapi import Query
from assimilator.core.database import BaseRepository
from assimilator.core.database.exceptions import InvalidQueryError

from velait.common.services.search import Search, SearchError, SearchOperator


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
        self.repository = repository
        self.model = model
        super(AlchemyRepositorySearch, self).__init__(
            search=search_obj,
            query=query,
            page=page,
            ordering=ordering,
        )

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
            raise SearchError(
                name="search",
                description="Search could not be conducted",
            )

    def _validate_query_part(self, query_part: dict):
        super(AlchemyRepositorySearch, self)._validate_query_part(query_part)
        name, value = query_part.get('fn'), query_part.get('fv')

        column = getattr(self.model, name, None)
        if column is None:
            raise SearchError(
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
    return search_obj.search()


__all__ = [
    'search',
    'SearchError',
    'SearchOperator',
    'AlchemyRepositorySearch',
]
