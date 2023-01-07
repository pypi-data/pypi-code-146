from typing import Optional

from rhino_health.lib.constants import ApiEnvironment
from rhino_health.lib.rest_api.error_handler import ErrorHandler
from rhino_health.lib.rest_api.rhino_authenticator import AuthenticationDetails, RhinoAuthenticator
from rhino_health.lib.rest_handler import RequestDataType, RestHandler
from rhino_health.lib.rhino_client import RhinoClient, SDKVersion
from rhino_health.lib.utils import rhino_error_wrapper


# Class docstring in rhino_client for autodoc
class RhinoSession(RhinoClient):
    @rhino_error_wrapper
    def __init__(
        self,
        authentication_details: AuthenticationDetails,
        otp_code: Optional[str] = None,
        rhino_api_url: str = ApiEnvironment.PROD_API_URL,
        sdk_version: str = SDKVersion.PREVIEW,
        show_traceback: bool = False,
    ):
        super().__init__(
            rhino_api_url=rhino_api_url, sdk_version=sdk_version, show_traceback=show_traceback
        )
        self.authenticator = RhinoAuthenticator(self.api_url, authentication_details, otp_code)
        self.login()
        self.rest_adapter = RestHandler(
            session=self,
            base_url=self.api_url,
            adapters={
                self.authenticator.__class__.__name__: self.authenticator,
                ErrorHandler.__class__.__name__: ErrorHandler(),
            },
        )

    def login(self):
        """
        @autoapi False
        Login to the Rhino Cloud API. Called automatically on initialization
        """
        self.authenticator.authenticate()

    def switch_user(self, authentication_details, otp_code=None):
        """
        Switch the currently logged in user.

        Parameters
        ----------
        authentication_details: AuthenticationDetails
            A dictionary containing authentication details
        otp_code: Optional[str]
            2FA login code if 2FA is enabled for the account

        See Also
        --------
        rhino_health.lib.rest_api.rhino_authenticator.AuthenticationDetails: Authentication Details
        """
        new_authenticator = RhinoAuthenticator(self.api_url, authentication_details, otp_code)
        self.login()
        self.authenticator = new_authenticator
        self.rest_adapter.adapters[self.authenticator.__class__.__name__] = self.authenticator

    # These are just remappings for now until we need more complex stuff in future
    @rhino_error_wrapper
    def get(self, url: str, params: Optional[dict] = None, adapter_kwargs: Optional[dict] = None):
        """
        Low level interface for submitting a REST GET request.

        Parameters
        ----------
        url: str
            The URL that you are hitting
        params: Optional[dict]
            A dictionary of `query params <https://en.wikipedia.org/wiki/Query_string>`_ to send with the request
        adapter_kwargs: Optional[dict]
            | (Advanced) a dictionary of additional kwargs to pass to the system
            | • accepted_status_codes List[int]: List of status codes to accept
            | • data_as_json bool: Pass the data attribute as a json to `requests <https://docs.python-requests.org/en/latest/>`_

        Examples
        --------
        >>> session.get("/alpha/secret/api").raw_response.json()
        { "status": "success" }

        Returns
        -------
        api_response: APIResponse
            Result of making the HTTP GET request

        See Also
        --------
        rhino_health.lib.rest_api.api_response.APIResponse: Response object
        """
        return self.rest_adapter.get(url=url, params=params, adapter_kwargs=adapter_kwargs)

    @rhino_error_wrapper
    def post(
        self,
        url: str,
        data: Optional[RequestDataType] = None,
        params: Optional[dict] = None,
        adapter_kwargs: dict = None,
    ):
        """
        Low level interface for submitting a REST POST request.

        Parameters
        ----------
        url: str
            The URL that you are hitting
        data: Union[str, dict, list]
            The payload to include with the POST request
        params: Optional[dict]
            A dictionary of `query params <https://en.wikipedia.org/wiki/Query_string>`_ to send with the request
        adapter_kwargs: Optional[dict]
            | (Advanced) a dictionary of additional kwargs to pass to the system
            | • accepted_status_codes List[int]: List of status codes to accept
            | • data_as_json bool: Pass the data attribute as a json to `requests <https://docs.python-requests.org/en/latest/>`_


        Examples
        --------
        >>> session.post(
        ...   "/alpha/secret/api",
        ...   {"arbitrary_payload": "value"}
        ... ).raw_response.json()
        { "status": "success" }

        Returns
        -------
        api_response: APIResponse
            Result of making the HTTP Post request

        See Also
        --------
        rhino_health.lib.rest_api.api_response.APIResponse: Response object
        """
        return self.rest_adapter.post(
            url=url,
            data=data,
            params=params,
            adapter_kwargs=adapter_kwargs,
        )
