# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from chain_app_client_sdk.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    AUTH_SIGNUP = "/auth/signup"
    AUTH_SIGNIN = "/auth/signin"
    MAIN_POOL_GET_POOL_SIZE_HISTORY = "/main_pool/get_pool_size_history"
