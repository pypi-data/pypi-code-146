from dataclasses import dataclass
from decimal import Decimal


@dataclass
class LineItemRequest:
    amount: Decimal
    metadata: dict
    description: str
    accounting_category_id: str

    def to_json(self):
        return {
            'amount': self.amount,
            'metadata': self.metadata,
            'description': self.description,
            'accounting_category_id': self.accounting_category_id
        }
