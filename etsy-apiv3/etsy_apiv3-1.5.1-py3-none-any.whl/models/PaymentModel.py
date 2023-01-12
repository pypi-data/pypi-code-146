from typing import Optional, List
from pydantic import BaseModel
from .PriceModel import Price



class PaymentAdjustmentItem(BaseModel):
    payment_adjustment_id: int
    payment_adjustment_item_id: int
    adjustment_type: Optional[str]
    amount: int = 0
    shop_amount: int = 0
    transaction_id: Optional[int]
    bill_payment_id: Optional[int]
    created_timestamp: int
    updated_timestamp: int

class PaymentAdjustment(BaseModel):
    payment_adjustment_id: int
    payment_id: int
    status: str
    is_success: bool
    user_id: int
    reason_code: str
    total_adjustment_amount: Optional[int]
    shop_total_adjustment_amount: Optional[int]
    buyer_total_adjustment_amount: Optional[int]
    total_fee_adjustment_amount: Optional[int]
    create_timestamp: int
    created_timestamp: int
    update_timestamp: int
    updated_timestamp: int
    payment_adjustment_items: List[PaymentAdjustmentItem]


class PaymentAccountLedgerEntry(BaseModel):
    entry_id: int
    ledger_id: int
    sequence_number: int
    amount: int
    currency: str
    description: str
    balance: int
    create_date: int
    created_timestamp: int
    ledger_type: str
    reference_type: str
    reference_id: Optional[str]
    payment_adjustments: List[PaymentAdjustment]

class Payment(BaseModel):
    payment_id: int
    buyer_user_id: int
    shop_id: int
    receipt_id: int
    amount_gross: Price
    amount_fees: Price
    amount_net: Price
    posted_gross: Price
    posted_fees: Price
    posted_net: Price
    adjusted_gross: Optional[Price]
    adjusted_fees: Optional[Price]
    adjusted_net: Optional[Price]
    currency: str
    shop_currency: Optional[str]
    shipping_user_id: Optional[int]
    shipping_address_id: Optional[int]
    billing_address_id: Optional[int]
    status: str
    shipped_timestamp: Optional[int]
    create_timestamp: Optional[int]
    created_timestamp: Optional[int]
    update_timestamp: Optional[int]
    updated_timestamp: Optional[int]
    payment_adjustments: List[PaymentAdjustment]
    
    