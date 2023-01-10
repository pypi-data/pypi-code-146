from abc import ABC
from typing import Type, TypeVar, Generic
from ratio.database.models.model import Model


T = TypeVar("T", bound=Model)


class Queryable(ABC, Generic[T]):
    __table: str
    __model: Type[T]
    __primary_key: str

    def __init__(self, model: Type[T]):
        self.__table = model.__class__.__name__.lower()
        self.__model = model

    def get_by_id(self):
        if not self.__primary_key == "id":
            raise NotImplementedError


class UserQueryable(Queryable):
    pass
