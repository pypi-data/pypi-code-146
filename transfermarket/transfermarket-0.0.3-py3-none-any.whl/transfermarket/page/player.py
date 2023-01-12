"""
This module provides logic for parsing the player page.
"""

import datetime as dt

import bs4

from transfermarket.common.currency import Currency
from transfermarket.common.utils import slugify
from transfermarket.page.object import PageObject
from transfermarket.services.currency import CurrencyService


class PlayerPage(PageObject):
    """
    This class provides logic for parsing the player page.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        slug = kwargs.get("slug")
        if slug is None:
            name = kwargs.get("name")
            if name is not None:
                slug = slugify(name)

        identifier = kwargs.get("identifier")
        self.currency_service = kwargs.get("currency_service", CurrencyService())

        user_agent = "transfermarkt"

        self.headers = {"user-agent": user_agent}

        self.url = f"https://www.transfermarkt.com/{slug}/profil/spieler/{identifier}"

        if kwargs.get("auto_load", False):
            self.load()

    @property
    def name(self) -> str:
        """
        Returns the name of the player.
        """
        return self.soup.find("h1", class_=["data-header__headline-wrapper"]).text.strip()

    @property
    def height(self) -> str:
        """
        Returns the height of the player.
        """
        return self.soup.find("span", {"itemprop": "height"}).text.strip()

    @property
    def citizenship(self) -> str:
        """
        Returns the citizenship of the player.
        """
        return self.soup.find("span", {"itemprop": "nationality"}).text.strip()

    @property
    def position(self) -> str:
        """
        Returns the position of the player.
        """
        raise NotImplementedError()

    @property
    def caps(self) -> str:
        """
        Returns the number of caps for the player.
        """
        raise NotImplementedError()

    @property
    def goals(self) -> str:
        """
        Returns the number of goals scored by the player.
        """
        raise NotImplementedError()

    @property
    def market_value(self) -> str:
        """
        Returns the market value of the player.
        """
        value = "0.0"

        wrapper = self.soup.find("a", class_=["data-header__market-value-wrapper"])

        waehrung_items = wrapper.find_all("span", class_=["waehrung"])

        if len(waehrung_items) == 2:
            symbol = waehrung_items[0].text.strip()
            unit = waehrung_items[1].text.strip()

            for child in list(wrapper.children):
                if isinstance(child, bs4.element.NavigableString):
                    value = child.strip()
                    if len(value) > 0:
                        value = value.replace('"', "")
                        break

            if unit == "m":
                value = float(value) * 1000000
            elif unit == "k":
                value = float(value) * 1000
            else:
                value = float(value)

            if symbol == "\N{euro sign}":
                value = self.currency_service.convert(value, Currency.EUR, Currency.USD)

            value = round(value, 2)
            value = str(value)
        else:
            raise ValueError("Could not parse market value")

        return value

    @property
    def date_of_birth(self) -> dt.datetime:
        """
        Returns the date of birth of the player.
        """
        value = self.soup.find("span", {"itemprop": "birthDate"}).text.strip()

        lparen = value.index("(")
        if lparen is not None:
            value = value[:lparen].strip()

        return dt.datetime.strptime(value, "%b %d, %Y")

    @property
    def age(self) -> int:
        """
        Returns the age of the player in years.
        """
        return (dt.datetime.now() - self.date_of_birth).days // 365

    @property
    def place_of_birth(self) -> str:
        """
        Returns the place of birth.
        """
        return self.soup.find("span", {"itemprop": "birthPlace"}).text.strip()
