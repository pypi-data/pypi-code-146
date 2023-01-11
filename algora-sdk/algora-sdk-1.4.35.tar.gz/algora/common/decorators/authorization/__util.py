import json
import logging

from requests import Response

from algora.common.errors import AuthenticationError

logger = logging.getLogger(__name__)


def _handle_auth_response(auth_response: Response, error_msg: str) -> dict:
    if auth_response.status_code == 200:
        bearer_token = auth_response.json()['access_token']
        return {'Authorization': f'Bearer {bearer_token}'}
    else:
        error = AuthenticationError(error_msg)
        logger.error(error)
        raise error


def _access_token(access_token: str) -> dict:
    return json.loads(access_token)


def _validate_headers(**kwargs):
    headers = kwargs.get("headers", {})

    if headers.get("Authorization") is None:
        error = AuthenticationError("Authentication for the package was configured incorrectly and is either "
                                    "missing a ALGORA_ACCESS_TOKEN or ALGORA_REFRESH_TOKEN or ALGORA_USER and "
                                    "ALGORA_PWD environment variable(s)")
        logger.error(error)
        # TODO this fails when using FRED API (outside of Algora API, so it doesn't need Authorization header)
        #  raise error
