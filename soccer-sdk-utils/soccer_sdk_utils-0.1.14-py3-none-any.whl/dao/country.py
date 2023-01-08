import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject


class CountryDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("country", "/id", **kwargs)

    def exists(self, name: str) -> bool:
        logging.info(f"Checking if country exists with name {name}")

        try:
            query = f"{self._select_prefix()} c WHERE c.name = '{name}'"
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            countries = list(items)

            return len(countries) > 0
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_name(self, name: str):
        logging.info(f"Fetching country with name {name}")

        try:
            query = f"{self._select_prefix()} c WHERE c.name = '{name}'"
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            countries = list(items)

            if len(countries) == 0:
                return None
            else:
                return countries[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err
