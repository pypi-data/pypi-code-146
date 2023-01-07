from __future__ import annotations
from pydantic import BaseModel


class GeoDataClass(BaseModel):
    zip: str
    name: str
    lat: float
    lon: float
    country: str
