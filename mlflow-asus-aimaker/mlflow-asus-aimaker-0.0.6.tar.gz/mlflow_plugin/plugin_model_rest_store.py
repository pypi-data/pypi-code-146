import os
from mlflow.store.model_registry.rest_store import RestStore
from mlflow.utils import rest_utils

# Extra environment variables which take precedence for setting the basic/bearer
# auth on http requests.
_TRACKING_USERNAME_ENV_VAR = "MLFLOW_TRACKING_USERNAME"
_TRACKING_PASSWORD_ENV_VAR = "MLFLOW_TRACKING_PASSWORD"
_TRACKING_TOKEN_ENV_VAR = "MLFLOW_TRACKING_TOKEN"

# sets verify param of 'requests.request' function
# see https://requests.readthedocs.io/en/master/api/
_TRACKING_INSECURE_TLS_ENV_VAR = "MLFLOW_TRACKING_INSECURE_TLS"
_TRACKING_SERVER_CERT_PATH_ENV_VAR = "MLFLOW_TRACKING_SERVER_CERT_PATH"

# sets cert param of 'requests.request' function
# see https://requests.readthedocs.io/en/master/api/
_TRACKING_CLIENT_CERT_PATH_ENV_VAR = "MLFLOW_TRACKING_CLIENT_CERT_PATH"


class PluginRegistryRestStore(RestStore):
    def __init__(self, store_uri=None):
        self.is_plugin = True
        self.restStore = RestStore(self._get_default_host_creds)
        super().__init__(self._get_default_host_creds)

    def _get_default_host_creds(store_uri):
        return rest_utils.MlflowHostCreds(
            host=os.environ.get("MLFLOW_REST_URL"),
            username=os.environ.get(_TRACKING_USERNAME_ENV_VAR),
            password=os.environ.get(_TRACKING_PASSWORD_ENV_VAR),
            token=os.environ.get(_TRACKING_TOKEN_ENV_VAR),
            ignore_tls_verification=os.environ.get(
                _TRACKING_INSECURE_TLS_ENV_VAR) == "true",
            client_cert_path=os.environ.get(
                _TRACKING_CLIENT_CERT_PATH_ENV_VAR),
            server_cert_path=os.environ.get(
                _TRACKING_SERVER_CERT_PATH_ENV_VAR),
        )
