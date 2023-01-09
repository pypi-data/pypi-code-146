from pydantic import BaseModel


class UserCompact(BaseModel):
    id: int
    full_name: str
    email: str
