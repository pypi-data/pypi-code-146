#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from roc.rpl.packet_structure.data import Data


class TestRPLExtraction(unittest.TestCase):
    """
    To test the parameter extraction from bytearray.
    """

    def setUp(self):
        """
        Create the bytearray from where to read the data and store it.
        """
        # keep a reference, since it is C pointer inside Data
        self.byte_data = bytes(bytearray.fromhex("{:x}".format(4194967196)))

        # create data object
        self.data = Data(self.byte_data, len(self.byte_data))

    def test_unsigned_char(self):
        """
        Test the conversion for unsigned char at different positions.
        """
        self.assertEqual(
            self.data.u8p(0, 0, 8),
            250,
        )
        self.assertEqual(
            self.data.u8p(1, 0, 8),
            10,
        )
        self.assertEqual(
            self.data.u8p(2, 0, 8),
            30,
        )
        self.assertEqual(
            self.data.u8p(3, 0, 8),
            156,
        )
        self.assertEqual(
            self.data.u8p(2, 5, 6),
            52,
        )

    def test_unsigned_short(self):
        """
        Test the conversion for unsigned short at different positions.
        """
        self.assertEqual(
            self.data.u16p(0, 0, 16),
            64010,
        )
        self.assertEqual(
            self.data.u16p(2, 0, 16),
            7836,
        )
        self.assertEqual(
            self.data.u16p(1, 5, 6),
            16,
        )

    def test_unsigned_long(self):
        """
        Test the conversion for unsigned long at different positions.
        """
        self.assertEqual(
            self.data.u32p(0, 0, 32),
            4194967196,
        )

    def test_signed_short(self):
        self.assertEqual(
            self.data.i16p(0, 0, 16),
            -1526,
        )

    def test_signed_long(self):
        """
        Test read as signed long.
        """
        self.assertEqual(
            self.data.i32p(0, 0, 32),
            -100000100,
        )

    def test_signed_char(self):
        """
        Test the conversion for signed char at different positions.
        """
        self.assertEqual(
            self.data.i8p(0, 0, 8),
            -6,
        )
        self.assertEqual(
            self.data.i8p(1, 0, 8),
            10,
        )
        self.assertEqual(
            self.data.i8p(2, 0, 8),
            30,
        )
        self.assertEqual(
            self.data.i8p(3, 0, 8),
            -100,
        )
        self.assertEqual(
            self.data.i8p(2, 5, 6),
            52,
        )

    def test_float_float(self):
        """
        Test the value read for floats.
        """
        self.assertAlmostEqual(
            self.data.f32p(0, 0, 32),
            -1.79289449589817e+35,
        )
