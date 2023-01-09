from typing import Optional, TypeVar, Generic, List

from pydantic.generics import GenericModel

from velait.velait_fastapi.api.schemas import BaseSchema


class PageInfo(BaseSchema):
    total_records: int
    total_pages: int
    first: str
    last: str
    next: Optional[str]
    previous: Optional[str]


T = TypeVar("T")


class Page(GenericModel, Generic[T]):
    results: List[T]
    pagination: PageInfo


__all__ = ['Page']
