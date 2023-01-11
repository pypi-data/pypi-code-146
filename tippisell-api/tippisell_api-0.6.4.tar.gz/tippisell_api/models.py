import typing
import pydantic
import datetime


class User(pydantic.BaseModel):
    id: int
    telegram_id: typing.Optional[int]
    username: typing.Optional[str]
    balance: float
    joined_timestamp: datetime.datetime
    last_use_timestamp: datetime.datetime


class Product(pydantic.BaseModel):
    id: int
    name: str
    description: str
    type: str
    price: float
    category_id: typing.Optional[int]
    min_buy: int
    max_buy: int
    is_infinitely: bool


class HttpResponse(pydantic.BaseModel):
    status_code: int
    result: dict


class Shop(pydantic.BaseModel):
    id: int
    web_background: str
    web_favicon: str
    web_telegram_bot_link: bool
    bot_username: str
