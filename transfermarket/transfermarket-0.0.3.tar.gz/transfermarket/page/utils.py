"""
This module provides common utilities for parsing pages.
"""

from datetime import date

BASE_URL = "https://www.transfermarkt.com"


def get_href_from_anchor(anchor):
    """
    Returns the href from the anchor.
    """

    if anchor is None:
        return None

    if anchor.name != "a":
        anchor = anchor.find("a")

    if anchor is None:
        return None

    href = anchor.get("href")
    if href is None:
        return None

    href = href.strip()
    if len(href) == 0:
        return None

    return href


def get_text_from_anchor(anchor):
    """
    Returns the text from the anchor.
    """

    if anchor is None:
        return None

    if anchor.name != "a":
        anchor = anchor.find("a")

    if anchor is None:
        return None

    text = anchor.text.strip()
    if len(text) == 0:
        return None

    return text


def current_season() -> int:
    """
    Returns the current season based on the current date.
    """
    return __get_season(date.today())


def __get_season(input_date: date) -> int:
    """
    Returns the current season based on the input date.
    """
    end_season = date(day=30, month=6, year=input_date.year)
    delta = input_date - end_season

    if delta.days > 0:
        return input_date.year

    return input_date.year - 1
