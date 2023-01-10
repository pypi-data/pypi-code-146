# from bubot.Client.OcfDevice.OcfDevice import OcfDevice
import asyncio
import json
import os.path
from uuid import uuid4

# from bubot.Catalog.Client.WebServer import API
from Bubot.Core.DataBase.Mongo import Mongo as Storage
# from bubot.Core.DataBase.SqlLite import SqlLite as Storage
from Bubot.Core.FastStorage.Simple import SimpleFastStorage as FastStorage
from Bubot.Helpers.ActionDecorator import async_action
from Bubot.Helpers.ExtException import ExtException, ResourceNotAvailable
from Bubot.Helpers.Helper import Helper
from Bubot.Ocf.Helper import find_drivers
from BubotObj.OcfDevice.subtype.Device.Device import Device
from BubotObj.OcfDevice.subtype.Device.QueueMixin import QueueMixin
from BubotObj.OcfDevice.subtype.VirtualServer.VirtualServer import VirtualServer
from BubotObj.OcfDevice.subtype.WebServer.FormHandler import FormHandler
# import logging
from BubotObj.OcfDevice.subtype.WebServer.HttpHandler import HttpHandler, PublicHttpHandler
from BubotObj.OcfDevice.subtype.WebServer.SessionStorageApp import SessionStorageApp
from BubotObj.OcfDevice.subtype.WebServer.SessionStorageMongo import SessionStorageMongo
from BubotObj.OcfDevice.subtype.WebServer.WsHandler import WsHandler
from aiohttp import web
from aiohttp_session import get_session, setup

from .__init__ import __version__ as device_version


# from bson import ObjectId


# _logger = logging.getLogger(__name__)


