import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

from requests.auth import AuthBase
from .responses.auth import SignInResponse, AwsCredentials
from .constants import LoftyApi, AuthCognitoIdp

from .aws_cognito_idp import AwsCognitoIdp


class ClientAuth(AuthBase):
    def __init__(self, verbose: bool = False, api_host_override: str = None):
        """
        Initializes the API client.

        Parameters:
        verbose (bool): Whether to print messages to the console verbosely.
        api_host_override (str): An override for the API Host defined in API Constants - only override for testing.
        """
        # These will get set during the login process
        self._session = None
        self._aws_credentials = None

        self._verbose: bool = verbose
        self._api_constants: LoftyApi = LoftyApi(api_host_override)
        self._auth_constants: AuthCognitoIdp = self._api_constants.auth.cognito_idp
        self._cognito_idp_client = boto3.client('cognito-idp', region_name=self._auth_constants.region)
        self._cognito_identity = boto3.client('cognito-identity', region_name=self._auth_constants.region)
        self._aws_auth = AwsCognitoIdp(
            pool_id=self._auth_constants.user_pool_id,
            client_id=self._auth_constants.user_pool_web_client_id,
            client=self._cognito_idp_client
        )

    # Auth handler for requests using this ClientAuth
    # Intercepts requests to inject authorization headers
    def __call__(self, request):
        aws_request = AWSRequest(
            method=request.method,
            url=request.url,
            # Manage which additional headers are included in the signature
            headers={
                'Cache-Control': 'no-cache'
            }
        )
        signer = SigV4Auth(self._aws_credentials, 'execute-api', region_name=self._api_constants.region)
        signer.add_auth(aws_request)
        aws_request_headers = dict(aws_request.headers)
        request.headers.update({
            **aws_request_headers,
        })
        # TODO: handle token expiry and refreshes
        return request

    def _get_jwts(self, username: str, password: str) -> SignInResponse:
        authentication_result = self._aws_auth.authenticate_user(username, password)
        return SignInResponse(authentication_result)

    def _get_credentials(self, sign_in_response: SignInResponse) -> AwsCredentials:
        identity_id_response = self._cognito_identity.get_id(IdentityPoolId=self._auth_constants.identity_pool_id)
        self._aws_identity_id = identity_id_response.get('IdentityId')
        credentials = self._cognito_identity.get_credentials_for_identity(
            IdentityId=self._aws_identity_id,
            Logins={
                self._auth_constants.login: sign_in_response.id_token
            }
        )
        return AwsCredentials(credentials.get('Credentials'))

    def login(self, username: str, password: str) -> AwsCredentials:
        sign_in_response = self._get_jwts(username, password)
        credentials = self._get_credentials(sign_in_response)
        session = boto3.Session(
            aws_access_key_id=credentials.access_key_id,
            aws_session_token=credentials.session_token,
            aws_secret_access_key=credentials.secret_key,
            region_name=self._auth_constants.region
        )
        session_credentials = session.get_credentials()
        self._session = session
        self._aws_credentials = session_credentials.get_frozen_credentials()
        return credentials
