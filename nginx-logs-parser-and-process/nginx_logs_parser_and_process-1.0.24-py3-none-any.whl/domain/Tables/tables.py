from pydantic import BaseModel


class Tables(BaseModel):
    temporal: str
    final: str
    clean_log: str
