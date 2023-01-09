from typing import Dict, Optional, Union

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.api_core.exceptions import ServiceUnavailable
from google.auth.exceptions import RefreshError

from arcane.core import UserRightsEnum, RightsLevelEnum, BadRequestError, BaseAccount
from arcane.credentials import get_user_decrypted_credentials
from arcane.datastore import Client as DatastoreClient
from arcane.requests import call_get_route

from .exceptions import GoogleAnalyticsAccountLostAccessException, GoogleAnalyticsServiceDownException



def get_google_analytics_account(
    base_account: BaseAccount,
    clients_service_url: Optional[str] = None,
    firebase_api_key: Optional[str] = None,
    gcp_credentials_path: Optional[str] = None,
    auth_enabled: bool = True
) -> Dict:
    if not clients_service_url or not firebase_api_key or not gcp_credentials_path:
        raise BadRequestError('clients_service_url or firebase_api_key or  gcp_credentials_path should not be None')
    url = f"{clients_service_url}/api/google-analytics-account?account_id={base_account['id']}&client_id={base_account['client_id']}"
    accounts = call_get_route(
        url,
        firebase_api_key,
        claims={'features_rights':{UserRightsEnum.AMS_GTP: RightsLevelEnum.VIEWER}, 'authorized_clients': ['all']},
        auth_enabled=auth_enabled,
        credentials_path=gcp_credentials_path
    )
    if len(accounts) == 0:
        raise BadRequestError(f'Error while getting google analytics account with: {base_account}. No account corresponding.')
    elif len(accounts) > 1:
        raise BadRequestError(f'Error while getting google analytics account with: {base_account}. Several account corresponding: {accounts}')

    return accounts[0]


def check_access_type_before_creation(ga_view_id: str,
                                    user_email: str,
                                    gcp_credentials_path: str,
                                    secret_key_file: str,
                                    gcp_project: str = '',
                                    by_pass_user_check: Optional[bool] = False,
                                    datastore_client: Optional[DatastoreClient] = None) -> bool:
    """ check access before posting account

    Args:
        ga_view_id (str): the id of the view we want access
        user_email (str): the email of the user checking the access
        gcp_credentials_path (str): Aracane credential path
        secret_key_file (str): the secret file
        gcp_project (str, optional): the Google Cloud Plateform project
        by_pass_user_check (Optional[bool], optional): By pass user access, used for super admin right. Defaults to False.
        datastore_client (Optional[DatastoreClient], optional): the Datastore client. Defaults to None.

    Raises:
        BadRequestError: Raise when arguments are not good
        GoogleAnalyticsAccountLostAccessException: Raise when we have no access

    Returns:
        bool: should use user access
    """
    should_use_user_access = True
    scopes = ['https://www.googleapis.com/auth/analytics.readonly']

    if not secret_key_file:
        raise BadRequestError('secret_key_file should not be None while using user access protocol')

    user_credentials = get_user_decrypted_credentials(
            user_email=user_email,
            secret_key_file=secret_key_file,
            gcp_credentials_path=gcp_credentials_path,
            gcp_project=gcp_project,
            datastore_client=datastore_client
        )

    try:
        service = build('analytics', 'v3', credentials=user_credentials, cache_discovery=False)
        _get_view_name_lgq(ga_view_id, service, user_email)
    except GoogleAnalyticsAccountLostAccessException as e:
        if not by_pass_user_check:
            raise e
        should_use_user_access = False
        pass

    arcane_credentials = service_account.Credentials.from_service_account_file(gcp_credentials_path, scopes=scopes)
    try:
        service = build('analytics', 'v3', credentials=arcane_credentials, cache_discovery=False)
        _get_view_name_lgq(ga_view_id, service, user_email)
        should_use_user_access = False
    except GoogleAnalyticsAccountLostAccessException as e:
        if by_pass_user_check and not should_use_user_access:
            raise e
        pass

    return should_use_user_access


def _get_view_name_lgq(ga_view_id: str, service, user_email: Union[str, None]) -> str:
    down_message = f"The Google Analytics API does not respond. Thus, we cannot check if we can access your Google Analytics account with the id: {ga_view_id}. Please try later"
    try:
        views = service.management().profiles().list(accountId='~all', webPropertyId='~all').execute()
    except HttpError as err:
        if err.resp.status >= 400 and err.resp.status < 500:
            raise GoogleAnalyticsAccountLostAccessException(get_exception_message_cannot_access(ga_view_id))
        else:
            raise GoogleAnalyticsServiceDownException(down_message)
    except ServiceUnavailable:
        raise GoogleAnalyticsServiceDownException(down_message)
    except RefreshError as err:
        if ('Token has been expired' in str(err) or 'invalid_grant' in str(err)) and user_email:
            print(str(err))
            raise GoogleAnalyticsAccountLostAccessException(
                f"{user_email} authorization has expired. Please renew the access to {ga_view_id}.")
        raise

    for view in views.get('items', []):
        if view.get('id') == ga_view_id:
            return view.get('name', '')

    raise GoogleAnalyticsAccountLostAccessException(get_exception_message_cannot_access(ga_view_id))



def get_exception_message_cannot_access(ga_view_id: str) -> str:
    return f'We cannot find this account ({ga_view_id}). Are you sure you entered the correct id?'

