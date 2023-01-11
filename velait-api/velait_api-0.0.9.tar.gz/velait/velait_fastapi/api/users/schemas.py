from typing import List
from uuid import UUID

from velait.velait_fastapi.api.schemas import ReadBaseSchema


class UserSchema(ReadBaseSchema):
    id: UUID
    username: str
    email: str
    permissions: List[str]


__all__ = ['UserSchema']
