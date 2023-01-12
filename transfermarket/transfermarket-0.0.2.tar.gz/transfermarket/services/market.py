"""This module provides services for the transfermarket."""
import requests

from transfermarket.common.gender import Gender
from transfermarket.common.utils import urljoin
from transfermarket.models.player import Player
from transfermarket.models.team import Team


class MarketService:
    """The MarketService class provides methods to retrieve data from the transfermarkt site."""

    BASE_URL = "https://www.transfermarkt.com"

    POSITION_MAPPING = {
        "1": "Goalkeeper",
        "2": "Defender",
        "3": "Midfielder",
        "4": "Forward",
    }

    def __init__(self):
        pass

    @property
    def headers(self):
        """
        Retrieve the headers for the request.
        """
        return {"User-Agent": "transfermarkt"}

    def get(self, url: str) -> requests.Response:
        """
        Retrieve a response from the transfermarkt site.
        """
        headers = {"user-agent": "transfer_market_service"}
        url = urljoin(self.BASE_URL, url)
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        return res

    def get_teams(self, identifier: str):
        """
        Retrieve a list of teams.
        """
        teams = []

        res = self.get(f"/quickselect/teams/{identifier}")
        records = res.json()
        for record in records:
            team = Team()
            team.id = record.get("id")
            team.title = record.get("name")
            team.add_property("id", record.get("id"))
            team.add_property("link", record.get("link"))

            teams.append(team)

        return teams

    # def get_player_profile(self, name: str, pid: str) -> dict:
    #     """Retrieve a player profile
    #
    #     Example:
    #         https://www.transfermarkt.com/alexander-molnar/profil/spieler/100000
    #     """
    #     profile = {}
    #
    #     return profile

    def get_players(self, identifier: str):
        """
        Retrieve a list of players.
        """
        players = []

        res = self.get(f"/quickselect/players/{identifier}")
        records = res.json()

        for record in records:
            player = Player()
            player.id = record.get("id")
            player.gender = Gender.Male
            player.name = record.get("name")
            player.position = record.get("positionId")

            player.position = str(player.position)

            if player.position is not None:
                if player.position in self.POSITION_MAPPING:
                    player.position = self.POSITION_MAPPING[player.position]
                else:
                    raise ValueError(f"Unknown position identifier: {player.position}")

            player.add_property("id", record.get("id"))
            player.add_property("url", record.get("link"))
            player.add_property("position_id", record.get("positionId"))
            player.add_property("jersey_number", record.get("shirtNumber"))

            players.append(player)

        return players
