import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, String, func


_base, _named = None, None


def create_base_models(Base):
    global _base, _named

    if _base is not None:
        return _base, _named

    class BaseModel(Base):
        __abstract__ = True
        id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True)

        created_at = Column(TIMESTAMP, server_default=func.now())
        updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
        created_by_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
        updated_by_id = Column(UUID(as_uuid=True), default=uuid.uuid4)

        queryable_fields = ("id", "created_at", "updated_at", "created_by_id", "updated_by_id")
        orderable_fields = ("id", "created_at", "updated_at", "created_by_id", "updated_by_id")
        searchable_fields = ("id", "created_at", "updated_at", "created_by_id", "updated_by_id")
        searched_values = ("id", "created_at", "updated_at", "created_by_id", "updated_by_id")

    class NameModel(BaseModel):
        __abstract__ = True
        name_eng = Column(String, unique=True)
        name_kaz = Column(String, unique=True)
        name_rus = Column(String, unique=True)

    _base, _named = BaseModel, NameModel
    return _base, _named


__all__ = [
    'create_base_models',
]
