import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject
from soccer_sdk_utils.gender import Gender


class MatchDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("match", "/id", **kwargs)

    def find(self, gender: Gender, date, team1, team2, division=None):
        logging.info(f"Fetching match '{date} {team1} vs {team2}' {gender.name}")

        try:
            matches = self.get_by_date(gender, date, division)

            for match in matches:
                if match["team1"] == team1 and match["team2"] == team2:
                    return match

                if match["team1"] == team2 and match["team2"] == team1:
                    return match

            return None
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def exists(self, gender: Gender, date, team1, team2):
        logging.info(
            f"Checking if match '{date} {team1} vs {team2}' {gender.name} exists"
        )

        try:
            for match in self.get_by_date(gender, date):
                if match["team1"] == team1 and match["team2"] == team2:
                    return True

                if match["team1"] == team2 and match["team2"] == team1:
                    return True

            return False
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_date(self, gender: Gender, date, division=None):
        logging.info(
            f"Fetching matches on date '{date}' for division '{division}' {gender.name}"
        )

        try:
            query = f"{self._select_prefix()} c WHERE c.date = '{date}' AND "
            if division is None:
                query += f"c.gender = '{gender}'"
            else:
                query += f"c.division = '{division}' AND c.gender = '{gender}'"

            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            return list(items)
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_date_range(self, gender: Gender, date_start, date_end, division=None):
        logging.info(
            f"Fetching matches between '{date_start}' and '{date_end}' for division '{division}'"
        )

        try:
            query = f"{self._select_prefix()} c WHERE "
            query += f"c.gender = '{gender}' AND "
            if division is None:
                query += f"(c.date BETWEEN '{date_start}' AND '{date_end}')"
            else:
                query += f"c.division = '{division}' AND "
                query += f"(c.date BETWEEN '{date_start}' AND '{date_end}')"

            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            return list(items)
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_team(self, gender: Gender, team):
        logging.info(f"Fetching matches for team '{team}' {gender.name}")

        try:
            query = f"{self._select_prefix()} c WHERE c.gender = '{gender}' AND (c.team1 = '{team}' OR c.team2 = '{team}')"
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            return list(items)
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err
