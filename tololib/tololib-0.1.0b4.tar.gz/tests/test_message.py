from unittest import TestCase

from tololib import Message


class MessageTest(TestCase):
    def test_init(self) -> None:
        pass  # TODO write tests

    def test_generate_crc(self) -> None:
        self.assertEqual(Message.generate_crc(b"\xaa\xaaa\x00\xffUU"), 0x9E)

        self.assertNotEqual(Message.generate_crc(b"\xaa\xaaa\x00\xffUU"), 0)

    def test_validate_crc(self) -> None:
        self.assertTrue(Message.validate_crc(b"\xaa\xaaa\x00\xffUU\x9e"))

        self.assertFalse(Message.validate_crc(b"\xaa\xaaa\x00\xffUU\x00"))

    def test_validate_meta(self) -> None:
        self.assertTrue(Message.validate_meta(b"\xaa\xaaa\x00\xffUU\x9e"))
        self.assertTrue(Message.validate_meta(b"\xaa\xaaFOOBAR\xffUU\xe8"))

        self.assertFalse(Message.validate_meta(b"\xaa\xaaa\x00\xffUU\x00"))
        self.assertFalse(Message.validate_meta(b"\xaaa\x00\xffU\x9e"))

    def test_to_bytes(self) -> None:
        pass  # TODO write tests
