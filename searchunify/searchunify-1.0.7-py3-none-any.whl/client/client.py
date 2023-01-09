from searchunify.utils.validation.oauth2 import OauthValidator
from searchunify.utils.constants.constants import *

AUTH_VARS = AuthVariables()
CONSTANTS = Constants()

class Client:
    def authentication_type_validation(client):
        OauthValidator.instance_url(**client)
        AuthVariables.INSTANCE = client.get('instance').strip('/')
        if(client.get('client_id') and client.get('client_secret')):
            OauthValidator.access_token(**client)
            AuthVariables.AUTH_TYPE = CONSTANTS.OAUTH2_DEL
            AuthVariables.CLIENT_ID = client.get('client_id')
            AuthVariables.SECRETS = client.get('client_secret')

        elif(client.get('api_token')):
            OauthValidator.api_key_token(**client)
            AuthVariables.AUTH_TYPE = client.get('api_token')
            AuthVariables.AUTH_TYPE = CONSTANTS.API_KEY_DEL

        elif(client.get('jwt_token')):
            OauthValidator.jwt_token(**client)
            AuthVariables.JWT_TOKEN = client.get('jwt_token')
            AuthVariables.AUTH_TYPE = CONSTANTS.JWT_KEY_DEL

        else:
            raise Exception('Incomplete client parameters.')
            