from dataclasses import dataclass


@dataclass
class Club:
    """
    This class contains the domain model for a club.
    """

    id: int
    name: str
    total_players: int
    avg_age: float
    total_foreigners: int
    avg_market_value: str
    market_value: str

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.total_players = kwargs.get("total_players")
        self.avg_age = kwargs.get("avg_age")
        self.total_foreigners = kwargs.get("total_foreigners")
        self.avg_market_value = kwargs.get("avg_market_value")
        self.market_value = kwargs.get("market_value")

    def __repr__(self):
        attribute_value_pairs = [
            f"id={self.id}",
            f"name='{self.name}'",
            f"total_players={self.total_players}",
            f"avg_age={self.avg_age}",
            f"total_foreigners={self.total_foreigners}",
            f"avg_market_value='{self.avg_market_value}'",
            f"market_value='{self.market_value}'",
        ]

        return f"Club({', '.join(attribute_value_pairs)})"
