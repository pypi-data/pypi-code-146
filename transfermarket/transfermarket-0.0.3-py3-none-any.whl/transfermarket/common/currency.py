from enum import Enum


class Currency(Enum):
    EUR = "€"
    GBP = "£"
    USD = "$"
    JPY = "¥"
    KRW = "₩"
    INR = "₹"
    RUB = "₽"

    def __repr__(self):
        return f"Currency.{self.name}"


def string_to_currency(string: str) -> Currency:
    for currency in Currency:
        if string in [currency.value, currency.name]:
            return currency

    raise ValueError(f"Currency {string} not found")
