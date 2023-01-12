from pydantic import BaseModel


class ShopSection(BaseModel):
    shop_section_id: int
    title: str
    rank: int
    user_id: int
    active_listing_count: int