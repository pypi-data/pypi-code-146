from searchunify.client.client import CONSTANTS
from searchunify.utils.constants.constants import AuthVariables, Constants

AUTH_VARS = AuthVariables()
CONSTANTS = Constants()

def get_auth_header():
    authHeader = { 
        'Authorization': None,
        'Content-Type': 'application/json'
    }
    if(AUTH_VARS.AUTH_TYPE == CONSTANTS.OAUTH2_DEL):
        authHeader['Authorization'] = 'Bearer ' + AUTH_VARS.ACCESS_TOKEN
    elif(AUTH_VARS.AUTH_TYPE == CONSTANTS.API_KEY_DEL):
        authHeader['Authorization'] = 'ApiKey ' + AUTH_VARS.ACCESS_TOKEN
    elif(AUTH_VARS.AUTH_TYPE == CONSTANTS.JWT_KEY_DEL):
        authHeader['Authorization'] = 'Jwt ' + AUTH_VARS.JWT_TOKEN
    else:
        raise Exception('Invalid authorization header.')
    
    return authHeader
