import logging
import json
from typing import Type, Optional, Any, TYPE_CHECKING, TypeVar, cast


from cloudformation_cli_python_lib import exceptions

from cf_extension_core.dynamo_table_creator import DynamoTableCreator

from cloudformation_cli_python_lib.interface import (
    BaseResourceHandlerRequest as _BaseResourceHandlerRequest,
    BaseModel as _BaseModel,
)
from cryptography.fernet import Fernet, InvalidToken
import datetime

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
    from mypy_boto3_dynamodb.service_resource import Table
else:
    DynamoDBServiceResource = object
    Table = object

import cf_extension_core.constants as constants

# Module Logger
logger = logging.getLogger(__name__)


class ResourceBase:

    T = TypeVar("T", bound=Optional[_BaseModel])

    def __init__(
        self,
        db_resource: DynamoDBServiceResource,
        request: _BaseResourceHandlerRequest,
        type_name: str,
        primary_identifier: Optional[str] = None,
    ):

        self._request: _BaseResourceHandlerRequest = request
        self._db_resource = db_resource

        self._primary_identifier = primary_identifier
        self._type_name = type_name

        # Guarantee the table exists for any and all resources.
        DynamoTableCreator(self._db_resource).create_standard_table()

    # Business logic for saving Model to Dynamo for RO use cases primarily#######
    class ResourceData:
        _HELPER_KEY = "SleJXVw-6uvCUbd3whNDafJZ-Fc2UU0iQ1NiRCDY2dY="
        T = TypeVar("T", bound=Optional[_BaseModel])

        @staticmethod
        def _model_to_string(model: T) -> str:

            # MODEL is not serializable
            #
            mystr = json.dumps(model._serialize())  # type: ignore
            return Fernet(ResourceBase.ResourceData._HELPER_KEY.encode()).encrypt(mystr.encode()).decode()

        # Read Only use case - we need to handle
        @staticmethod
        def _model_from_string(
            modelstr: str,
            class_type: Type[T],
        ) -> Any:
            try:
                mystr = Fernet(ResourceBase.ResourceData._HELPER_KEY.encode()).decrypt(modelstr.encode()).decode()
            except InvalidToken as exc:
                raise ResourceBase.ResourceData.DecryptionException(exc.args) from exc

            mymapping = json.loads(mystr)

            return class_type._deserialize(json_data=mymapping)  # type: ignore

        class DecryptionException(Exception):
            def __init__(self, *args: Any) -> None:
                super().__init__(*args)

    def _current_time(self) -> str:
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

    def _get_primary_identifier(self) -> str:
        if self._primary_identifier is None:
            raise Exception("primary_identifier is still Null")

        return cast(str, self._primary_identifier)

    def _not_found_check(self) -> None:
        if not self._db_item_exists():
            raise exceptions.NotFound(type_name=self._type_name, identifier=self._get_primary_identifier())

    # Finding the table ###
    def _dynamo_db_table(self) -> Table:

        return self._db_resource.Table(constants.DynamoDBValues.TABLE_NAME)

    # Insert Requests#######
    def _db_item_insert_without_overwrite(
        self,
        model: T,
    ) -> None:

        the_table = self._dynamo_db_table()

        requested_item = {
            constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME: self._get_primary_identifier(),
            constants.RowColumnNames.STACK_NAME: self._request.stackId,
            constants.RowColumnNames.RESOURCE_NAME: self._request.logicalResourceIdentifier,
            constants.RowColumnNames.LASTUPDATED_NAME: self._current_time(),
            constants.RowColumnNames.MODEL_NAME: ResourceBase.ResourceData._model_to_string(model),
            constants.RowColumnNames.TYPE_NAME: self._type_name,
        }

        logger.info("Create Request item: %s", str(requested_item))
        try:
            the_table.put_item(
                Item=requested_item,
                ConditionExpression="attribute_not_exists(#pk)",
                ExpressionAttributeNames={"#pk": constants.DynamoDBValues.PARTITION_KEY},
            )
            logger.debug("Row created....")
        except self._db_resource.meta.client.exceptions.ConditionalCheckFailedException as ex:
            logger.info("Row exists when trying to create resource, data tier is out of sorts")
            raise Exception(
                "Attempting to create resource record failed in dynamo, please contact CLOUD team for help"
            ) from ex

    # POST Requests#######
    def _db_item_update_model(
        self,
        model: T,
    ) -> None:

        logger.info("_db_item_update_model called")
        the_table = self._dynamo_db_table()

        model_str = ResourceBase.ResourceData._model_to_string(model)

        the_table.update_item(
            Key={constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME: self._get_primary_identifier()},
            UpdateExpression="SET #model = :model, #lastupdate = :lastupdate",
            ConditionExpression="attribute_exists(#pk)",
            ExpressionAttributeNames={
                "#model": constants.RowColumnNames.MODEL_NAME,
                "#lastupdate": constants.RowColumnNames.LASTUPDATED_NAME,
                "#pk": constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME,
            },
            ExpressionAttributeValues={
                ":model": model_str,
                ":lastupdate": self._current_time(),
            },
        )
        logger.info("_db_item_update_model Finished...")

    # GET Requests ####
    def _db_get_item(self) -> Any:
        logger.info("get_item read...")
        the_table = self._dynamo_db_table()

        response = the_table.get_item(
            Key={constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME: self._get_primary_identifier()},
            ConsistentRead=True,
        )
        logger.info("get_item read properly...")

        if "Item" in response:
            return response["Item"]
        else:
            return None

    def _db_item_exists(self) -> bool:
        myitem = self._db_get_item()
        if myitem is None:
            logger.info("Row not found")
            return False
        else:
            logger.info("Row found: %s", str(myitem))
            return True

    def _db_item_get_model(
        self,
        model_type: Type[T],
    ) -> Any:

        logger.info("_db_item_get_model called")

        # Raw Item -
        item = self._db_get_item()
        if item is None:
            raise Exception("Row in dynamodb did not exist when attempting to read model data")

        logger.info("_db_item_get_model read properly...")

        # Get the data out of it
        random_str = cast(str, item[constants.RowColumnNames.MODEL_NAME])

        return ResourceBase.ResourceData._model_from_string(random_str, class_type=model_type)

    def _db_item_list_primary_identifiers_for_cr_type(self):
        if self._type_name is None:
            raise Exception("Cannot support getting primary identifiers if I dont know type to get")

        return_value = []

        scan_output = self._db_resource.meta.client.scan(
            TableName=constants.DynamoDBValues.TABLE_NAME,
            Select="SPECIFIC_ATTRIBUTES",
            ProjectionExpression=constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME,
            FilterExpression="#tn = :tn",
            ExpressionAttributeNames={"#tn": constants.RowColumnNames.TYPE_NAME},
            ExpressionAttributeValues={":tn": self._type_name},
            ConsistentRead=True,
        )
        for item in scan_output["Items"]:
            return_value.append(item[constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME])

        # Paginate indefinitely
        if "LastEvaluatedKey" in scan_output:
            last_evaluated_key_data = scan_output["LastEvaluatedKey"]

            while last_evaluated_key_data is not None:
                scan_output2 = self._db_resource.meta.client.scan(
                    TableName=constants.DynamoDBValues.TABLE_NAME,
                    Select="SPECIFIC_ATTRIBUTES",
                    ProjectionExpression=constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME,
                    FilterExpression="#tn = :tn",
                    ExpressionAttributeNames={"#tn": constants.RowColumnNames.TYPE_NAME},
                    ExpressionAttributeValues={":tn": self._type_name},
                    ConsistentRead=True,
                    ExclusiveStartKey=last_evaluated_key_data,
                )
                for item in scan_output2["Items"]:
                    return_value.append(item[constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME])

                if "LastEvaluatedKey" in scan_output2:
                    last_evaluated_key_data = scan_output2["LastEvaluatedKey"]
                else:
                    last_evaluated_key_data = None

        return return_value

    # DELETE Requests######
    def _db_item_delete(
        self,
        best_effort: bool = False,
    ) -> None:

        logger.info(
            "Deleting item with best effort set to : %s. Primary Key: %s",
            str(best_effort),
            self._get_primary_identifier(),
        )

        the_table = self._dynamo_db_table()
        try:
            the_table.delete_item(
                Key={constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME: self._get_primary_identifier()},
                ConditionExpression="attribute_exists(#pk)",
                ExpressionAttributeNames={"#pk": constants.RowColumnNames.PRIMARY_IDENTIFIER_NAME},
            )
            logger.info("Item Deleted...")
        except self._db_resource.meta.client.exceptions.ConditionalCheckFailedException as ex:
            if best_effort:
                logger.info("Item did not exist, returning...")
                return
            else:
                logger.info("Item does not exist when trying to delete resource, data tier is out of sorts")
                raise Exception(
                    "Attempting to delete resource record failed in dynamo, please contact CLOUD team for help"
                ) from ex
