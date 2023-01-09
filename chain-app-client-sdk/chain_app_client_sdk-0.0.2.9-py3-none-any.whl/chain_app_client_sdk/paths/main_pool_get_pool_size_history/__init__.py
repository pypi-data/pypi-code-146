# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from chain_app_client_sdk.paths.main_pool_get_pool_size_history import Api

from chain_app_client_sdk.paths import PathValues

path = PathValues.MAIN_POOL_GET_POOL_SIZE_HISTORY