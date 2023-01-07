import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject


class ClubTranslationDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("club_translation", "/id", **kwargs)

    def get_by_source(self, source: str) -> list[dict]:
        query = f'{self._select_prefix()} c WHERE c["from"] = "{source}"'
        try:
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            translations = list(items)

            return translations
        except exceptions.CosmosHttpResponseError as err:
            print(f"Query: {query}")
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_mapping(self, from_: str, to_: str):
        query = f'{self._select_prefix()} c WHERE c["from"] = "{from_}" AND c["to"] = "{to_}"'
        try:
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            translations = list(items)

            if len(translations) > 0:
                return translations[0]

            return None
        except exceptions.CosmosHttpResponseError as err:
            print(f"Query: {query}")
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def translate(self, name: str):
        if name is None:
            return None

        name = name.strip()

        query = f'{self._select_prefix()} c WHERE c["from"] = "{name}"'
        try:
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            translations = list(items)

            if len(translations) > 0:
                logging.info(f"Translating club name {name}")
                return translations[0]["to"]

            logging.info(f"No translation found for club name {name}")
            return name
        except exceptions.CosmosHttpResponseError as err:
            print(f"Query: {query}")
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err
