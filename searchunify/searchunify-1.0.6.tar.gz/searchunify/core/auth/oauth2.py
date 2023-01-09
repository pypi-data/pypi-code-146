from searchunify.client.client import CONSTANTS
from searchunify.utils.http_client.request_handler import RequestManager
from searchunify.utils.apis.apis import Apis
from searchunify.utils.constants.constants import AuthVariables, Constants
import base64

API = Apis.get_apis('oauth')
AUTH_VARS = AuthVariables()
CONSTANTS = Constants()

def base64_encode(args):
    message = args.get('client_id')+":"+args.get('client_secret')
    message = message.encode('ascii')
    message = base64.b64encode(message)
    base64_message = message.decode('ascii')
    playLoad = 'grant_type='+CONSTANTS.GRANT_TYPE+'&username='+args.get('username')+'&password='+args.get('password')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic '+base64_message,
        'cache-contro': 'no-cache'
    }
    return {"playload": playLoad, "headers": headers}

class Oauth2:
    def generate_access_token(args):
        try:
            url = AUTH_VARS.INSTANCE + API['accessToken']
            del args['instance']
            result = base64_encode(args)
            response = RequestManager.http_request(
                "POST", url, headers=result["headers"], data=result["playload"])
            if (response['accessToken'] and response['refreshToken']):
                AuthVariables.ACCESS_TOKEN = response['accessToken']
                AuthVariables.REFRESH_TOKEN = response['refreshToken']
                return 'SearchUnify client initialize successfully.'
            else:
                raise Exception('SearchUnify client not initialized.')
        except Exception as e:
            raise Exception('SearchUnify client not initialized.', e)


    def access_token_from_refresh_token():
        try:
            url = AUTH_VARS.INSTANCE + API['accessToken']
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'cache-contro': 'no-cache'
            }
            payload = 'grant_type='+CONSTANTS.GRANT_TYPE_REFRESH_TOKEN+'&refresh_token='+AUTH_VARS.REFRESH_TOKEN + '&client_id='+ AUTH_VARS.CLIENT_ID + '&client_secret='+ AUTH_VARS.SECRETS
            response = RequestManager.http_request(
                "POST", url, headers=headers, data=payload)
            if (response['accessToken'] and response['refreshToken']):
                AuthVariables.ACCESS_TOKEN = response['accessToken']
                AuthVariables.REFRESH_TOKEN = response['refreshToken']
                return 'Token refreshed successfully.'
            else:
                raise Exception('Token not refreshed.')
        except Exception as e:
            raise Exception('Access token not refreshed.', e)
