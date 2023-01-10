import os
import json
from google.cloud import secretmanager as _secretmanager
from dwh_oppfolging.misc import get_oppfolging_environment, ENV_KNADA_GKE


def _get_knada_gke_secrets() -> dict:
    "reads and returns knada gcp secrets as a dict"
    secrets = _secretmanager.SecretManagerServiceClient()
    resource_name = f"{os.environ['KNADA_TEAM_SECRET']}/versions/latest"
    secret = secrets.access_secret_version(name=resource_name)
    data = secret.payload.data.decode("UTF-8") # type: ignore
    return json.loads(data)

def get_secrets() -> dict:
    """reads secrets"""
    env = get_oppfolging_environment()
    if env != ENV_KNADA_GKE and "GOOGLE_APPLICATION_SECRETS" not in os.environ:
        raise Exception("Secrets in this environment require path to json account creds set in GOOGLE_APPLICATION_CREDENTIALS.")
    return _get_knada_gke_secrets()
