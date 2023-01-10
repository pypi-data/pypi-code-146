import json
import aio_pika
from scan.common import logger
from json import JSONDecodeError


class RabbitMQ:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host') or 'localhost'
        self.port = kwargs.get('port') or 5672
        self.user = kwargs.get('user') or 'root'
        self.password = kwargs.get('password') or 'root'
        self.virtualhost = kwargs.get('virtualhost') or '/'
        self.loop = None
        self.max_pool_size = 1
        self.connection = None

    async def init(self, max_pool_size=None):
        if max_pool_size and isinstance(max_pool_size, int):
            self.max_pool_size = max_pool_size
        await self.get_connection()

    async def get_connection(self):
        if self.connection:
            try:
                await self.connection.close()
            except:
                pass
        self.connection = await aio_pika.connect_robust(host=self.host, port=int(self.port), login=self.user,
                                                        password=self.password, virtualhost=self.virtualhost)

    async def get_channel(self):
        for _ in range(3):
            try:
                if not self.connection:
                    await self.get_connection()
                channel = await self.connection.channel()
                return channel
            except Exception as e:
                logger.error(f'get channel error:{e}')
                self.connection = None

    async def consume(self, call_back,  queue_name, no_ack=False, durable=True, auto_delete=False, arguments=None, qos=1):
        """
        :param call_back: 回调函数
        :param qos:
        :param auto_delete:
        :param durable:
        :param no_ack:
        :param arguments: mq绑定参数
        :param queue_name: 队列名
        :return:
        """
        try:
            channel = await self.get_channel()
            async with channel:
                await channel.set_qos(qos)
                queue = await channel.declare_queue(queue_name, durable=durable, arguments=arguments,
                                                    auto_delete=auto_delete)
                async with queue.iterator(no_ack=no_ack) as queue_iter:
                    async for message in queue_iter:
                        body = message.body
                        try:
                            task_info = json.loads(body.decode())
                        except JSONDecodeError:
                            logger.error(f'Description Failed to format task data:{body}')
                            await message.ack()
                            continue
                        try:
                            pres = await call_back(task_info)
                        except Exception as e:
                            logger.error(f'consume error:{e}')
                        if pres:
                            await message.ack()
                        else:
                            logger.error(f'task fail, resend data:{task_info}')
                            await self.publish(data=task_info, routing_key=queue_name)
                            await message.ack()
        except Exception as e:
            logger.error(f'consume process error: {e}')

    async def publish(self, data, routing_key, priority=None):
        """
        :param priority: 消息优先级
        :param data: 要发送的数据
        :param routing_key: 队列名
        :return:
        """
        try:
            channel = await self.get_channel()
            async with channel:
                data = json.dumps(data)
                for _ in range(3):
                    try:
                        await channel.default_exchange.publish(aio_pika.Message(body=data.encode(), priority=priority),
                                                               routing_key=routing_key)
                        return True
                    except Exception as e:
                        logger.error(f'publish error: {e}')
        except Exception as e:
            logger.error(f'publish process error: {e}')

    async def purge(self, queue_name, arguments=None):
        """
        :param arguments: 绑定队列参数
        :param queue_name: 要清空的队列名
        :return:
        """
        try:
            channel = await self.get_channel()
            async with channel:
                try:
                    queue = await channel.declare_queue(queue_name, durable=True, arguments=arguments,
                                                        auto_delete=False)
                    await queue.purge()
                    return True
                except Exception as e:
                    logger.error(f'purge error: {e}')
        except Exception as e:
            logger.error(f'purge process error: {e}')

    async def message_count(self, queue_name, arguments=None):
        try:
            channel = await self.get_channel()
            async with channel:
                try:
                    queue = await channel.declare_queue(queue_name, durable=True, arguments=arguments,
                                                        auto_delete=False)
                    count = queue.declaration_result.message_count
                    return count
                except Exception as e:
                    logger.error(f'message_count error: {e}')
        except Exception as e:
            logger.error(f'message_count process error: {e}')


__all__ = RabbitMQ








