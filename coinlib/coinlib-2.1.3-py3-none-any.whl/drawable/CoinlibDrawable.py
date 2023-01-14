import asyncio
import threading

import aio_pika
from aio_pika import IncomingMessage
from chipmunkdb.ChipmunkDb import ChipmunkDb

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import simplejson as json

from coinlib import helper
from coinlib.feature.FeatureDTO import RabbitInfo
from coinlib.helper import is_in_ipynb, serializeDTO
import ipynb_path
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
import grpc
import inspect
from coinlib.Registrar import Registrar
import aio_pika
import simplejson as json
from aio_pika import connect, Message, DeliveryMode, ExchangeType
import asyncio
import datetime
import threading
import time
from typing import List

class CoinlibDrawable:

    def __init__(self, manager, worker):
        self.manager = manager
        self._list = []
        self.rabbit_info = RabbitInfo()
        self.worker = worker
        self._sendLogQueueRunning = False

        self._lastTimeLogQueueWasRunning = 0
        pass

    def runNextLogQueue(self):

        threading.Thread(target=self.send_worker_data_to_queue_sync, args=[], daemon=True).start()

        return True


    def plot(self, plot_fig, window="drawable1"):

        jsondata = json.dumps(plot_fig, default=serializeDTO)


        plot = {
            "name": window,
            "data": json.loads(jsondata)
        }
        self._list.append(plot)
        self.runNextLogQueue()

        return True

    def send_worker_data_to_queue_sync(self, force=False):

        timeDistanceInSeconds = time.time() - self._lastTimeLogQueueWasRunning
        if force or (not self._sendLogQueueRunning and timeDistanceInSeconds > 5):
            self._lastTimeLogQueueWasRunning = time.time()

            self.manager.loop.run_until_complete(self.send_worker_data_to_queue())

        return True

    async def send_worker_data_to_queue(self):
        self._sendLogQueueRunning = True
        message_log_queue = self._list.copy()
        self._list.clear()
        try:
            connection = await aio_pika.connect_robust(
                "amqp://" + self.rabbit_info.user + ":" + self.rabbit_info.pwd + "@" + self.rabbit_info.ip + ":" + self.rabbit_info.port + "/",
                loop=self.manager.loop
            )

            async with connection:
                # Creating channel
                channel = await connection.channel()

                queue = await channel.declare_queue(
                    "save_logic_plotly_data",
                    durable=True
                )

                message_body = json.dumps({"data_plots": message_log_queue, "activityId": self.manager.getAppWorkerActivityIdentifier(),
                                           "createdAt": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ"),
                                           "applicationId": self.manager.getAppWorkerIdentifier()},
                                            default=helper.serializeDTO)

                message = Message(
                    str.encode(message_body),
                    delivery_mode=DeliveryMode.PERSISTENT
                )

                # Sending the message
                await channel.default_exchange.publish(
                    message, routing_key="save_logic_plotly_data"
                )

                await connection.close()

        except Exception as e:
            print(e)
            pass

            self._sendLogQueueRunning = False
