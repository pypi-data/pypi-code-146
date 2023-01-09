import typing_extensions

from chain_app_client_sdk.apis.tags import TagValues
from chain_app_client_sdk.apis.tags.auth_api import AuthApi
from chain_app_client_sdk.apis.tags.main_pool_api import MainPoolApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.AUTH: AuthApi,
        TagValues.MAIN_POOL: MainPoolApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.AUTH: AuthApi,
        TagValues.MAIN_POOL: MainPoolApi,
    }
)
