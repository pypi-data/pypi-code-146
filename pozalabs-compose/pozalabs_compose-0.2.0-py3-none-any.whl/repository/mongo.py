from __future__ import annotations

from typing import Any, ClassVar, Generic, Optional, TypeVar, get_args

import pymongo
from pymongo import UpdateOne
from pymongo.collection import Collection
from pymongo.database import Database

from .. import types
from ..entity import Entity
from ..pagination import Pagination
from ..query.mongo import MongoFilterQuery
from . import base

EntityType = TypeVar("EntityType", bound=Entity)


class MongoRepository(base.BaseRepository, Generic[EntityType]):
    __collection_name__: ClassVar[str] = ""
    __indexes__: ClassVar[Optional[list[pymongo.IndexModel]]] = None

    def __init__(self, collection: Collection):
        self.collection = collection

    @classmethod
    def create(cls, database: Database, **kwargs) -> MongoRepository:
        collection = database.get_collection(cls.__collection_name__, **kwargs)
        if cls.__indexes__ is not None:
            collection.create_indexes(cls.__indexes__)
        return cls(collection)

    def find_by_id(self, entity_id: types.PyObjectId, **kwargs) -> Optional[EntityType]:
        return self.find_by({"_id": entity_id}, **kwargs)

    def find_by(self, filter_: dict[str, Any], **kwargs) -> Optional[EntityType]:
        """https://stackoverflow.com/a/73746554/9331155"""
        entity_type: EntityType = get_args(self.__class__.__orig_bases__[0])[0]
        result = self.collection.find_one(filter=filter_, **kwargs)
        return result and entity_type.parse_obj(result)

    def add(self, entity: EntityType, **kwargs) -> None:
        self.collection.insert_one(entity.dict(by_alias=True), **kwargs)

    def add_many(self, entities: list[EntityType], **kwargs) -> None:
        self.collection.insert_many([entity.dict(by_alias=True) for entity in entities], **kwargs)

    def update(self, entity: EntityType, **kwargs) -> None:
        self.collection.update_one(
            {"_id": entity.id},
            {"$set": entity.dict(by_alias=True)},
            **kwargs,
        )

    def update_many(self, entities: list[EntityType], **kwargs) -> None:
        self.collection.bulk_write(
            requests=[
                UpdateOne({"_id": entity.id}, {"$set": entity.dict(by_alias=True)})
                for entity in entities
            ],
            **kwargs,
        )

    def delete(self, entity_id: types.PyObjectId, **kwargs) -> None:
        self.collection.delete_one({"_id": entity_id}, **kwargs)

    def execute_raw(self, operation: str, **operation_kwargs) -> Any:
        op = getattr(self.collection, operation, None)
        if op is None:
            raise ValueError(f"Unknown operation on collection: {operation}")
        return op(**operation_kwargs)

    def filter(self, qry: MongoFilterQuery) -> Pagination:
        result = self.collection.aggregate(qry.to_query())
        result = next(result, None)
        return Pagination(
            total=(result["metadata"][0]["total"] if result["metadata"] else 0),
            items=result["items"],
            page=qry.page,
            per_page=qry.per_page,
        )
