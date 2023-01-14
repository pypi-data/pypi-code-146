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


class ResourceDelete(ResourceBase):
    """
    Easily usable class that can be used to Delete resources in the custom resource code.
    """

    # #Delete Handler use case - WE THINK
    # with dynamodb.resource_delete(request=self.request,
    #                               primary_identifier=self._request.previousResourceState.ReadOnlyIdentifier) as DB:
    #
    #     #Arbitrary Code
    #     DB.update_model(model=self._callback_context["working_model"])
    #

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
        pass

    def __enter__(self) -> "ResourceDelete":
        logger.info("DynamoDelete Enter... ")

        # Check to see if the row/resource is not found
        self._not_found_check()

        logger.info("DynamoDelete Enter Completed")
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> Literal[False]:

        logger.info("DynamoDelete Exit...")

        if exception_type is None:
            logger.info("Has Failure = False")

            self._db_item_delete()
        else:
            # We failed in delete logic
            logger.info("Has Failure = True, row will not be deleted")

            # Failed during delete of resource for any number of reasons
            # Assuming it failed with a dependency.  Nothing deleted from dynamo DB perspective
            # Dont update the Row

        logger.info("DynamoDelete Exit Completed")

        # let exception flourish always
        return False
