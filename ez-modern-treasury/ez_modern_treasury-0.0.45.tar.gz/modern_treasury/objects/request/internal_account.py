from dataclasses import dataclass
from typing import Optional


@dataclass
class InternalAccountRequest():
    connection_id: str
    name: str
    party_name: str
    currency: str
    entity_id: Optional[str] = None
    idempotency_key: Optional[str] = None

    def __post_init__(self):
        self.idempotency_key  = f"intenal_account_{self.idempotency_key}" if self.idempotency_key else None

    def to_json(self):
        return {
            "connection_id": self.connection_id,
            "name": self.name,
            "party_name": self.party_name,
            "currency": self.currency,
            "entity_id": self.entity_id
        }
