from datetime import timedelta
from typing import TYPE_CHECKING

import pydantic

AZURE_QUANTUM_RESOURCE_ID_REGEX = r"^/subscriptions/([a-fA-F0-9-]*)/resourceGroups/([^\s/]*)/providers/Microsoft\.Quantum/Workspaces/([^\s/]*)$"

_IONQ_API_KEY_LENGTH: int = 32
INVALID_API_KEY: str = _IONQ_API_KEY_LENGTH * "a"
MAX_EXECUTION_TIMEOUT_SECONDS = timedelta(hours=4).total_seconds()

if TYPE_CHECKING:
    PydanticExecutionTimeout = int
    PydanticAwsRoleArn = str
    PydanticS3BucketKey = str
    PydanticS3BucketName = str
    PydanticAzureResourceIDType = str
    PydanticIonQApiKeyType = str
    PydanticArgumentNameType = str
else:
    # TODO Simplify regular expressions in this file

    PydanticAwsRoleArn = pydantic.constr(
        strip_whitespace=True,
    )

    PydanticS3BucketName = pydantic.constr(strip_whitespace=True, min_length=3)

    PydanticS3BucketKey = pydantic.constr(strip_whitespace=True, min_length=1)

    PydanticAzureResourceIDType = pydantic.constr(regex=AZURE_QUANTUM_RESOURCE_ID_REGEX)

    PydanticIonQApiKeyType = pydantic.constr(
        regex=f"[A-Za-z0-9]{{{_IONQ_API_KEY_LENGTH}}}"
    )
    PydanticExecutionTimeout = pydantic.conint(gt=0, le=MAX_EXECUTION_TIMEOUT_SECONDS)

    PydanticArgumentNameType = pydantic.constr(regex="[_a-zA-Z][_a-zA-Z0-9]*")
