from dataclasses import dataclass
from typing import List, Optional

from .account_details import AccountDetailsRequest


@dataclass
class VirtualAccountRequest:
    name:str
    internal_account_id:str
    credit_ledger_account_id: Optional[str] = None
    debit_ledger_account_id: Optional[str] = None
    counterparty_id: Optional[str] = None
    account_details_list: Optional[List[AccountDetailsRequest]] = None
    metadata: Optional[dict] = None
    idempotency_key: Optional[str] = None
    
    def __post_init__(self):
        self.account_details_list = [] if not self.account_details_list else self.account_details_list
        self.metadata = {} if not self.metadata else self.metadata
        self.idempotency_key = f"virtual_account_{self.idempotency_key}" if self.idempotency_key else None

    def to_json(self):
        account_details = [account_details.to_json() for account_details in self.account_details_list]

        return {
            'name': self.name,
            'internal_account_id': self.internal_account_id,
            'credit_ledger_account_id': self.credit_ledger_account_id,
            'debit_ledger_account_id': self.debit_ledger_account_id,
            'counterparty_id': self.counterparty_id,
            'account_details_list': account_details,
            'metadata': self.metadata,
        }
