from unittest import TestCase

import tololib


class InitTest(TestCase):
    def test_init(self) -> None:
        self.assertIn("Command", tololib.__all__)
        self.assertIn("ToloClient", tololib.__all__)
        self.assertIn("ToloServer", tololib.__all__)
