import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject


class UserDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("user", "/id", **kwargs)

    def revoke_token(self, jti):
        logging.info(f"Revoking token with jti {jti}")

        try:
            query = f'{self._select_prefix()} c WHERE c.jti = "{jti}"'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            users = list(items)

            if len(users) == 0:
                return None

            user = users[0]
            user["revoked"] = True

            self.container.upsert_item(user)

            return user
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def email_exists(self, email: str):
        logging.info(f"Checking if email {email} exists")

        try:
            query = f'{self._select_prefix()} c WHERE c.email = "{email}"'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            users = list(items)

            if len(users) == 0:
                return False

            return True
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def username_exists(self, username: str):
        logging.info(f"Checking if username {username} exists")

        try:
            query = f'{self._select_prefix()} c WHERE c.username = "{username}"'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            users = list(items)

            if len(users) == 0:
                return False

            return True
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def delete_by_email(self, email: str):
        logging.info(f"Deleting user with email {email}")

        try:
            user_data = self.get_by_email(email)

            if user_data is None:
                return

            UserDAO().delete(user_data["id"])

            return
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_username(self, username: str):
        logging.info(f"Fetching user with username {username}")

        try:
            query = f'{self._select_prefix()} c WHERE c.username = "{username}"'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            users = list(items)

            if len(users) == 0:
                return None

            return users[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def get_by_email(self, email: str):
        logging.info(f"Fetching user with email {email}")

        try:
            query = f'{self._select_prefix()} c WHERE c.email = "{email}"'
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            users = list(items)

            if len(users) == 0:
                return None

            return users[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err
