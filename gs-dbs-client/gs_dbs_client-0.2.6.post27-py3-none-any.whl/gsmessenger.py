import asyncio
import json
import logging

import socketio
import ujson as ujson
from multiprocessing.dummy import Pool


class GSCNodeFunctionReceiverSocket:
    @classmethod
    def create(cls, sio, gsdbs, oncnodefunction):
        self = GSCNodeFunctionReceiverSocket()
        self.sio = sio
        self.gsdbs = gsdbs
        self._pool = Pool(self.gsdbs.credentials["poolsize"])
        self.oncnodefunction = oncnodefunction
        self._logger = logging.getLogger(__name__)

        @self.sio.event
        def connect():
            self._logger.info('oncnodefunction connected')

        def on_success(r):
            self._logger.info('cnodefunction succeed')

        def on_errorPost(error):
            self._logger.exception('cnodefunction failed :' + error)

        @self.sio.event
        def oncnodefunction(id, msg):
            self._pool.apply_async(self.oncnodefunction, args=[self.gsdbs, id, ujson.loads(msg)], callback=on_success,
                                   error_callback=on_errorPost)
            # self.oncnodefunction(self.gsdbs, id, ujson.loads(msg))

        connectURL = ""

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}&global=true')
        self.sio.wait()

    def sendcnodefunctionResult(self, id, msg):
        self.sio.emit("answer", id, msg)


class GSCNodeFunctionReceiver:
    def __init__(self, gsdbs, oncnodefunction):
        self.sio = socketio.Client()
        self.gsdbs = gsdbs
        self.oncnodefunction = oncnodefunction

    def startSocket(self):
        GSCNodeFunctionReceiverSocket.create(self.sio, self.gsdbs, self.oncnodefunction)

    def sendcnodefunctionanswer(self, id, msg):
        self.sio.emit("answer", {"id": id, "message": ujson.dumps(msg)})


class GSCNodeFunctionCallerSocket:
    @classmethod
    def create(cls, sio, gsdbs, oncnodefunctionanswer):
        self = GSCNodeFunctionCallerSocket()
        self.sio = sio
        self.gsdbs = gsdbs
        self._logger = logging.getLogger(__name__)
        self.oncnodefunctionanswer = oncnodefunctionanswer

        @self.sio.event
        def connect():
            self._logger.info('oncnodefunction connected')

        @self.sio.event
        def answer(id, message):
            self.oncnodefunctionanswer(self.gsdbs, ujson.loads(message))

        connectURL = ""

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}&caller=true')
        self.sio.wait()


class GSCNodeFunctionCaller:
    def __init__(self, gsdbs, oncnodefunctionanswer):
        self.sio = socketio.Client()
        self.gsdbs = gsdbs
        self.oncnodefunctionanswer = oncnodefunctionanswer
        self._pool = Pool(100)
        self._logger = logging.getLogger(__name__)

    def startSocket(self):
        GSCNodeFunctionCallerSocket.create(self.sio, self.gsdbs, self.oncnodefunctionanswer)

    def on_success(self, r):
        self._logger.info('cnodefunction succeed')

    def on_errorPost(self, error):
        self._logger.exception('cnodefunction failed :' + error)

    def emitFunction(self, sio, target, msg):
        sio.emit("oncnodefunction", {"target": target, "message": ujson.dumps(msg)})

    def sendcnodefunction(self, target, msg):
        self._pool.apply_async(self.emitFunction, args=[self.sio, target, msg], callback=self.on_success,
                               error_callback=self.on_errorPost)
