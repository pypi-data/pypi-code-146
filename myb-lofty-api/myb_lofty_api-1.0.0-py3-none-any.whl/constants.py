class LoftyApi:
    def __init__(self, api_host_override: str = None):
        self.host = 'https://api.lofty.ai' if api_host_override is None else api_host_override
        self.api_endpoint = self.host + '/prod'
        self.region = 'us-east-1'
        self.auth = ApiAuth()


class ApiAuth:
    def __init__(self):
        self.cognito_idp = AuthCognitoIdp()


class AuthCognitoIdp:
    def __init__(self):
        self.region = 'us-east-1'
        self.identity_pool_id = 'us-east-1:2c317179-beec-488f-8bc2-f7be6fc13872'
        self.user_pool_id = 'us-east-1_TiP3uwZvv'
        self.user_pool_web_client_id = '7rjqrno1ul86rr0dajjjhvik78'
        self.login = f'cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}'
