from dataclasses import dataclass
from typing import List, Optional

from .account import AccountRequest


@dataclass
class CounterPartyRequest():
    name: str
    metadata: dict
    account_request_list: List[AccountRequest]
    idempotency_key: Optional[str] = None
    
    def __post_init__(self):
        self.idempotency_key = f"counterparty_{self.idempotency_key}" if self.idempotency_key else None

    def to_json(self) -> dict:
        account_list = [account.to_json() for account in self.account_request_list]

        counterparty_json = {
            "name": self.name,
            "accounts": account_list,
            "metadata": self.metadata,
        }
        return counterparty_json
