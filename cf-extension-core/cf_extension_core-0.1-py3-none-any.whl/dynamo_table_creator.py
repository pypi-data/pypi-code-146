"""
Generates the dynamo table and makes sure all the settings are correct for resource creation/deletion
"""
import logging
import time
import botocore.exceptions
from typing import TYPE_CHECKING
from cf_extension_core.constants import DynamoDBValues

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
else:
    DynamoDBServiceResource = object

# Module Logger
logger = logging.getLogger(__name__)


class DynamoTableCreator:
    def __init__(self, db_resource: DynamoDBServiceResource):
        self._client = db_resource

    def delete_table(self) -> None:
        if self.table_exists():
            logger.info("Deleting table: " + DynamoDBValues.TABLE_NAME)
            the_table = self._client.Table(DynamoDBValues.TABLE_NAME)
            the_table.delete()
            self._wait_for_table_to_be_deleted()

    def table_exists(self) -> bool:
        try:
            self._client.meta.client.describe_table(TableName=DynamoDBValues.TABLE_NAME)
            return True
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                return False
            else:
                raise

    def create_standard_table(self) -> None:

        if self.table_exists():
            logging.info("Table exist")
            return

        self._create_table(
            name=DynamoDBValues.TABLE_NAME,
            partition_key=DynamoDBValues.PARTITION_KEY,
        )

    def _create_table(
        self,
        name: str,
        partition_key: str,
    ) -> None:
        """
        Guarantees to create the table in dynamo db and waits for it to be active.
        If table already exists, this code exits cleanly
        """
        logger.debug("Creating table: " + name)

        try:
            self._client.create_table(
                AttributeDefinitions=[{"AttributeName": partition_key, "AttributeType": "S"}],
                KeySchema=[{"AttributeName": partition_key, "KeyType": "HASH"}],  # Required for a partition key
                TableName=name,
                BillingMode="PAY_PER_REQUEST",  # ON Demand
                SSESpecification={"Enabled": False},  # Opposite of what you think it should be.
            )

            # Wait for table to be active
            self._wait_for_table_to_be_active()
        except self._client.meta.client.exceptions.ResourceInUseException as ex:
            logger.debug("Table already exists")
            self._wait_for_table_to_be_active()

            # Table exists validate some of the properties?
            table = self._client.Table(name)

            # Key Schema
            keyschema = table.key_schema
            mypartkey = keyschema[0]
            if not (mypartkey["AttributeName"] == partition_key and mypartkey["KeyType"] == "HASH"):
                raise Exception("DynamoDB - Partition Key schema does not match: Actual: " + str(mypartkey)) from ex

            # If key schema is good, return
            # We are assuming here if the schema checks out, then this table should work for us.
            logger.debug("Table has correct settings, returning")
            return

    def _wait_for_table_to_be_active(self) -> None:
        logger.debug("Waiting till the table becomes ACTIVE")
        while True:
            status = self._client.Table(DynamoDBValues.TABLE_NAME).table_status
            if status == "ACTIVE":
                logger.debug("Table is Active")
                break
            else:
                time.sleep(2)

    def _wait_for_table_to_be_deleted(self) -> None:
        logger.debug("Waiting till the table deleted")
        while True:
            status = self.table_exists()
            if status is False:
                logger.debug("Table deleted")
                break
            else:
                time.sleep(2)


if __name__ == "__main__":
    import boto3

    boto3.setup_default_session(profile_name="CT", region_name="eu-west-2")
    dynamodb = boto3.resource("dynamodb")

    test = DynamoTableCreator(db_resource=dynamodb)
    print("Deleting table")
    test.delete_table()
    print("Creating table")
    test.create_standard_table()
    print("Table Created")
