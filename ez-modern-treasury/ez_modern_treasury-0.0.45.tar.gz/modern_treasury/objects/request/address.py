from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class AddressRequest:
    line1: Optional[str]
    line2: Optional[str]
    locality: Optional[str]
    region: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]

    def to_json(self) -> dict:
        return asdict(self)