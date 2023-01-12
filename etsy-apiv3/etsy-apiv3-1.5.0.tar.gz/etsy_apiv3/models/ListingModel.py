from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel

from .ListingImageModel import ListingImage 
from .ProductionPartnerModel import ProductionPartner
from .ShippingProfileModel import ShippingProfile
from .ShopModel import Shop
from .TranslationModel import Translation
from .UserModel import User
from .PriceModel import Price
from .ProductModel import Product


class Video(BaseModel):
    video_id: int
    height: int
    width: int
    thumbnail_url: str
    video_url: str
    video_state: str
    

class VariationImage(BaseModel):
    property_id: int
    value_id: int
    value: Optional[str] = None
    image_id: int

class Inventory(BaseModel):
    products: List[Product]
    price_on_property: List[int]
    quantity_on_property: List[int]
    sku_on_property: List[int]
    listing: Optional[Listing]


class DraftListing(BaseModel):
    quantity: int
    title: str
    description: str
    price: float
    who_made: str = "i_did"
    when_made: str = "made_to_order"
    taxonomy_id: int
    shipping_profile_id: Optional[int]
    return_policy_id: Optional[int]
    materials: Optional[List[str]]
    shop_section_id: Optional[int]
    processing_min: Optional[int]
    processing_max: Optional[int]
    tags: Optional[List[str]]
    styles: Optional[List[str]]
    item_weight: Optional[float]
    item_length: Optional[float]
    item_width: Optional[float]
    item_height: Optional[float]
    item_weight_unit: Optional[str]
    item_dimensions_unit: Optional[str]
    is_personalizable: bool
    personalization_is_required: Optional[bool]
    personalization_char_count_max: Optional[int]
    personalization_instructions: Optional[int]
    production_partner_ids: List[int]
    image_ids: List[int]
    is_supply: bool
    is_customizable: bool
    should_auto_renew: bool
    is_taxable: bool
    type: str = "physical"
    
class Listing(BaseModel):
    listing_id: int
    user_id: int
    shop_id: int
    title: str
    description: str
    state: str
    creation_timestamp: int
    ending_timestamp: int
    original_creation_timestamp: int
    last_modified_timestamp: int
    state_timestamp: int
    quantity: int
    shop_section_id: Optional[int]
    featured_rank: int
    url: str
    num_favorers: int
    non_taxable: bool
    is_customizable: bool
    is_personalizable: bool
    personalization_is_required: bool
    personalization_char_count_max: Optional[int]
    personalization_instructions: Optional[str]
    listing_type: str
    tags: List[str]
    materials: List[str]
    shipping_profile_id: Optional[int]
    processing_min: Optional[int]
    processing_max: Optional[int]
    who_made: Optional[str]
    when_made: Optional[str]
    is_supply: bool
    item_weight: Optional[int]
    item_weight_unit: Optional[str]
    item_length: Optional[int]
    item_width: Optional[int]
    item_height: Optional[int]
    item_dimensions_unit: Optional[str]
    is_private: bool
    style: List[str]
    file_data: str
    has_variations: bool
    should_auto_renew: bool
    language: str
    price: Price
    taxonomy_id: int
    shipping_profile: Optional[ShippingProfile]
    user: Optional[User]
    shop: Optional[Shop]
    images: Optional[List[ListingImage]]
    production_partners: List[ProductionPartner]
    skus: List[str]
    translations: Optional[List[Translation]]
    inventory: Optional[Inventory]
    
Inventory.update_forward_refs()