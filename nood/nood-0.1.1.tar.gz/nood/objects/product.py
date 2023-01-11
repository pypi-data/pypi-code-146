from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Size(BaseModel):
    value: str
    stock: int
    atc_url: Optional[str] = Field(None, alias='atcUrl')
    direct_url: Optional[str] = Field(None, alias='directUrl')


class Product(BaseModel):
    site_id: int = Field(..., alias='siteId')
    url: str
    name: str
    brand: str
    price: int
    currency: str
    sku: str
    sizes: list[Size]
    thumbnail_url: str = Field(..., alias='thumbnailUrl')
