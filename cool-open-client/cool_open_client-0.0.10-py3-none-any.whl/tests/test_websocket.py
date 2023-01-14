import unittest
import logging
import sys
from time import sleep
import asyncio
from cool_open_client.cool_automation_client import CoolAutomationClient



class TestWebSocket(unittest.TestCase):
    def setUp(self):
        self._LOGGER = logging.getLogger(__package__)
        self._LOGGER.addHandler(logging.StreamHandler(sys.stdout))
        self._LOGGER.setLevel(logging.DEBUG)

        with open("token.txt") as token_file:
            self.token = token_file.read()
        self.loop = asyncio.get_event_loop()

    def test_websocket(self):
        client = self.loop.run_until_complete(CoolAutomationClient.create(self.token, self._LOGGER))
        client.open_socket()
        sleep(120)
        # self.loop.run_until_complete(task)


if __name__ == "__main__":
    unittest.main()
