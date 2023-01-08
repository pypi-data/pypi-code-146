import logging
import os
import sys
import uuid

from azure.cosmos import CosmosClient, PartitionKey, exceptions
from dotenv import load_dotenv


class DataAccessObject(object):
    def __init__(self, *args, **kwargs):
        self.cname = args[0]
        self.partition_key = args[1]

        self.last_query = None

        debug = kwargs.get("debug", False)

        basedir = sys.path[0]
        load_dotenv(os.path.join(basedir, ".env"))

        db_name = os.environ.get("DATABASE_NAME")

        if hasattr(sys, "_called_from_test"):
            db_name += "-test"

        acct_uri = os.environ["COSMOS_ACCOUNT_URI"]
        acct_key = os.environ["COSMOS_ACCOUNT_KEY"]

        if debug:
            # Create a logger for the 'azure' SDK
            logger = logging.getLogger("azure")
            logger.setLevel(logging.DEBUG)

            # Configure a console output
            handler = logging.StreamHandler(stream=sys.stdout)
            logger.addHandler(handler)

            self.client = CosmosClient(
                url=acct_uri, credential=acct_key, logging_enable=True
            )
        else:
            self.client = CosmosClient(url=acct_uri, credential=acct_key)

        try:
            # Try to create the database if it doesn't exist
            self.db = self.client.create_database(db_name)
        except exceptions.CosmosResourceExistsError:
            self.db = self.client.get_database_client(db_name)

        try:
            self.container = self.db.create_container(
                self.cname, PartitionKey(path=self.partition_key)
            )
        except exceptions.CosmosResourceExistsError:
            self.container = self.db.get_container_client(self.cname)

    def _select_prefix(self):
        return f"SELECT * FROM {self.cname}"

    def get_all(self):
        logging.info(f"Fetching all {self.cname}s")

        try:
            query = f"{self._select_prefix()} c"
            self.last_query = query
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

    def get(self, id):
        logging.info(f"Fetching {self.cname} {id}")
        try:
            query = f"{self._select_prefix()} c WHERE c.id = '{id}'"
            self.last_query = query
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            for item in items:
                if item.get("id") != id:
                    continue

                return item

            return None
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def create(self, data):
        logging.info(f"Creating {self.cname}")

        try:
            if not data.get("id"):
                data["id"] = str(uuid.uuid4())

            return self.container.create_item(data)
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def update(self, id, data):
        logging.info(f"Updating {self.cname} {id}")

        try:
            return self.container.upsert_item(data, id)
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err

    def delete(self, id):
        logging.info(f"Deleting {self.cname} {id}")

        try:
            query = f"{self._select_prefix()} c WHERE c.id = '{id}'"
            self.last_query = query
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )
            for item in items:
                self.container.delete_item(item, id)
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err
