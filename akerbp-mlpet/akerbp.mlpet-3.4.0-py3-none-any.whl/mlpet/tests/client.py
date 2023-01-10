import os

from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import APIKey

CLIENT_NAME = "MLPet testing"
CLIENT_NAME_FUNCTIONS = "MLPet testing, functions"
PROJECT = "akbp-subsurface"


class MissingEnvironmentVariableError(Exception):
    """Raised if an environment variable is missing"""


try:
    credentials = APIKey(os.environ["COGNITE_API_KEY"])
except KeyError as e:
    raise MissingEnvironmentVariableError(
        "Environment variable 'COGNITE_API_KEY' is missing, unable to initialize client for testing"
    ) from e

try:
    credentials_functions = APIKey(os.environ["COGNITE_API_KEY_FUNCTIONS"])
except KeyError as e:
    raise MissingEnvironmentVariableError(
        "Environment variable 'COGNITE_API_KEY_FUNCTIONS' is missing, unable to initialize client for testing"
    ) from e

client_config = ClientConfig(
    client_name=CLIENT_NAME,
    project=PROJECT,
    credentials=credentials,
)
client_config_functions = ClientConfig(
    client_name=CLIENT_NAME_FUNCTIONS,
    project=PROJECT,
    credentials=credentials_functions,
)

CLIENT = CogniteClient(config=client_config)
CLIENT_FUNCTIONS = CogniteClient(config=client_config_functions)
