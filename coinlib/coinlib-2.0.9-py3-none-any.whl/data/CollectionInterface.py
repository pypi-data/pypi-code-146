import asyncio
import threading
import random
import string
import aio_pika
import json
import requests
import simplejson as json
from aio_pika import ExchangeType, Message, DeliveryMode

from coinlib import Registrar, helper
from coinlib.feature.FeatureDTO import RabbitInfo


class CollectionInterface:
    def __init__(self, name: str, cdn: str = None, loop = None):
        self.registrar = Registrar()
        self.commandRegistry = []
        self.commandReceived = {}
        if not self.registrar.isLiveEnvironment():
            name = "dev_"+name
        self.name = name
        if cdn is None:
            cdn = "cdn1"
        self.cdn = cdn

        if loop is None:
            loop = asyncio.new_event_loop()
        self.loop = loop

        letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
        self.session_id = ''.join(random.choice(letters) for i in range(28))
        pass

    async def connect(self):
        pass

    def _send_command(self, command: string, params: object = None):

        data_server_target = self.cdn
        url = self.registrar.coinlib_backend_host + "/api/v1/collectionfeatures/" + data_server_target + "/" + command
        message_body = json.dumps(params,
                default=helper.serializeDTO)
        data = requests.post(url, json=params)
        retdata = data.json()

        if retdata["success"]:
            return retdata["data"]

        raise Exception(retdata["error"])

    def logger(self):
        return self.registrar.logger

    def query(self, query):
        data = self._send_command("query", {"collectionName": self.name, "query": query})
        return data

    def len(self):
        result = self._send_command("count", {"collectionName": self.name})
        return result

    def delete(self, query: object):
        result = self._send_command("delete", {"collectionName": self.name, "query": query})
        return result

    def update(self, query: object, data: object):
        result = self._send_command("update", {"collectionName": self.name, "query": query, "data": data})
        return result

    def insert(self, data: [object]):
        result = self._send_command("insert", {"collectionName": self.name, "data": data})
        return result

    def insertOrUpdate(self, query: object, data: object):
        result = self._send_command("insertOrUpdate", {"collectionName": self.name, "query": query, "data": data})
        return result
