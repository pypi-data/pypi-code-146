import unittest
from colorise_terminal import cprint


class TestValidArguments(unittest.TestCase):
    def test_hex_length_text_color(self):
        with self.assertRaises(ValueError):
            cprint("Test", text_color="#FFFFFFF")

    def test_hex_length_bg_color(self):
        with self.assertRaises(ValueError):
            cprint("Test", bg_color="#FFFFFFF")

    def test_hex_format_text_color(self):
        with self.assertRaises(ValueError):
            cprint("Test", text_color="#AABBHH")

    def test_hex_format_bg_color(self):
        with self.assertRaises(ValueError):
            cprint("Test", bg_color="#AABBHH")

    def test_rgb_format_text_color(self):
        with self.assertRaises(ValueError):
            cprint("Test", text_color=(-1, 2, 2))

    def test_rgb_format_bg_color(self):
        with self.assertRaises(ValueError):
            cprint("Test", bg_color=(-1, 2, 2))


if __name__ == "__main__":
    unittest.main()
