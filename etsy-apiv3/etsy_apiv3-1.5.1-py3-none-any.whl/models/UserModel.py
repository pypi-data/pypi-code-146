from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

class Me(BaseModel):
    shop_id: int
    user_id: int
    

class OtherUser(BaseModel):
    user_id: int
    primary_email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    image_url_75x75: Optional[str]


class User(BaseModel):
    user_id: int
    login_name: str
    primary_email: str
    first_name: str
    last_name: str
    create_timestamp: int
    referred_by_user_id: int
    use_new_inventory_endpoints: bool
    is_seller: bool
    bio: str
    gender: str
    birth_month: str
    birth_day: str
    transaction_buy_count: int
    transaction_sold_count: int