from BubotObj.OcfDevice.subtype.WebServer.HttpHandler import HttpHandler, ApiHandler
from aiohttp import web, WSMsgType
from bson.json_util import dumps, loads
from Bubot.Helpers.ExtException import ExtException, CancelOperation
import asyncio
from uuid import uuid4
import json
from BubotObj.OcfDevice.subtype.WebServer.ApiHelper import WsResponse as Response, json_options
import re
from datetime import datetime
from Bubot.Helpers.Action import Action


class WsHandler(HttpHandler):
    clear = re.compile('[^a-zA-Z0-9._]')

    def __init__(self, request):
        super().__init__(request)
        self.ws_uid = str(uuid4())
        self.ws = None

    async def get(self):
        self.ws = web.WebSocketResponse()
        await self.ws.prepare(self.request)
        try:

            self.log.debug('websocket connection open ', self.ws_uid)
            self.device.ws[self.ws_uid] = {
                "ws": self.ws,
                "begin": datetime.now(),
                "last": datetime.now(),
                "task": {}
            }

            async for msg in self.ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        self.device.ws[self.ws_uid]['last'] = datetime.now()
                        msg = WsView.loads(self, msg.data)
                    except Exception as err:
                        # self.log.warning()
                        await self.ws.send_json({
                            "type": "error",
                            "data": ExtException(f"Bad ws msg {msg.data}").to_dict()
                        })
                        continue
                    try:
                        await getattr(self, f"{msg.type}_handler")(msg)
                    except CancelOperation:
                        await self.ws.send_json({
                            "type": "cancel",
                            "uid": msg.uid,
                        })
                    except ExtException as err:
                        await self.ws.send_json({
                            "type": "error",
                            "uid": msg.uid,
                            "data": err.to_dict()
                        })
                    except Exception as err:
                        await self.ws.send_json({
                            "type": "error",
                            "uid": msg.uid,
                            "data": ExtException(parent=err).to_dict()
                        })
                        continue

                elif msg.type == WSMsgType.ERROR:
                    print('ws connection closed with exception %s' %
                          self.ws.exception())
        finally:
            if not self.ws.closed:
                self.log.debug('ws connection closed {}'.format(self.ws_uid))
                await self.ws.close()
            for msg_uid in self.device.ws[self.ws_uid]['task']:
                try:
                    self.device.ws[self.ws_uid]['task'][msg_uid].cancel()
                except KeyError:
                    pass
            del self.device.ws[self.ws_uid]
            return self.ws

    async def post(self):
        raise NotImplementedError()

    async def call_handler(self, msg):
        try:
            device, obj_name, action = msg.name.split('/')
        except ValueError:
            raise ExtException(action='call_handler', message='Bad format message', detail=msg.name)
        try:
            task = await msg.prepare(self.request, device, obj_name, action, 'api', Response)
            self.device.ws[self.ws_uid]['task'][msg.uid] = asyncio.create_task(
                msg.call_handler(task)
            )
        except ExtException as err:
            raise ExtException(action='call_handler', parent=err)
        except Exception as err:
            raise ExtException(action='call_handler', parent=err)

    async def cancel_handler(self, msg):
        try:
            task = self.device.ws[self.ws_uid]['task'][msg.uid]
            task.cancel()
        except KeyError:
            raise ExtException(action='cancel_handler', message='Task not found', detail=msg.name)


class WsView(ApiHandler):
    def __init__(self, view):
        self.request = view.request
        ApiHandler.__init__(self, view.request)
        self.ws = view.ws
        self.ws_uid = view.ws_uid
        self.data = None
        self.task = None
        # self.uid = view.uid
        # self.data = None
        # self.executor = None
        self.notificator = None
        self.arrival = None
        # self.begin = None
        # self.end = None
        # self.stat = {}
        # self.session = {}

    @classmethod
    def loads(cls, ws_handler, data):
        self = cls(ws_handler)
        self.data = loads(data, json_options=json_options)
        return self

    @property
    def uid(self):
        return self.data.get('uid')

    @property
    def type(self):
        return self.data.get('type')

    @property
    def name(self):
        return self.data.get('name')

    async def notify(self, data):
        await self.ws.send_json({
            "type": "notify",
            "uid": self.uid,
            "data": data
        })

    async def call_handler(self, task):
        _action = Action(name='request_handler')
        try:
            res = _action.add_stat(await task)
            _action.set_end()
            await self.ws.send_json({
                "type": "success",
                "uid": self.uid,
                "data": res,
                "stat": _action.stat
            })
        except CancelOperation:
            await self.ws.send_json({
                "type": "cancel",
                "uid": self.uid,
            })
        except ExtException as err:
            await self.ws.send_json({
                "type": "error",
                "uid": self.uid,
                "data": err.to_dict()
            })
        except Exception as err:
            await self.ws.send_json({
                "type": "error",
                "uid": self.uid,
                "data": ExtException(parent=err).to_dict()
            })
        finally:
            try:
                del self.device.ws[self.ws_uid]['task'][self.uid]  # удаляем task
            except KeyError:
                pass

    @staticmethod
    async def loads_request_data(view):
        return view.data['data']

    @staticmethod
    async def loads_json_request_data(view):
        return view.data['data']
