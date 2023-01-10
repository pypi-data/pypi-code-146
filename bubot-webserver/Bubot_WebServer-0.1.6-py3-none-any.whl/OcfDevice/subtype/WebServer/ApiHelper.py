from Bubot.Helpers.Helper import get_tzinfo
from aiohttp import web
from bson.json_util import dumps, JSONOptions

json_options = JSONOptions(
    tz_aware=False,
    # tzinfo=get_tzinfo()
)


class DeviceApi:
    def __init__(self, response, **kwargs):
        self.response = response
        self.db = kwargs.get('db')
        self.filter_fields = {}
        self.list_limit = 1000


class WebResponse:

    @staticmethod
    def json_response(data, *, status: int = 200, headers=None, content_type: str = 'application/json',
                      dumps=dumps) -> web.Response:
        text = dumps(data, ensure_ascii=False, json_options=json_options)
        return web.Response(text=text, status=status, headers=headers, content_type=content_type)

    @staticmethod
    def text_response(text='', *, status: int = 200, headers=None) -> web.Response:
        return web.Response(text=text, status=status, headers=headers)


class WsResponse:
    @staticmethod
    def json_response(data):
        return data
