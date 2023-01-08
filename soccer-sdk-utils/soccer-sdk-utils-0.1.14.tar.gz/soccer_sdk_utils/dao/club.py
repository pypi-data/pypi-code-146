import logging

from azure.cosmos import exceptions
from marshmallow import EXCLUDE

from soccer_sdk_utils.dao.base import DataAccessObject
from soccer_sdk_utils.dao.club_translation import ClubTranslationDAO
from soccer_sdk_utils.schema.club import ClubSchema


class ClubDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("club", "/id", **kwargs)

    def get_by_name(self, name: str):
        """
        Get a club by name

        :param name: Name of the club
        :return: Club data as a dict
        """
        logging.info(f"Fetching club with name {name}")

        name = ClubTranslationDAO().translate(name)

        try:
            query = f"{self._select_prefix()} c WHERE c.name = '{name}'"
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            clubs = list(items)

            if len(clubs) == 0:
                return None
            else:
                return clubs[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err

    def lookup_league(self, club_name: str) -> str | None:
        club_data = self.get_by_name(club_name)

        if club_data is None:
            return None

        club = ClubSchema(unknown=EXCLUDE).load(club_data)

        if club is None:
            return None

        return club.league

    def get_by_league(self, league: str):
        logging.info(f"Fetching clubs in league {league}")

        try:
            query = f'SELECT c.name FROM {self.cname} c JOIN (SELECT VALUE t FROM t in c.leagues WHERE t.name = "{league}")'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            return list(items)
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
