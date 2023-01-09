import json

from aio_pika import ExchangeType

from coinlib import log
from coinlib.feature.CoinlibFeature import CoinlibFeature
from abc import abstractmethod
import asyncio
import aio_pika

from coinlib.feature.FeatureDTO import FeatureData, ProcessResponse, FeatureLakeData


class CoinlibFeatureLake(CoinlibFeature):

    async def start_run_process(self):
        return await self.run_process()

    async def run_process(self):
        try:
            loop = asyncio.get_event_loop()
            connection = await aio_pika.connect_robust(
                "amqp://"+self.rabbit_info.user+":"+self.rabbit_info.pwd+"@"+self.rabbit_info.ip+":"+self.rabbit_info.port+"/", loop=loop
            )

            async with connection:
                queue_name = "datastream"

                # Creating channel
                self.channel = await connection.channel()  # type: aio_pika.Channel

                # Declaring queue
                exchange = await self.channel.get_exchange(
                    queue_name
                )
                routing_key = self.registrar.environment+"_"+self.session_id
                queue = await self.channel.declare_queue(auto_delete=True)
                await queue.bind(exchange, routing_key=routing_key)
                async with queue.iterator() as queue_iter:
                    # Cancel consuming after __aexit__
                    async for message in queue_iter:
                        async with message.process():
                            try:
                                message_raw = json.loads(message.body)
                                message_data = json.loads(message_raw["data"])
                                await self.data_received(message_data)
                            except Exception as e:
                                self.logger().error("Can not connect to registry %s", str(e))
                                pass

        except Exception as e:
            self.logger().error("Can not connect to registry %s", str(e))
            return False

        return True

    def stop(self):
        self.channel.close()
        super().stop()

    @abstractmethod
    async def data_received(self, data: FeatureLakeData) -> ProcessResponse:
        pass
