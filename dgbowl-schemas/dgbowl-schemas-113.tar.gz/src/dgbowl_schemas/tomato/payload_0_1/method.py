from pydantic import BaseModel, Extra


class Method(BaseModel, extra=Extra.allow):
    device: str
    technique: str
