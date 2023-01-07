from soccer_sdk_utils.gender import Gender
from dataclasses import dataclass


@dataclass
class Event:
    id: int
    name: str
    gender: Gender

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", -1)
        self.name = kwargs.get("name", "unknown")
        self.gender = kwargs.get("gender", Gender.All)

    def __str__(self):
        return f"{self.id} - '{self.name}'"

    def __repr__(self):
        return f"Event(id={self.id}, name={self.name}, gender='{self.gender.name}')"

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.name < other.name


@dataclass
class Flight:
    division_id: int
    id: int
    name: str
    teams_count: int
    has_active_schedule: bool
    hide_settings: int

    def __init__(self, **kwargs):
        self.division_id = kwargs.get("division_id", -1)
        self.id = kwargs.get("id", -1)
        self.name = kwargs.get("name", "unknown")
        self.teams_count = kwargs.get("teams_count", 0)
        self.has_active_schedule = kwargs.get("has_active_schedule", False)
        self.hide_settings = kwargs.get("hide_settings", 0)

    def __str__(self):
        return self.name

    def __repr__(self):
        attribute_value_pairs = [
            f"division_id={self.division_id}",
            f"id={self.id}",
            f"name={self.name}",
            f"teams_count={self.teams_count}",
            f"has_active_schedule={self.has_active_schedule}",
            f"hide_settings={self.hide_settings}"
        ]

        return f"Flight({', '.join(attribute_value_pairs)})"

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.name < other.name


@dataclass
class Division:
    id: int
    name: str
    flights: list[Flight]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", -1)
        self.name = kwargs.get("name", "unknown")
        self.flights = kwargs.get("flights", [])

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Division(id={self.id}, name={self.name})"

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.name < other.name
