from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Size(BaseModel):
    value: str
    stock: Optional[int]
    atc_url: Optional[str] = Field(None, alias='atcUrl')
    direct_url: Optional[str] = Field(None, alias='directUrl')


class Product(BaseModel):
    site_id: Optional[int] = Field(None, alias='siteId')
    url: str
    name: str
    brand: Optional[str]
    price: Optional[int]
    currency: Optional[str]
    sku: Optional[str]
    sizes: Optional[List[Size]] = []
    thumbnail_url: Optional[str] = Field("", alias='thumbnailUrl')
