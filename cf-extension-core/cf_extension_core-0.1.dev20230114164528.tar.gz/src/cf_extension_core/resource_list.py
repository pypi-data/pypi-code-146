import logging
import types

from typing import Type, Literal, TYPE_CHECKING, Optional, List

from cloudformation_cli_python_lib.interface import BaseResourceHandlerRequest

from cf_extension_core.resource_base import ResourceBase

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
else:
    DynamoDBServiceResource = object

# Module Logger
logger = logging.getLogger(__name__)


class ResourceList(ResourceBase):
    """
    Easily usable class that can be used to List resources in the custom resource code.
    """

    # with dynamodb_list(request=self._request) as DB:
    #
    #     #Arbitrary Code
    #     res_model = DB.read_model()

    def __init__(
        self,
        request: BaseResourceHandlerRequest,
        db_resource: DynamoDBServiceResource,
        type_name: str,
    ):

        super().__init__(
            request=request,
            db_resource=db_resource,
            primary_identifier=None,
            type_name=type_name,
        )

    def list_identifiers(self) -> List[str]:

        return self._db_item_list_primary_identifiers_for_cr_type()

    def __enter__(self) -> "ResourceList":
        logger.info("DynamoList Enter... ")

        # Check to see if the row/resource is not found
        # No - list literally cannot do this - we have no identifier
        # self._not_found_check()

        logger.info("DynamoList Enter Completed")
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> Literal[False]:

        logger.info("DynamoList Exit...")

        if exception_type is None:
            logger.info("Has Failure = False, row No Op")
        else:

            # We failed in update logic
            logger.info("Has Failure = True, row No Op")

        logger.info("DynamoList Exit Completed")

        # let exception flourish always
        return False
