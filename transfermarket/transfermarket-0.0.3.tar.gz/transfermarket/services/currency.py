"""
This module provides services to access currency translation information.
"""

import bs4
import requests

from transfermarket.common.currency import Currency
from transfermarket.common.utils import urljoin


class CurrencyService:
    """The CurrencyService class provides methods to retrieve currency exchange rates."""

    BASE_URL = "https://www.x-rates.com"

    def __init__(self, **kwargs):
        pass

    def get_exchange_rate(self, from_currency: Currency, to_currency: Currency) -> float:
        """Returns the exchange rate from one currency to another."""
        params = f"?from={from_currency.name}&to={to_currency.name}&amount=1"

        url = urljoin(self.BASE_URL, "calculator")
        url = urljoin(url, params)

        res = requests.get(url, timeout=10)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.content, "html.parser")

        element = soup.find("span", class_=["ccOutputRslt"])

        if element is None:
            raise ValueError("Could not find output result element")

        value = element.text
        pivot = value.find(" ")
        value = value[:pivot]

        return float(value)

    def convert(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        """Converts an amount from one currency to another."""
        return amount * self.get_exchange_rate(from_currency, to_currency)
