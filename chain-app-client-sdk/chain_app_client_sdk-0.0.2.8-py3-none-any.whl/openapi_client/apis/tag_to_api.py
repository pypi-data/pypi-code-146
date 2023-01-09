import typing_extensions

from openapi_client.apis.tags import TagValues
from openapi_client.apis.tags.main_pool_api import MainPoolApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.MAIN_POOL: MainPoolApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.MAIN_POOL: MainPoolApi,
    }
)
