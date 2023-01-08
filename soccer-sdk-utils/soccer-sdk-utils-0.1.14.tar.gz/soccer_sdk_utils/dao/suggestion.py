import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject


class SuggestionDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("suggestion", "/id", **kwargs)

    def get_by_state(self, state):
        logging.info(f"Fetching suggestions with state {state}")

        try:
            query = f"{self._select_prefix()} c WHERE c.state = '{state}'"
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
