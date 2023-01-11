"""
Add it to to your Django settings

REST_FRAMEWORK = {
  ...
  'DEFAULT_AUTHENTICATION_CLASSES': [
    ...
    'rest_framework.authentication.SessionAuthentication',
    'w.drf.sso.sso_auth_backend.SsoAuthBackend',
  ]
}

Need extra django settings configuration

SSO={
    "SERVER_URL": <sso url>,
    "REALM": <sso api realm>,
    "CLIENT_ID": <sso client id api>,
    "CLIENT_SECRET_KEY": <sso client secret see Client credentials>,
    "USER_SERVICE": <path to ModelService handling sso user model>
}

USER_SERVICE should inherit from SsoUserMixin and AbstractModelService
and model should inherit from AbstractSsoUser
"""
from django.conf import settings
from rest_framework.authentication import TokenAuthentication

from w import utils
from w.services.technical.sso_service import SsoService
from w.tests.helpers import sso_test_helper


class SsoAuthBackend(TokenAuthentication):
    keyword = "Bearer"

    def _is_token_valid(self, token):
        return SsoService.is_token_valid(token)

    def _create_or_update_user(self, valid_token):
        user_service = utils.import_path(settings.SSO["USER_SERVICE"])
        data = valid_token.to_dict()
        uuid = data.pop("sso_uuid")
        user, created = user_service.create_or_update_by_uuid(uuid, data)
        return user.user

    def authenticate_credentials(self, token):
        # Checks token is active
        valid_token = self._is_token_valid(token)

        if "USER_SERVICE" not in settings.SSO:
            raise RuntimeError("'USER_SERVICE' is missing from SSO settings")

        user = self._create_or_update_user(valid_token)
        return user, None


class SsoAuthTestBackend(SsoAuthBackend):  # pragma: no cover
    _user = None

    @classmethod
    def set_user(cls, user):
        cls._user = user

    def _is_token_valid(self, token):
        if token != "invalid-token":
            return token
        with sso_test_helper.valid_token_failure():
            SsoService.is_token_valid(token)

    def _create_or_update_user(self, valid_token):
        return self._user
