from unittest import TestCase

from tololib import Command


class CommandTest(TestCase):
    def test_from_code(self) -> None:
        self.assertRaises(ValueError, Command.from_code, 255)
