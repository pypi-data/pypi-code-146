import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject


class ConferenceDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("conference", "/id", **kwargs)

    def exists(self, division: str, name: str):
        conference = self.get_by_division_and_name(division, name)

        if conference is None:
            return False

        return True

    def get_by_division_and_name(self, division: str, name: str):
        try:
            query = f"{self._select_prefix()} c WHERE c.division = '{division}' AND c.name = '{name}'"
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            conferences = list(items)
            if len(conferences) == 0:
                return None
            else:
                return conferences[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
