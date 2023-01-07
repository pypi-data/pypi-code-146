from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel


class WeatherItem(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Current(BaseModel):
    dt: int
    sunrise: int
    sunset: int
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


class WeatherItem1(BaseModel):
    id: int
    main: str
    description: str
    icon: str


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
    wind_gust: Optional[float] = None
    weather: List[WeatherItem1]


class HistoricDataClass(BaseModel):
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    current: Current
    hourly: List[HourlyItem]
