import base64
import json

from openapi_client import ApiClient, Configuration
from openapi_client.api.daily_production_api import DailyProductionApi
from openapi_client.api.well_api import WellApi
from openapi_client.api.wellbore_api import WellboreApi
from openapi_client.api.formation_property_api import FormationPropertyApi
from openapi_client.api.deviation_survey_api import DeviationSurveyApi
from openapi_client.api.tubing_api import TubingApi
from openapi_client.api.casing_api import CasingApi


class XectaApi:
    """
    This is a simple wrapper around the openapi generated client that adds some extra functionality for mtls auth
    as well as generating access tokens.
    """
    _configuration: Configuration = None

    def __init__(self, base_url: str, client_cert_file: str, client_key_file: str):
        """
        This will boot strap the initial configuration before allowing the client to authenticate. Upon successful
        authentication a XectaApiClient instance will be returned
        :param base_url: The base url without any extra path parameters. example "https://testawsapi.onxecta.com"
        :param client_cert_file: The full path to the client certificate file for mtls.
        :param client_key_file: the full path to the client certificate key for mtls.
        """
        self._configuration = Configuration(host=base_url)

        # Must initialize the configuration token to None initially or the client initialization will fail
        # with an error about missing access_token property.
        self._configuration.access_token = None

        # Initialize your mtls certificate and key that were provided by Xecta onboarding.
        # Note this should be the absolute path to your client certificate and key.
        self._configuration.cert_file = client_cert_file
        self._configuration.key_file = client_key_file

    class XectaApiClient:
        """
        This is an implementation of the api client that executes api functions. An instance of
        this class is returned from the xecta api authenticate function however this can be initialized
        manually if you already have a valid bearer token.
        """

        def __init__(self, configuration, bearer_token: str):
            self._configuration = configuration
            self.bearer_token = bearer_token
            self._configuration.access_token = bearer_token

        def daily_production_api(self) -> DailyProductionApi:
            with ApiClient(self._configuration) as api_client:
                return DailyProductionApi(api_client)

        def well_header_api(self) -> WellApi:
            with ApiClient(self._configuration) as api_client:
                return WellApi(api_client)

        def wellbore_api(self) -> WellboreApi:
            with ApiClient(self._configuration) as api_client:
                return WellboreApi(api_client)

        def wellbore_formation_api(self) -> FormationPropertyApi:
            with ApiClient(self._configuration) as api_client:
                return FormationPropertyApi(api_client)

        def deviation_survey_api(self) -> DeviationSurveyApi:
            with ApiClient(self._configuration) as api_client:
                return DeviationSurveyApi(api_client)

        def wellbore_tubing_api(self) -> TubingApi:
            with ApiClient(self._configuration) as api_client:
                return TubingApi(api_client)

        def wellbore_casing_api(self) -> CasingApi:
            with ApiClient(self._configuration) as api_client:
                return CasingApi(api_client)

    def authenticate(self, api_key: str, api_secret: str) -> XectaApiClient:
        """
        This function will handle the authentication and upon successful authentiction return a xecta api client
        implementation.
        :param api_key: The api key that was distributed by xecta during onboarding.
        :param api_secret: The api secret that was distributed by xecta during onboarding.
        :return: XectaApiClient implementation upon successful authentication.
        """
        with ApiClient(self._configuration) as api_client:
            encoded = f"{api_key}:{api_secret}".encode("utf-8")
            basic_auth = base64.b64encode(encoded).decode("utf-8")
            query_params = {"grant_type": "client_credentials"}
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {basic_auth}"
            }
            client_response = api_client.rest_client.POST(url=f"{self._configuration.host}/authenticate/oauth2/token",
                                                          headers=headers,
                                                          query_params=query_params)
            response_data = json.loads(client_response.data.decode('utf-8'))
            return XectaApi.XectaApiClient(self._configuration, response_data['access_token'])
