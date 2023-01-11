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
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.feature.FeatureDTO import RabbitInfo


class EventConsumer:
    def __init__(self, basicJob: WorkerJobProcess):
        self.rabbit_info = RabbitInfo()
        self.basicJob = basicJob
        self.queue = None
        self.registrar = Registrar()
        self.pre_registered = []
        _thread = threading.Thread(target=self.startMQWorkerThread, args=())
        _thread.start()

        pass

    def consume(self, event: str):
        if not self.registrar.isLiveEnvironment():
            event = event+"_dev"
        if self.queue is not None:
            self.listener_loop.run_until_complete(self.queue.bind("event_manager", routing_key=event))
        else:
            self.pre_registered.append(event)

    def logger(self):
        return self.registrar.logger

    def startMQWorkerThread(self):
        self.listener_loop = asyncio.new_event_loop()
        self.listener_loop.run_until_complete(self.startMQWorker())

    async def startMQWorker(self):

        connection = await aio_pika.connect_robust(
            "amqp://" + self.rabbit_info.user + ":" + self.rabbit_info.pwd + "@" + self.rabbit_info.ip + ":" + self.rabbit_info.port + "/",
            loop=self.listener_loop
            )

        # Creating channel
        self.channel = await connection.channel()  # type: aio_pika.Channel

        # Declaring queue
        await self.channel.declare_exchange(
            "event_manager".lower(),
            ExchangeType.TOPIC,
            durable=True,
        )

        self.queue = await self.channel.declare_queue(auto_delete=True)

        for p in self.pre_registered:

            await self.queue.bind("event_manager", routing_key=p)

        async with self.queue.iterator() as queue_iter:
            try:
                # Cancel consuming after __aexit__
                async for message in queue_iter:
                    async with message.process():
                        try:
                            message_raw = json.loads(message.body)
                            self._on_event_receive('newICOCoinDetected_dev', message_raw)
                        except Exception as e:
                            self.logger().error(e)
                            pass
            except Exception as e:
                print(e)
                pass
        return True

    def _on_event_receive(self, routing_key, message):
        self.basicJob.onEventCallback(routing_key, message)
