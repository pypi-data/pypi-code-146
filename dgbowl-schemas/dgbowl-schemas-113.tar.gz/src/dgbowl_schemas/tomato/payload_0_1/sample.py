from pydantic import BaseModel, Extra


class Sample(BaseModel, extra=Extra.allow):
    name: str
