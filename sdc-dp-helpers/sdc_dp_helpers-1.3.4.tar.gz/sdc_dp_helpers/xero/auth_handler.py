# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,unused-import,import-error,ungrouped-imports,wildcard-import,unused-argument,unused-wildcard-import
import json
import ast
import requests
from oauth2 import *
from xero.auth import OAuth2Credentials
from xero.exceptions import XeroForbidden


def token_isvalid(creds: OAuth2Credentials) -> bool:
    if not isinstance(creds, OAuth2Credentials):
        raise TypeError("creds is not an object of type OAuth2Credentials")

    return creds.get_tenants()[0]["tenantId"] is not None


def get_auth_token(client_id: str, local_token_path: str) -> OAuth2Credentials:
    """
    Consumes the client id and the previous auth processes refresh token.
    This returns an authentication token that will last 30 minutes
    to make queries the minute it is used. Or it will expire in 60 days of no use.
    The newly generated last refresh token now needs token stored for
    next use.
    PS: we receive and save the auth_token in a local dir supplied by the encapsulating project
    we never interact with s3 from inside of this class
    """
    if (not client_id) or (len(client_id) != 32):
        raise ValueError("Invalid client_id")

    with open(local_token_path, "r") as token_file:
        auth_token = ast.literal_eval(token_file.read())
    print("original token:", auth_token)
    auth_creds = OAuth2Credentials(client_id, client_secret="", token=auth_token)
    return refresh_auth_token(client_id, auth_creds, local_token_path)


def refresh_auth_token(
    client_id: str, auth_creds: OAuth2Credentials, local_token_path: str
) -> OAuth2Credentials:
    cred = {
        "grant_type": "refresh_token",
        "refresh_token": auth_creds.token["refresh_token"],  #
        "client_id": client_id,
    }
    # print(cred, auth_creds.token)
    response = requests.post(
        "https://identity.xero.com/connect/token", cred, timeout=30
    )
    auth_token = response.json()
    print("response:", auth_token)
    print("auth keys", auth_token.keys())
    err_message = auth_token.get("error")
    if err_message:
        raise Exception(err_message)

    print("Writing new Xero token to path: ", local_token_path)
    with open(local_token_path, "w") as outfile:
        outfile.write(json.dumps(auth_token))

    auth_creds = OAuth2Credentials(client_id, client_secret="", token=auth_token)
    if not token_isvalid(auth_creds):
        raise XeroForbidden(
            f"Error while trying to authenticate the refreshed token: {str(auth_creds)}"
        )
    return auth_creds


def save_auth_token(auth_token):
    """
    function to persist the latest auth token to s3
    """
    # TO DO: pull update_refresh_token from readers into here

    pass
