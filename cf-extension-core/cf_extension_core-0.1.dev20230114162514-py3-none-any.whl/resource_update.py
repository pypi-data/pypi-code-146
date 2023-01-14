import logging
import types
from typing import Type, Literal, TYPE_CHECKING, Optional

from cloudformation_cli_python_lib.interface import BaseModel
from cloudformation_cli_python_lib.interface import (
    BaseResourceHandlerRequest as _BaseResourceHandlerRequest,
)

from cf_extension_core.resource_base import ResourceBase as _ResourceBase

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
else:
    DynamoDBServiceResource = object

# Module Logger
logger = logging.getLogger(__name__)


class ResourceUpdate(_ResourceBase):
    """
    Easily usable class that can be used to Update resources in the custom resource code.
    """

    # #Create Handler use case - as we update via callbacks, continue to update row
    # with dynamodb_update(primary_identifier=self._callback_context["working_model"].ReadOnlyIdentifier,
    #                      request=self._request) as DB:
    #
    #     #Arbitrary Code
    #     DB.update_model(model=self._callback_context["working_model"])
    #
    #
    # #Update Use case
    # with dynamodb_update(primary_identifier=self._request.previousResourceState.ReadOnlyIdentifier,
    #                      request=self._request) as DB:
    #
    #     # Arbitrary Code
    #     DB.update_model(model=self._callback_context["working_model"])

    def __init__(
        self,
        request: _BaseResourceHandlerRequest,
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

        self._updated_model: Optional[BaseModel] = None
        self._was_model_updated = False

    def update_model(
        self,
        updated_model: _ResourceBase.T,
    ) -> None:

        if self._primary_identifier is None:
            raise Exception("Primary Identifier cannot be Null")

        if updated_model is None:
            raise Exception("The current_model cannot be Null")

        self._was_model_updated = True
        self._updated_model = updated_model

    def __enter__(self) -> "ResourceUpdate":
        logger.info("DynamoUpdate Enter... ")

        # Check to see if the row/resource is not found
        self._not_found_check()

        logger.info("DynamoUpdate Enter Completed")
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> Literal[False]:

        logger.info("DynamoUpdate Exit...")

        if exception_type is None:
            logger.info("Has Failure = False")

            if self._was_model_updated:
                logger.info("Row being Updated")
                self._db_item_update_model(model=self._updated_model)
        else:

            # We failed in update logic
            logger.info("Has Failure = True, row NOT updated")

            # Failed during update of resource for any number of reasons
            # Assuming it failed with no resource actually changed from a dynamo perspective.
            # Dont update the Row

        logger.info("DynamoUpdate Exit Completed")

        # let exception flourish always
        return False
