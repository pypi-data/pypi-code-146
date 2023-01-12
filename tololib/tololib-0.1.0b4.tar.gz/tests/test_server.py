from typing import Any, Optional
from unittest import TestCase

from tololib import ToloServer


class ServerTest(TestCase):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._server: Optional[ToloServer] = None

    def setUp(self) -> None:
        self._server = ToloServer("localhost", 0)
        self._server.start()

    def tearDown(self) -> None:
        if self._server is not None:
            self._server.stop()
            self._server.join()
            self._server = None
