from __future__ import annotations
from typing import List
from pydantic import BaseModel
from .PriceModel import Price

class Offering(BaseModel):
    offering_id: int
    quantity: int
    is_enabled: bool
    is_deleted: bool
    price: Price