'''Assetto Corsa Websocket handlers'''

import asyncio
import logging
import websockets

from ac_websocket_server.error import WebsocketsServerError

_logger = logging.getLogger('ac-ws.ws-handlers')


async def consumer_handler(websocket, consumer):
    '''Consumer messages from websocket and pass to user function'''
    try:
        async for message in websocket:
            await consumer(message)
    except websockets.exceptions.ConnectionClosed:
        _logger.info("connection closed")
    except Exception as error:
        print(error)
        raise


async def handler(websocket, consumer, producer):
    '''Setup consumer and producer handlers.'''

    consumer_task = asyncio.create_task(consumer_handler(websocket, consumer))
    producer_task = asyncio.create_task(producer_handler(websocket, producer))
    _done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


async def producer_handler(websocket, producer):
    '''Send user producer output to websocket'''
    # pylint: disable=broad-except
    while True:
        try:
            await websocket.send(await producer())
        except websockets.exceptions.ConnectionClosed as error:
            print(error)
            raise WebsocketsServerError(error) from error
        except Exception as error:
            print(error)
            raise
