from cloudformation_cli_python_lib.interface import (
    BaseResourceHandlerRequest as _BaseResourceHandlerRequest,
)
import boto3

from typing import TYPE_CHECKING, Optional as _Optional

import cf_extension_core.resource_update as _resource_update
import cf_extension_core.resource_create as _resource_create
import cf_extension_core.resource_read as _resource_read
import cf_extension_core.resource_delete as _resource_delete
import cf_extension_core.resource_list as _resource_list

from cf_extension_core.dynamo_table_creator import DynamoTableCreator  # noqa: F401
from cf_extension_core.custom_resource_helpers import CustomResourceHelpers  # noqa: F401
from cf_extension_core.constants import DynamoDBValues  # noqa: F401

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import (
        DynamoDBServiceResource as _DynamoDBServiceResource,
    )
else:
    _DynamoDBServiceResource = object


def generate_dynamo_resource() -> _DynamoDBServiceResource:
    return boto3.resource("dynamodb")


def create_resource(
    request: _BaseResourceHandlerRequest,
    type_name: str,
    db_resource: _DynamoDBServiceResource,
    primary_identifier: _Optional[str] = None,
) -> _resource_create.ResourceCreate:

    return _resource_create.ResourceCreate(
        db_resource=db_resource,
        type_name=type_name,
        primary_identifier=primary_identifier,
        request=request,
    )


def update_resource(
    primary_identifier: str,
    type_name: str,
    request: _BaseResourceHandlerRequest,
    db_resource: _DynamoDBServiceResource,
) -> _resource_update.ResourceUpdate:
    return _resource_update.ResourceUpdate(
        db_resource=db_resource,
        type_name=type_name,
        primary_identifier=primary_identifier,
        request=request,
    )


def delete_resource(
    primary_identifier: str,
    type_name: str,
    request: _BaseResourceHandlerRequest,
    db_resource: _DynamoDBServiceResource,
) -> _resource_delete.ResourceDelete:
    return _resource_delete.ResourceDelete(
        db_resource=db_resource,
        type_name=type_name,
        primary_identifier=primary_identifier,
        request=request,
    )


def read_resource(
    primary_identifier: str,
    type_name: str,
    request: _BaseResourceHandlerRequest,
    db_resource: _DynamoDBServiceResource,
) -> _resource_read.ResourceRead:
    return _resource_read.ResourceRead(
        db_resource=db_resource,
        type_name=type_name,
        primary_identifier=primary_identifier,
        request=request,
    )


def list_resource(
    type_name: str,
    request: _BaseResourceHandlerRequest,
    db_resource: _DynamoDBServiceResource,
) -> _resource_list.ResourceList:

    return _resource_list.ResourceList(db_resource=db_resource, type_name=type_name, request=request)
