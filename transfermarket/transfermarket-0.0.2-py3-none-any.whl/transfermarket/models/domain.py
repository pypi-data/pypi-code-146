"""
This module contains domain models for domain.
"""

from dataclasses import dataclass


@dataclass
class Domain:
    """
    This class contains the domain model for a domain.
    """

    name: str
    url: str

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")

    def __repr__(self):
        return f"Domain(name='{self.name}', url='{self.url}')"
