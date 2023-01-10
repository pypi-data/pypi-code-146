import re

from Bubot.Core.BubotHelper import BubotHelper
from Bubot.Helpers.Action import Action
from Bubot.Helpers.ActionDecorator import async_action
from Bubot.Helpers.ExtException import ExtException, Unauthorized, AccessDenied
# from bubot.Helpers.Сryptography.SignedData import SignedData
from aiohttp import web
from aiohttp_session import get_session
from bson.json_util import dumps, loads

from BubotObj.OcfDevice.subtype.WebServer.ApiHelper import WebResponse as Response
from BubotObj.OcfDevice.subtype.WebServer.ApiHelper import json_options
from BubotObj.User.User import User


# from bubot.Catalog.Account.Account import Account


class ApiHandler:
    clear = re.compile('[^a-zA-Z0-9._]')
    api_class_cache = {}

    def __init__(self, request):
        self.session = None
        # self.request = request
        self.storage = request.app['storage']
        self.app = request.app
        self.device = request.app['device']
        self.log = self.device.log

    async def prepare(self, request, device, obj_name, subtype, action, prefix, response_class):
        try:
            api_class = self.get_api_class(device, obj_name, subtype)
        except Exception as err:
            raise ExtException(message='Bad API handler', detail=f'{device}/{obj_name}', parent=err)
        try:
            api_class = api_class(response_class)
        except Exception as err:
            raise ExtException(
                message='Unknown error while initializing API handler',
                detail=f'{device}/{obj_name}',
                parent=err
            )
        api_action = f'{prefix}_{action}'
        self.session = await get_session(request)
        # session_last_visit = self.session.get('last_visit')
        # if session_last_visit and int(time.time()) - session_last_visit > 60 * 60:
        #     self.session['last_visit'] = int(time.time())
        try:
            task = getattr(api_class, api_action)
        except Exception as err:
            raise ExtException(message='API handler not found', detail=f'{device}/{obj_name}/{action}')
        return task(self)

    # async def get_json_data(self):
    #     data = await self.request.text()
    #     if not data:
    #         raise Exception('empty data')
    #     return loads(data)

    def get_api_class(self, device, obj_name, subtype=None):
        uid = device
        if obj_name:
            uid += f'.{obj_name}'
        if subtype:
            uid += f'.{device}'
        try:
            return self.api_class_cache[uid]
        except KeyError:
            pass
        if obj_name:
            try:
                api_class = BubotHelper.get_extension_class(obj_name, device, suffix='Api')
            except:
                if subtype:
                    try:
                        api_class = BubotHelper.get_subtype_class(obj_name, subtype, suffix='Api')
                    except:
                        api_class = BubotHelper.get_obj_class(obj_name, suffix='Api')
                else:
                    api_class = BubotHelper.get_obj_class(obj_name, suffix='Api')
        else:
            api_class = BubotHelper.get_subtype_class('OcfDevice', device, suffix='Api')
        self.api_class_cache[uid] = api_class
        return api_class

    @async_action
    async def check_right(self, **kwargs):
        kwargs['account'] = kwargs['account'] if kwargs.get('account') else self.session['account']
        kwargs['user'] = self.session.get('user')
        if not kwargs['user']:
            raise Unauthorized()
        if not kwargs['account']:
            raise AccessDenied()
        kwargs['storage'] = self.storage
        return await User.check_right(**kwargs)

    @staticmethod
    async def loads_request_data(view):
        data = await view.request.text()
        return loads(data, json_options=json_options) if data else {}

    @staticmethod
    async def loads_json_request_data(view):
        if view.request.method == 'GET':
            return dict(view.request.query)
        else:
            return await view.loads_request_data(view)


class HttpHandler(web.View, ApiHandler):
    prefix_api = 'api'

    def __init__(self, request):
        web.View.__init__(self, request)
        ApiHandler.__init__(self, request)
        # self.storage = request.app['storage']
        # self.app = request.app
        # self.session = None
        # self.data = None
        self.lang = request.headers.get('accept-language')
        pass

    async def get(self):
        return await self.request_handler(self.prefix_api)

    async def post(self):
        async def www_form_decode():
            return dict(await self.request.post())
            pass

        async def json_decode():
            data = await self.request.text()
            return loads(data, json_options=json_options) if data else {}

        data_decoder = {
            'application/x-www-form-urlencoded': www_form_decode,
            'application/json': json_decode
        }
        data_type = self.request.headers.get('content-type')
        if data_type and data_type in data_decoder:
            self.data = await data_decoder[data_type]()

        return await self.request_handler(self.prefix_api)

    async def request_handler(self, prefix, **kwargs):
        _action = Action(name=f'{self.__class__.__name__}.request_handler')
        device = self.request.match_info.get('device')
        obj_name = self.request.match_info.get('obj_name')
        subtype = self.request.match_info.get('subtype')
        action = self.request.match_info.get('action')

        try:
            task = await self.prepare(self.request, device, obj_name, subtype, action, prefix, Response)
            response = _action.add_stat(await task)
            _action.set_end()
            response.headers['stat'] = dumps(_action.stat, ensure_ascii=True)
            return response
        except ExtException as err:
            return Response.json_response(ExtException(
                action=_action.name,
                dump={
                    "device": device,
                    "obj_name": obj_name,
                    "action": action
                },
                parent=err).to_dict(), status=err.http_code)
        except Exception as err:
            return Response.json_response(ExtException(action=_action.name, parent=err).to_dict(), status=500)

    async def notify(self, data):
        return


class PublicHttpHandler(HttpHandler):
    prefix_api = 'public_api'
