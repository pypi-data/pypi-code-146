import asyncio
import pika
import aio_pika
from pydantic import BaseModel
import functools
import json

class Msg(BaseModel):
     msg:str

class FlowiaRmq:
     _channel = None
     _connection= None

     async def connect(self , url): 
          self._connection = await aio_pika.connect_robust(url)
          self._channel = await self._connection.channel()

     async def channel_declare(self , topic_name):
         await self._channel.declare_exchange(topic_name , 'fanout')
 
     async def publish(self ,topic_name , message , event ):
          exchange = await self._channel.declare_exchange(topic_name, type="fanout")
          await exchange.publish(
               aio_pika.Message(
               bytes(json.dumps(message.dict()) , "utf-8"),
               content_type="application/json",
               headers={"event":event}
               ),routing_key="")

     async def  subscribe(self ,topic_name ,callback, events=[] ) :
          queue = await self._channel.declare_queue('', auto_delete=True)
          queue_name = queue.name
          await queue.bind(topic_name , queue_name)
          cb = functools.partial(self.process_message, events=events , callback=callback)
          await queue.consume(cb)

     async def process_message(self , message: aio_pika.abc.AbstractIncomingMessage , events: list[str] , callback ) -> None:
        async with message.process():
          event = message.headers.get("event") 
          if (events.__contains__(event)):
              await callback(json.loads(message.body.decode("utf-8")))
