from vgs.sdk import auth_api
from vgs.sdk.errors import AuthenticationError
from vgs.configuration import Configuration
from vgs.exceptions import VgsApiException


class BaseApi(object):
    ACCESS_TOKEN_KEY = "access_token"
    REFRESH_TOKEN_KEY = "refresh_token"

    def __init__(self, config: Configuration):
        self.auth_environment = "dev" if config.environment == "dev" else "prod"
        self.auth_api = auth_api.create_api(self.auth_environment)
        self.auth_token = None
        self.refresh_token = None
        self.config = config

    def _auth(self):
        if not (self.config.service_account_name and self.config.service_account_password):
            raise VgsApiException(
                "API configuration is not complete. "
                "Please set 'service_account_name' and 'service_account_password' to use this API."
            )
        try:
            if self.auth_token is None:
                response = auth_api.get_auto_token(
                    self.auth_api,
                    client_id=self.config.service_account_name,
                    client_secret=self.config.service_account_password,
                )
                self.auth_token = response.body.get(self.ACCESS_TOKEN_KEY)
                if self.REFRESH_TOKEN_KEY in response.body:
                    self.refresh_token = response.body.get(self.REFRESH_TOKEN_KEY)
            else:
                if not auth_api.validate_access_token(self.auth_token):
                    response = auth_api.refresh_token(
                        self.auth_api, refresh_token=self.refresh_token
                    )
                    self.auth_token = response.body.get(self.REFRESH_TOKEN_KEY)
        except Exception as e:
            raise AuthenticationError(e)
