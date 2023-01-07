from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class WeatherItem(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Rain(BaseModel):
    field_1h: float = Field(..., alias='1h')


class Snow(BaseModel):
    field_1h: float = Field(..., alias='1h')


class HourlyItem(BaseModel):
    dt: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    wind_gust: float
    weather: List[WeatherItem]
    pop: float
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None


class WeatherDataClass(BaseModel):
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    hourly: List[HourlyItem]
