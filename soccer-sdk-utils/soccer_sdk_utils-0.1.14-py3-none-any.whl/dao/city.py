import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject


class CityDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("city", "/id", **kwargs)

    def get_by_state_province_id(self, id: str):
        logging.info(f"Fetching cities with state/province id {id}")

        try:
            query = f"{self._select_prefix()} c WHERE c.spid = '{id}'"
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            return items
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_name(self, name: str):
        logging.info(f"Fetching city with name {name}")

        try:
            query = f'{self._select_prefix()} c WHERE c.name = "{name}"'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            cities = list(items)

            if len(cities) == 0:
                return None

            return cities[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err
