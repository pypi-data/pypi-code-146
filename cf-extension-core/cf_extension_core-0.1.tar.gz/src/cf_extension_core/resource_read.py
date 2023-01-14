import logging
import types
from typing import Type, Literal, TYPE_CHECKING, Optional

from cloudformation_cli_python_lib.interface import BaseResourceHandlerRequest

from cf_extension_core.resource_base import ResourceBase

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
else:
    DynamoDBServiceResource = object

# Module Logger
logger = logging.getLogger(__name__)


class ResourceRead(ResourceBase):
    # with dynamodb_read(primary_identifier=self._request.previousResourceState.ReadOnlyIdentifier,
    #                      request=self._request) as DB:
    #
    #     #Arbitrary Code
    #     res_model = DB.read_model()

    def __init__(
        self,
        request: BaseResourceHandlerRequest,
        db_resource: DynamoDBServiceResource,
        primary_identifier: str,
        type_name: str,
    ):

        super().__init__(
            request=request,
            db_resource=db_resource,
            primary_identifier=primary_identifier,
            type_name=type_name,
        )

    def read_model(
        self,
        model_type: Type[ResourceBase.T],
    ) -> ResourceBase.T:

        if self._primary_identifier is None:
            raise Exception("Primary Identifier cannot be Null")

        return self._db_item_get_model(model_type=model_type)

    def __enter__(self) -> "ResourceRead":
        logger.info("DynamoRead Enter... ")

        # Check to see if the row/resource is not found
        self._not_found_check()

        logger.info("DynamoRead Enter Completed")
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> Literal[False]:

        logger.info("DynamoRead Exit...")

        if exception_type is None:
            logger.info("Has Failure = False, row No Op")
        else:

            # We failed in update logic
            logger.info("Has Failure = True, row No Op")

        logger.info("DynamoRead Exit Completed")

        # let exception flourish always
        return False
