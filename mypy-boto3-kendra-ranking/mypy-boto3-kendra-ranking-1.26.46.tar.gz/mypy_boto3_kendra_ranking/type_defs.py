"""
Type annotations for kendra-ranking service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kendra_ranking/type_defs/)

Usage::

    ```python
    from mypy_boto3_kendra_ranking.type_defs import CapacityUnitsConfigurationTypeDef

    data: CapacityUnitsConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import RescoreExecutionPlanStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CapacityUnitsConfigurationTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteRescoreExecutionPlanRequestRequestTypeDef",
    "DescribeRescoreExecutionPlanRequestRequestTypeDef",
    "DocumentTypeDef",
    "ListRescoreExecutionPlansRequestRequestTypeDef",
    "RescoreExecutionPlanSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RescoreResultItemTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateRescoreExecutionPlanRequestRequestTypeDef",
    "CreateRescoreExecutionPlanRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateRescoreExecutionPlanResponseTypeDef",
    "DescribeRescoreExecutionPlanResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RescoreRequestRequestTypeDef",
    "ListRescoreExecutionPlansResponseTypeDef",
    "RescoreResultTypeDef",
)

CapacityUnitsConfigurationTypeDef = TypedDict(
    "CapacityUnitsConfigurationTypeDef",
    {
        "RescoreCapacityUnits": int,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

DeleteRescoreExecutionPlanRequestRequestTypeDef = TypedDict(
    "DeleteRescoreExecutionPlanRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DescribeRescoreExecutionPlanRequestRequestTypeDef = TypedDict(
    "DescribeRescoreExecutionPlanRequestRequestTypeDef",
    {
        "Id": str,
    },
)

_RequiredDocumentTypeDef = TypedDict(
    "_RequiredDocumentTypeDef",
    {
        "Id": str,
        "OriginalScore": float,
    },
)
_OptionalDocumentTypeDef = TypedDict(
    "_OptionalDocumentTypeDef",
    {
        "GroupId": str,
        "Title": str,
        "Body": str,
        "TokenizedTitle": Sequence[str],
        "TokenizedBody": Sequence[str],
    },
    total=False,
)


class DocumentTypeDef(_RequiredDocumentTypeDef, _OptionalDocumentTypeDef):
    pass


ListRescoreExecutionPlansRequestRequestTypeDef = TypedDict(
    "ListRescoreExecutionPlansRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

RescoreExecutionPlanSummaryTypeDef = TypedDict(
    "RescoreExecutionPlanSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Status": RescoreExecutionPlanStatusType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

RescoreResultItemTypeDef = TypedDict(
    "RescoreResultItemTypeDef",
    {
        "DocumentId": str,
        "Score": float,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateRescoreExecutionPlanRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRescoreExecutionPlanRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdateRescoreExecutionPlanRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRescoreExecutionPlanRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "CapacityUnits": CapacityUnitsConfigurationTypeDef,
    },
    total=False,
)


class UpdateRescoreExecutionPlanRequestRequestTypeDef(
    _RequiredUpdateRescoreExecutionPlanRequestRequestTypeDef,
    _OptionalUpdateRescoreExecutionPlanRequestRequestTypeDef,
):
    pass


_RequiredCreateRescoreExecutionPlanRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRescoreExecutionPlanRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateRescoreExecutionPlanRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRescoreExecutionPlanRequestRequestTypeDef",
    {
        "Description": str,
        "CapacityUnits": CapacityUnitsConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
        "ClientToken": str,
    },
    total=False,
)


class CreateRescoreExecutionPlanRequestRequestTypeDef(
    _RequiredCreateRescoreExecutionPlanRequestRequestTypeDef,
    _OptionalCreateRescoreExecutionPlanRequestRequestTypeDef,
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateRescoreExecutionPlanResponseTypeDef = TypedDict(
    "CreateRescoreExecutionPlanResponseTypeDef",
    {
        "Id": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRescoreExecutionPlanResponseTypeDef = TypedDict(
    "DescribeRescoreExecutionPlanResponseTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "CapacityUnits": CapacityUnitsConfigurationTypeDef,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Status": RescoreExecutionPlanStatusType,
        "ErrorMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RescoreRequestRequestTypeDef = TypedDict(
    "RescoreRequestRequestTypeDef",
    {
        "RescoreExecutionPlanId": str,
        "SearchQuery": str,
        "Documents": Sequence[DocumentTypeDef],
    },
)

ListRescoreExecutionPlansResponseTypeDef = TypedDict(
    "ListRescoreExecutionPlansResponseTypeDef",
    {
        "SummaryItems": List[RescoreExecutionPlanSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RescoreResultTypeDef = TypedDict(
    "RescoreResultTypeDef",
    {
        "RescoreId": str,
        "ResultItems": List[RescoreResultItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
