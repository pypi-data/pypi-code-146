from dataclasses import dataclass
from typing import Optional

from modern_treasury.objects.request.line_item import LineItemRequest


@dataclass
class ExpectedPaymentRequest:
    amount_upper_bound: int
    amount_lower_bound: int
    internal_account_id: str
    direction: str
    type: Optional[str] = None
    currency: Optional[str] = None
    date_upper_bound: Optional[str] = None
    date_lower_bound: Optional[str] = None
    description: Optional[str] = None
    statement_descriptor: Optional[str] = None
    metadata: Optional[dict] = None
    counterparty_id: Optional[str] = None
    line_items: Optional[LineItemRequest] = None
    idempotency_key: Optional[str] = None

    def __post_init__(self):
        self.metadata = {} if not self.metadata else {}
        self.line_items = [] if not self.line_items else line_items
        self.idempotency_key = f"expected_payment_{self.idempotency_key}" if self.idempotency_key else None

    def to_json(self):
        return {
            'amount_upper_bound': self.amount_upper_bound,
            'amount_lower_bound': self.amount_upper_bound,
            'direction': self.direction,
            'internal_account_id': self.internal_account_id,
            'type': self.type,
            'currency': self.currency,
            "date_upper_bound": self.date_upper_bound,
            "date_lower_bound": self.date_lower_bound,
            "statement_descriptor": self.statement_descriptor,
            "metadata": self.metadata,
            "counterparty_id": self.counterparty_id,
            "line_items": [line_item.to_json for line_item in self.line_items],
        }
