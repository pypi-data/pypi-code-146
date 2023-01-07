import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject


class PlayerDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("player", "/id", **kwargs)

    def search(self, gender: str, year: str, state: str):
        logging.info("Fetching players")

        try:
            query = f'{self._select_prefix()} c WHERE c.year = "{year}" AND c.gender = "{gender}" AND c.state = "{state}"'

            logging.info(f"Query: {query}")

            query_iterable = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            return list(query_iterable)
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_fname_lname(self, fname: str, lname: str):
        logging.info(f"Fetching player with first name {fname} and last name {lname}")

        try:
            query = f'{self._select_prefix()} c WHERE c.first_name = "{fname}" and c.last_name = "{lname}"'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            players = list(items)

            if len(players) == 0:
                return None
            else:
                return players[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err