class WebServer(VirtualServer, QueueMixin):
    version = device_version
    file = __file__
    template = False
    forms = dict()

    def __init__(self, **kwargs):
        # self.drivers = []
        # self.resources = []
        # self.cache_schemas = {}
        self.schemas_dir = []
        self.net_devices = {}
        self.request_queue = asyncio.Queue()
        self.serial_queue_worker = None
        self.ws = {}
        self.runner = None
        self.storage = None
        VirtualServer.__init__(self, **kwargs)

    async def on_pending(self):
        # self.serial_queue_worker = asyncio.ensure_future(self.queue_worker(self.request_queue, 'request_queue'))
        await self.run_web_server()
        await super().on_pending()

    async def on_cancelled(self):
        if self.storage:
            await self.storage.close()
        if self.runner is not None:
            await self.runner.cleanup()
        await super().on_cancelled()

    @async_action
    async def run_web_server(self, *, _action):

        # self = cls.init_from_file(**kwargs)
        # self.save_config()
        # self.log.info(f'{self.__class__.__name__} start up')
        app = web.Application(
            # middlewares=[
            #     self.middleware_auth,
            #     self.middleware_index
            # ]
        )
        app['device'] = self
        app['sessions'] = {}
        app['fast_storage'] = FastStorage()
        self.storage = await Storage.connect(self)
        app['storage'] = self.storage
        app.middlewares.append(self.middleware_index)
        _session_storage = self.get_session_storage(app, self.get_param('/oic/con', 'session_storage', 'App'))
        setup(app, _session_storage)
        app.middlewares.append(self.middleware_auth)
        drivers = find_drivers(log=self.log)
        self.set_param('/oic/mnt', 'drivers', drivers)
        self.build_i18n(drivers)
        self.add_routes(app)
        port = self.get_param('/oic/con', 'port', 8080)
        # app.on_startup.append(self.start_background_tasks)
        # app.on_cleanup.append(self.cleanup_background_tasks)
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, None, port)
        await site.start()
        self.log.info(f'{self.__class__.__name__} started up http://localhost:{port}')
        return app
        # web.run_app(app, port=port)

    @staticmethod
    async def start_background_tasks(app):
        pass
        # self = app['device']
        # app['device_task'] = asyncio.create_task(VirtualServer.main(self))

    @staticmethod
    async def cleanup_background_tasks(app):
        # if not app['main'].done():
        #     app['main'].cancel()
        #     await app['main']
        # if not app['broker'].done():
        #     app['broker'].cancel()
        #     await app['broker']
        pass

    def build_i18n(self, drivers):
        locales = {
            'en': {},
            'ru': {},
            'cn': {}
        }
        self.log.info('begin')
        for elem in drivers:
            _path = os.path.normpath(f'{drivers[elem]["path"]}/i18n')
            if not os.path.isdir(_path):
                continue
            for locale in locales:
                locale_path = os.path.normpath(f'{drivers[elem]["path"]}/i18n/{locale}.json')
                if not os.path.isfile(locale_path):
                    continue
                with open(locale_path, "r", encoding='utf-8') as file:
                    try:
                        _data = json.load(file)
                        if isinstance(_data, dict):
                            Helper.update_dict(locales[locale], _data)
                        else:
                            self.log.error(f'Build locale {locale} for driver {elem}: Bad format {_data}')
                    except Exception as err:
                        err = ExtException(parent=err)
                        self.log.error(f'Build locale {locale} for driver {elem}: {str(err)}')

        i18n_dir = os.path.normpath(f'{self.path}/i18n')
        try:
            os.mkdir(i18n_dir)
        except FileExistsError:
            pass
        except Exception as err:
            raise ResourceNotAvailable(detail=f'{err} - {i18n_dir}', parent=err)
        for locale in locales:
            build_path = os.path.normpath(f'{i18n_dir}/{locale}.json')
            with open(build_path, "w", encoding='utf-8') as file:
                try:
                    json.dump(locales[locale], file, ensure_ascii=False)
                except Exception as err:
                    self.log.error(f'Build locale {locale}: {str(err)}')

        self.log.info('build i18n complete')

    def add_routes(self, app):
        self.log.info('add routes')
        for elem in self.get_param('/oic/mnt', 'drivers'):
            try:
                ui_view: Device = self.get_device_class(elem)(path=self.path)
                ui_view.add_route(app)  # todo сделать разводящую из всех доступных
            except NotImplementedError:
                pass
            except Exception as e:
                err = ExtException(parent=e)
                self.log.error(f'Error import_ui_handlers({elem}): {err}')
        # for elem in app.router.routes():
        #     print(elem)
        pass

    def add_route(self, app):
        app.router.add_route('get', '/{device}/ws', WsHandler)
        app.router.add_route('*', '/{device}/api/{action}', HttpHandler)
        app.router.add_route('*', '/{device}/api/{obj_name}/{action}', HttpHandler)
        app.router.add_route('*', '/{device}/api/{obj_name}/{subtype}/{action}', HttpHandler)
        app.router.add_route('*', '/{device}/public_api/{action}', PublicHttpHandler)
        app.router.add_route('*', '/{device}/public_api/{obj_name}/{action}', PublicHttpHandler)
        app.router.add_route('*', '/{device}/public_api/{obj_name}/{subtype}/{action}', PublicHttpHandler)
        app.router.add_route('get', '/{device}/form/{obj_name}/{form_name}', FormHandler)
        app.router.add_route('get', '/{device}/form/{obj_name}/{subtype}/{form_name}', FormHandler)
        pass

    @staticmethod
    @web.middleware
    async def middleware_auth(request, handler):
        if handler in [HttpHandler, WsHandler]:
            try:
                session = await get_session(request)
            except Exception as err:
                raise err
            if session.get("user"):
                return await handler(request)
            else:
                raise web.HTTPUnauthorized()
        return await handler(request)

    @staticmethod
    @web.middleware
    async def middleware_index(request, handler, index='index.html'):
        # """Handler to serve index files (index.html) for static directories.
        #
        # :type request: aiohttp.web.Request
        # :returns: The result of the next handler in the chain.
        # :rtype: aiohttp.web.Response
        # """

        try:

            filename = request.match_info['filename']
            if not filename or filename.endswith('/'):
                filename = index
            request.match_info['filename'] = filename
        except KeyError:
            pass
        return await handler(request)

    # def get_schema_by_rt(self, rt):
    #     json_schema = JsonSchema4(cache=self.cache_schemas, dir=self.schemas_dir)
    #     return json_schema.load_from_rt(rt)

    async def on_notify_response(self, message, answer):
        try:
            self.log.debug('{0} receive notify {1} {2}'.format(
                self.__class__.__name__, message.to.di, message.to.href))
            for elem in self.ws:
                data = message.to_dict()
                await self.ws[elem].ws.send_json(data)
        except Exception as err:
            self.log.error('on_notify_response: {}'.format(err))

    @staticmethod
    def get_session_storage(app, name):

        def get_app_session_storage():
            return SessionStorageApp(
                app,
                httponly=False,
                key_factory=lambda: str(uuid4()),
                cookie_name="session",
                # encoder=cookie_encoder, decoder=cookie_decoder
            )

        def get_mongo_session_storage():
            return SessionStorageMongo(
                app,
                httponly=False,
                key_factory=lambda: str(uuid4()),
                cookie_name="session",
                # encoder=cookie_encoder, decoder=cookie_decoder
            )

        available = {
            'App': get_app_session_storage,
            'Mongo': get_mongo_session_storage
        }
        return available[name]()
