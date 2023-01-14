import asyncio
import threading
import random
import string
import aio_pika
import simplejson as json
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from aio_pika import ExchangeType, Message, DeliveryMode

from coinlib import Registrar, helper
from coinlib.BasicJob import BasicJob
from coinlib.feature.FeatureDTO import RabbitInfo


class EventInterface:
    def __init__(self, basicJob: BasicJob):
        self.basicJob = basicJob
        self.registrar = Registrar()
        pass


    def fire(self, eventName: str, params: object = None):
        stub = self.basicJob.getStub()
        fireEventRequest = statsModel.EventRequest()
        fireEventRequest.event = eventName
        fireEventRequest.stage = self.registrar.environment
        fireEventRequest.params = json.dumps(params, ignore_nan=True)
        stub.FireEvent(fireEventRequest)