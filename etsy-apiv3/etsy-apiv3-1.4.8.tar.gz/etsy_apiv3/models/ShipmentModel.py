from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

class Shipment(BaseModel):
    receipt_shipping_id: Optional[int]
    shipment_notification_timestamp: int
    carrier_name: str
    tracking_code: str