'''Assetto Corsa Websocket Server'''

import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger('ac-ws')

logging.getLogger("asyncio").setLevel(logging.DEBUG)
