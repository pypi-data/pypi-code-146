"""
This module contains the main entry point for the package.
"""

from transfermarket.page.competitions import CompetitionsPage

# from transfermarket.common.gender import Gender
# from transfermarket.common.model.player import Player
# from transfermarket.common.model.team import Team
# from transfermarket.common.utils import urljoin
from transfermarket.services.market import MarketService


class Market:
    """
    This class contains the main interface into the Transfermarkt package.
    """

    def __init__(self, **kwargs):
        self.market_service = kwargs.get("market_service", MarketService())
        self.competitions_page = kwargs.get("competitions_page", CompetitionsPage())

    def get_competitions(self):
        """
        Returns a list of competitions.
        """
        self.competitions_page.load()
        return self.competitions_page.get_competitions()

    def get_teams(self, competition_id: str):
        """
        Returns a list of teams for a given competition.
        """
        return self.market_service.get_teams(competition_id)

    def get_players(self, team_id: str):
        """
        Returns a list of players for a given team.
        """
        return self.market_service.get_players(team_id)
