import os

import pydantic

__all__ = ["API_CONFIG"]

os.environ["PRICEHUBBLE_CONF"] = os.environ.get(
    "PRICEHUBBLE_CONF", "config.env"
)


class ApiConfig(pydantic.BaseSettings):
    """
    Pricehubble API configuration loaded from the env file.
    The env file is by default 'config.env' in the current directory,
    but the path can additionally be set by the environmental variable
    'PRICEHUBBLE_CONF'
    """

    API_DOSSIER_URL: str
    API_LOGIN_URL: str
    API_USERNAME: str
    API_PASSWORD: str

    class Config:
        env_file: str = os.environ["PRICEHUBBLE_CONF"]


API_CONFIG = ApiConfig()
