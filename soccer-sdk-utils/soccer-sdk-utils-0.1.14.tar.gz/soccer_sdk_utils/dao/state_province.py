import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject
from soccer_sdk_utils.dao.country import CountryDAO


class StateProvinceError(Exception):
    def __init__(self, message):
        super().__init__(message)


class StateProvinceDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("state_province", "/id", **kwargs)

    def exists(self, name: str):
        logging.info(f"Checking if state/province with name {name} exists")

        try:
            return self.get_by_name(name) is not None
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_name(self, name: str):
        logging.info(f"Fetching state/province with name {name}")

        try:
            query = f"{self._select_prefix()} c WHERE c.name = '{name}'"
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            states_provinces = list(items)

            if len(states_provinces) == 0:
                return None
            else:
                return states_provinces[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_code(self, code: str):
        logging.info(f"Fetching state/province with code {code}")

        try:
            query = f"{self._select_prefix()} c WHERE c.code = '{code}'"
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            states_provinces = list(items)

            if len(states_provinces) == 0:
                return None
            else:
                return states_provinces[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_country_name(self, name: str):
        logging.info(f"Fetching state/province with country name {name}")

        try:
            country_dao = CountryDAO()
            country = country_dao.get_by_name(name)

            if country is None:
                raise StateProvinceError(f"There are no countries with name {name}!")

            return self.get_by_country_id(country.get_soup("id"))
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_country_id(self, id: str):
        logging.info(f"Fetching state/province with country id {id}")

        try:
            query = f"{self._select_prefix()} c WHERE c.country = '{id}'"
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
