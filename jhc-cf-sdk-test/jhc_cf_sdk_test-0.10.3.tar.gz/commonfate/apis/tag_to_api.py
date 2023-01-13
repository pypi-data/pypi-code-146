import typing_extensions

from commonfate.apis.tags import TagValues
from commonfate.apis.tags.end_user_api import EndUserApi
from commonfate.apis.tags.admin_api import AdminApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.END_USER: EndUserApi,
        TagValues.ADMIN: AdminApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.END_USER: EndUserApi,
        TagValues.ADMIN: AdminApi,
    }
)
