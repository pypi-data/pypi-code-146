# -*- coding: utf-8 -*-
"""
=======================
restricted_python_tools
=======================

This module implements basic Python functionality missing in restricted Python.
"""
from bs4 import BeautifulSoup


def contains_all(
    container: list,
    contained: list
) -> bool:
    """ Check if a list is contained in another list

    .. note:: 'all' is not available in restricted Python

    :param contained: the list to check if its contained
    :param container: the list to check it it containes the other one
    """

    return all(el in container for el in contained)


def contains_any(
    container: list,
    contained: list
) -> bool:
    """ Check if at least one element of a list is contained in another list

    .. note:: 'any' is not available in restricted Python

    :param contained: the list to check if its contained
    :param container: the list to check it it containes the other one
    """

    return any(el in container for el in contained)


def prettify_html(
    html: str
) -> str:
    """
    Prettify html (from bs4/BeautifulSoup)

    .. note:: This function is needed for Zope Python Scripts
        because even if bs4 can be imported, prettify throws
        an Unauthorized error in restricted Python
    """

    return BeautifulSoup(html, "html.parser").prettify()


def remove_duplicates(lst: list) -> list:
    """ Removes duplicates from a list

    .. note:: restricted Python does not allow sets
    """

    return list(set(lst))
