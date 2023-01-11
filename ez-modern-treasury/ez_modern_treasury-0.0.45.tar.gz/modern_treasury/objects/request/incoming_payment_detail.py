from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class IncomingPaymentDetailRequest:
    transfer_type: str
    direction:str
    amount: Decimal
    virtual_account_id: Optional[str] =None
    internal_account_id: Optional[str] = None
    idempotency_key: Optional[str] = None

    def __post_init__(self):
        self.idempotency_key  = f"incoming_payment_detail_{self.idempotency_key}" if self.idempotency_key else None
        self.amount = self.amount * 100

    def to_json(self):
        result = {
            "type": self.transfer_type,
            "direction": self.direction,
            "amount": self.amount,
        }
        if self.internal_account_id:
            result["internal_account_id"] = self.internal_account_id

        if self.virtual_account_id:
            result["virtual_account_id"] = self.virtual_account_id

        return result
