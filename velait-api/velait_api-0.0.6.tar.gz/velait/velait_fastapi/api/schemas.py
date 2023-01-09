from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


def to_camel_case(value: str):
    words = value.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class ReadBaseSchema(BaseSchema):
    id: UUID
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class WriteBaseSchema(BaseSchema):
    class Config:
        orm_mode = True
        alias_generator = to_camel_case
        allow_population_by_field_name = True


__all__ = [
    'BaseSchema',
    'ReadBaseSchema',
    'WriteBaseSchema',
]
