# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from chain_app_client_sdk.paths.auth_signup import Api

from chain_app_client_sdk.paths import PathValues

path = PathValues.AUTH_SIGNUP