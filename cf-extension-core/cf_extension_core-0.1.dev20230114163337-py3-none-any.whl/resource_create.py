import logging
import types
from typing import Type, Literal, TYPE_CHECKING, cast, Optional

import cloudformation_cli_python_lib.exceptions
from cloudformation_cli_python_lib.interface import BaseModel, BaseResourceHandlerRequest

from cf_extension_core.resource_base import ResourceBase as _ResourceBase

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
else:
    DynamoDBServiceResource = object

# Module Logger
logger = logging.getLogger(__name__)


class ResourceCreate(_ResourceBase):
    """
    Easily usable class that can be used to create resources in the custom resource code.
    """

    # Sample use case - Non known primary_identifier as input
    # with dynamodb_create(self._request) as DB:
    #     created_resource = self.action()
    #     if created_resource:
    #        DB.set_resource_created(primary_identifier=self._callback_context["working_model"].ReadOnlyIdentifier,
    #                                working_model=self._callback_context["working_model"])

    # Sample use case - Primary identifier known ahead of time
    # with dynamodb_create(self._request, self.primary_identifier) as DB:
    #     #AUTOMATIC CHECKING OF AlreadyEXISTS done by DynamoDB code when we have a primary identifier ahead of
    #     time. IE a user parameter
    #     created_resource = self.action()
    #     if created_resource:
    #        DB.set_resource_created(primary_identifier=self._callback_context["working_model"].ReadOnlyIdentifier,
    #                                working_model=self._callback_context["working_model"])

    def __init__(
        self,
        request: BaseResourceHandlerRequest,
        type_name: str,
        db_resource: DynamoDBServiceResource,
        primary_identifier: Optional[str] = None,
    ):

        super().__init__(
            request=request,
            db_resource=db_resource,
            primary_identifier=primary_identifier,
            type_name=type_name,
        )

        self._set_resource_created_called = False
        self._primary_identifier = primary_identifier
        self._current_model: Optional[BaseModel] = None

    def set_resource_created(
        self,
        primary_identifier: str,
        current_model: BaseModel,
    ) -> None:

        if primary_identifier is None:
            raise Exception("Primary Identifier cannot be Null")

        if current_model is None:
            raise Exception("The current_model cannot be Null")

        self._set_resource_created_called = True
        self._primary_identifier = primary_identifier
        self._current_model = current_model

    def duplicate_primary_identifier(self) -> None:
        if self._db_item_exists():
            raise cloudformation_cli_python_lib.exceptions.AlreadyExists(
                type_name=self._type_name, identifier=self._get_primary_identifier()
            )

    def __enter__(self) -> "ResourceCreate":
        logger.info("DynamoCreate Enter... ")

        # If primary identifier is already set (known with user input) - we need to check if the row already exists
        # Use case - sometimes the primary identifier is user input instead of a created resource
        # Real world example - S3 Bucket Name...
        if self._primary_identifier is not None:
            self.duplicate_primary_identifier()
        else:
            # We havent created the primary identifier yet or its not input - so cant do anything about it yet....
            pass

        logger.info("DynamoCreate Enter Complete")
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> Literal[False]:

        logger.info("DynamoCreate Exit...")

        # End with
        # IF success DB code should create the row if set_resource_created was called
        # If success but set_resource_created was not called - Do nothing in Dynamo -
        #   resource already existed - statemachine execution
        # If error/exception be - no row created and let it propagate upwards

        # Determine if error happened (bad CR to determine if we should delete the item at the end or not.
        # Resource was created...

        if exception_type is None:
            logger.info("Has Failure = False")
            if not self._set_resource_created_called:
                # Resource was already created - nothing to do here - no row needs to be created
                pass
            else:
                # Check if row exists - if it does we need to fail out correctly
                if self._primary_identifier is not None:
                    self.duplicate_primary_identifier()

                logger.info("Row being created")

                self._db_item_insert_without_overwrite(cast(BaseModel, self._current_model))
        else:

            # We failed in creation logic
            logger.info("Has Failure = True, row NOT created")

            # Failed during creation of resource for any number of reasons
            # Assuming it failed with no resource actually created - only valid assumption we can make.
            # Dont create the Row
            pass

        logger.info("DynamoCreate Exit Completed")

        # let exception flourish always
        return False
