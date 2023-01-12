"""
This module contains domain models for a competition.
"""

from dataclasses import dataclass


@dataclass
class Competition:
    """
    This class contains the domain model for a competition.
    """

    id: str
    name: str
    country: str
    total_clubs: int
    total_players: int
    avg_age: float
    foreigners_percent: float
    total_value: str
    tier: str

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.country = kwargs.get("country")
        self.total_clubs = kwargs.get("total_clubs")
        self.total_players = kwargs.get("total_players")
        self.avg_age = kwargs.get("avg_age")
        self.foreigners_percent = kwargs.get("foreigners_percent")
        self.total_value = kwargs.get("total_value")
        self.tier = kwargs.get("tier")

    def __repr__(self):
        attribute_value_pairs = [
            f"id='{self.id}'",
            f"name='{self.name}'",
            f"country='{self.country}'",
            f"total_clubs={self.total_clubs}",
            f"total_players={self.total_players}",
            f"avg_age={self.avg_age}",
            f"foreigners_percent={self.foreigners_percent}",
            f"total_value='{self.total_value}'",
            f"tier='{self.tier}'",
        ]

        return f"Competition({', '.join(attribute_value_pairs)})"
