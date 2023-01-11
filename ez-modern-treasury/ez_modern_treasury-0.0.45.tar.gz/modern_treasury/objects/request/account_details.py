from dataclasses import dataclass
from typing import Optional


@dataclass
class AccountDetailsRequest:
    account_number: str
    account_number_type: str
    idempotency_key: Optional[str] = None

    def __post_init__(self):
        self.idempotency_key = f"account_details_{self.idempotency_key}" if self.idempotency_key else None

    def to_json(self):
        return {
            'account_number': self.account_number,
            'account_number_type': self.account_number_type,
        }
