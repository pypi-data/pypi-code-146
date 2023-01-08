import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject


class BlacklistTokenDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("blacklist_token", "/id", **kwargs)

    def is_blacklisted(self, auth_token: str) -> bool:
        logging.info(f"Checking if token {auth_token} is blacklisted")

        try:
            query = f'{self._select_prefix()} c WHERE c.token = "{auth_token}"'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            tokens = list(items)

            if len(tokens) == 0:
                return False

            return True
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def delete_by_token(self, token: str):
        logging.info(f"Deleting token {token} from blacklist")

        try:
            query = f'{self._select_prefix()} c WHERE c.token = "{token}"'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            tokens = list(items)

            if len(tokens) == 0:
                return

            for token in tokens:
                self.delete(token.get("id"))
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err
