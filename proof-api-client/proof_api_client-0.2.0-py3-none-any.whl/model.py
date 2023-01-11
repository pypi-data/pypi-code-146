import typing

import pydantic


class GpsData(pydantic.BaseModel):
    lat: float
    lng: float
    alt: float
    speed: float
    heading: float
    acc: float
    # name: str


class Device(pydantic.BaseModel):
    id: str  # Device IMEI
    imsi: str
    name: str
    fw_version: str
    model: str
    states: typing.List[str] = list()
    gps: GpsData | None


class TokenInfo(pydantic.BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
