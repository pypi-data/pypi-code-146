from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from retrying import retry

class ServicePrincipalAuthorizationProvider:

    def __init__(self, tenant_name, principal_client_id, principal_secret):
        self.tenant_name = tenant_name
        self.principal_secret = principal_secret
        self.client_id = principal_client_id

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=300000)
    def get_auth_token(self):
        app_client_id = self.client_id
        app_secret = self.principal_secret
        client = BackendApplicationClient(client_id=app_client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url='https://login.microsoftonline.com/19393f3e-7639-4afe-bd82-ffb6e79b24b3/oauth2/v2.0/token', client_id=app_client_id,
        client_secret=app_secret,scope='https://management.azure.com/.default')
        access_token = token['access_token']
        return access_token

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=300000)
    def get_auth_token_graph_scope(self,scope):
        app_client_id = self.client_id
        app_secret = self.principal_secret
        client = BackendApplicationClient(client_id=app_client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url='https://login.microsoftonline.com/19393f3e-7639-4afe-bd82-ffb6e79b24b3/oauth2/v2.0/token', client_id=app_client_id,
        client_secret=app_secret,scope=scope)
        access_token = token['access_token']
        return access_token