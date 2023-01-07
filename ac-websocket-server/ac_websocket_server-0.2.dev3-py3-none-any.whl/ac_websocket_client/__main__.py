#!/usr/bin/env python

'''Assetto Corsa Websockets tkintr Client.

Opens a connection to a websocket server and enters an interactive loop to send/echo.

Reference: https://stackoverflow.com/questions/47895765/use-asyncio-and-tkinter-or-another-gui-lib-together-without-freezing-the-gui

'''

import argparse
import asyncio
import logging
import sys

from ac_websocket_client import DEBUG
from ac_websocket_client.app import App
from ac_websocket_server.constants import HOST, PORT


async def main(args):
    '''Parse command line arguments and start App'''

    parser = argparse.ArgumentParser(prog='client.py',
                                     description='A web-sockets test client.')

    parser.add_argument("--host",
                        type=str, default=HOST,
                        help="host to connect/listen")

    parser.add_argument("--port",
                        type=int, default=PORT,
                        help="port to connect/listen")

    parser.add_argument("--verbose",
                        action="store_true",
                        help="show verbose output")

    options = parser.parse_args(args)

    url = f'ws://{options.host}:{str(options.port)}'

    loop = asyncio.get_event_loop()

    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)

    app = App(loop, url)
    await app.start_ui()


if __name__ == '__main__':

    try:
        asyncio.run(main(sys.argv[1:]))
    except RuntimeError:
        pass
