import dataclasses
import time
from typing import Any


@dataclasses.dataclass(frozen=True)
class CryptodotcomRequestMessage:
    method: str
    params: dict[str, Any] = dataclasses.field(default_factory=dict)
    nonce: int = dataclasses.field(default_factory=lambda: int(1e3 * time.time()))
    id: int = 0
