from typing import Optional, Union

# "Literal" is only available on Python 3.8
# and above, so for older versions of Python
# we use "typing_extensions" instead.
# (https://stackoverflow.com/questions/61206437/importerror-cannot-import-name-literal-from-typing)
try:
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal
from uuid import UUID

from pydantic import Field, BaseModel

from bodosdk.models.base import CamelCaseBase, CloudConfigStatus


class CreateAwsProviderData(CamelCaseBase):
    tf_backend_region: str = Field(..., alias="tfBackendRegion")
    secret_access_key: Optional[str] = Field(None, alias="secretAccessKey")
    access_key_id: Optional[str] = Field(None, alias="accessKeyId")


class CreateAzureProviderData(CamelCaseBase):
    tf_backend_region: Optional[str] = Field(None, alias="tfBackendRegion")
    subscription_id: str = Field(..., alias="subscriptionId")
    tenant_id: str = Field(..., alias="tenantId")
    resource_group: str = Field(..., alias="resourceGroup")


class CreateAwsCloudConfig(CamelCaseBase):
    cloud_provider: Literal["AWS"] = Field("AWS", alias="cloudProvider")
    name: str
    aws_provider_data: CreateAwsProviderData = Field(..., alias="awsProviderData")


class CreateAzureCloudConfig(CamelCaseBase):
    cloud_provider: Literal["AZURE"] = Field("AZURE", alias="cloudProvider")
    name: str
    azure_provider_data: CreateAzureProviderData = Field(..., alias="azureProviderData")


class AwsProviderData(CreateAwsProviderData):
    tf_bucket_name: Optional[str] = Field(None, alias="tfBucketName")
    tf_dynamo_db_table_name: Optional[str] = Field(None, alias="tfDynamoDBTableName")
    role_arn: Optional["str"] = Field(None, alias="RoleArn")
    external_id: Optional[str] = Field(None, alias="externalId")
    account_id: Optional[str] = Field(None, alias="accountId")


class AzureProviderData(CreateAzureProviderData):
    application_id: str = Field(..., alias="applicationId")


class AwsCloudConfig(CreateAwsCloudConfig):
    uuid: Union[str, UUID]
    status: CloudConfigStatus
    organization_uuid: Union[str, UUID] = Field(..., alias="organizationUUID")


class AzureCloudConfig(CreateAzureCloudConfig):
    uuid: Union[str, UUID]
    status: CloudConfigStatus
    organization_uuid: Union[str, UUID] = Field(..., alias="organizationUUID")


class CloudConfig(BaseModel):
    __root__: Union[AzureCloudConfig, AwsCloudConfig]


x = [
    {
        "cloudProvider": "AWS",
        "uuid": "9bed36ca-ce6f-4842-83b4-0a5b14689d0f",
        "name": "AWS",
        "status": "ACTIVE",
        "organizationUUID": "769a7a8b-06e0-4aba-8b29-fab0998f547e",
        "id": 6,
        "awsProviderData": {
            "roleArn": "arn:aws:iam::481633624848:role/BodoPlatformUser-9bed36ca-c",
            "tfBucketName": "bodo-bucket-9bed36ca-c",
            "tfDynamoDbTableName": "bodo-table-9bed36ca-c",
            "tfBackendRegion": "us-west-1",
            "externalId": "4d1d9cd4-67d2-4a0d-9d06-72796e1ea10e",
            "accountId": "481633624848",
        },
    },
    {
        "cloudProvider": "AZURE",
        "uuid": "6d74f513-e464-48d2-b2c0-0a180a9a9bb2",
        "name": "AZURE",
        "status": "ACTIVE",
        "organizationUUID": "769a7a8b-06e0-4aba-8b29-fab0998f547e",
        "id": 93,
        "azureProviderData": {
            "resourceGroup": "Bodo-Platform-Testing-InitAcc-RG",
            "subscriptionId": "335dd4ae-737b-4e85-ac0e-ca5220ce7de5",
            "tenantId": "ac373ae0-dc77-4cbb-bbb7-deddcf6133b3",
            "applicationId": "9ba6526c-331a-4459-b341-ca9bac6be302",
        },
    },
]

x1 = x[0]
x2 = x[1]
