#!/usr/bin/env python3

from asyncio import Queue, sleep
from asyncio import Future

from aiohttp import web
from aiohttp.client_reqrep import ClientRequest
from aiohttp.client_proto import ResponseHandler

jobs = Queue()


class MockConn:
    def __init__(self, protocol):
        self.protocol = protocol

    def release(self):
        pass


class ReverseHttp(ResponseHandler):
    def connection_made(self, transport):
        super().connection_made(transport)

        async def _deque():
            (req, future) = await jobs.get()
            req = ClientRequest(method=req.method, url=req.url, headers=req.headers)

            self.set_response_params()

            resp = await req.send(MockConn(self))
            await resp.start(MockConn(self))
            future.set_result(resp)

        self.task = self._loop.create_task(_deque())

    def connection_lost(self, exc):
        super().connection_lost(exc)
        self.task.cancel()


async def client_handler(request):
    response = Future()
    await jobs.put((request, response))
    resp = await response
    return web.Response(body=resp.content)


async def start_client_server(loop, port):
    runner = web.ServerRunner(web.Server(client_handler))
    await runner.setup()
    await web.TCPSite(runner, port=port).start()

    print("======= Serving clients on http://127.0.0.1:%d/ ======" % port)


async def start_worker_server(loop, port):
    await loop.create_server(lambda: ReverseHttp(loop), port=port)

    print("======= Serving workers on http://127.0.0.1:%d/ ======" % port)


async def main(loop, main_port, worker_port):
    await start_client_server(loop, main_port)
    await start_worker_server(loop, worker_port)

    print("======= Running ======")
    while True:
        await sleep(100 * 3600)


if __name__ == "__main__":
    from logging import basicConfig, DEBUG
    from asyncio import get_event_loop
    from argparse import ArgumentParser

    loop = get_event_loop()
    basicConfig(level=DEBUG)

    parser = ArgumentParser(description="Run PTTH Hub")
    parser.add_argument(
        "--main-port", default=8080, type=int, help="Port for public services"
    )
    parser.add_argument(
        "--worker-port",
        default=4040,
        type=int,
        help="Port where workers should connect",
    )
    args = parser.parse_args()

    try:
        loop.run_until_complete(main(loop, args.main_port, args.worker_port))
    except KeyboardInterrupt:
        pass
    loop.close()
