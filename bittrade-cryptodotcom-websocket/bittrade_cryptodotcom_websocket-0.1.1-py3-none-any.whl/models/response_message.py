import dataclasses
from typing import Any


@dataclasses.dataclass
class CryptodotcomResponseMessage:
    id: int
    method: str
    code: int
    result: dict[str, Any] = dataclasses.field(default_factory=dict)
    message: str = ""
    original: str = ""