from random import randint
from faker import Faker
from datetime import datetime


faker = Faker()


def random_phone_number(country_code: str = "250") -> str:
    return f"{country_code}{randint(100000000, 1000000000)}"


def format_datetime(value: datetime) -> str:
    formatted = value.isoformat()

    if formatted.endswith("+00:00"):
        return formatted[:-6] + "Z"

    return formatted
