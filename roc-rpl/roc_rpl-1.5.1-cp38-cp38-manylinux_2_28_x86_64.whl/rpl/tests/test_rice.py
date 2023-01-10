#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path as osp
import struct
import unittest

from roc.rpl.packet_structure.data import Data
from roc.rpl.rice.rice import Compressor


class TestRICE(unittest.TestCase):
    """
    To test the algorithm of the compression and decompression of data.
    """

    def setUp(self):
        """
        Create the list of data to compress and decompress for tests.
        """
        self.data = [
            [
                0, 0, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
            ],
            [
                2, 4, 89, 233,
                3, 34, 4, 8,
                2, 4, 89, 233,
                3, 34, 4, 8,
            ],
            [
                1, 0, 0, 0,
                0, 1, 2, 9,
                1, 0, 0, 0,
                0, 1, 2, 9,
            ],
            [
                0, 0, 0, 1,
                0, 2, 0, 3,
                0, 4, 0, 5,
                0, 6, 0, 7,
                0, 8, 0, 9,
                0, 10, 0, 11,
                0, 12, 0, 13,
                0, 14, 0, 15,
            ],
        ]

        # open the file with data for test
        path = osp.abspath(osp.dirname(__file__))
        path = osp.join(path, 'data', 'data.dat')
        with open(path, 'r') as f:
            # read a line corresponding to a packet
            for line in f.readlines():
                # append the data
                data = [int(x) for x in line.split()]
                self.data.append(data)

        # convert into unsigned int bytes array
        self.byte_data = [
            bytes(struct.pack('>' + str(len(x)) + 'h', *x))
            for x in self.data
        ]

    def test_compress(self):
        """
        Just to check compression is good.
        """
        # run the test more than once to track segfault if possible
        for i in range(20):
            # loop over data
            for buf in self.byte_data:
                #  print("Buffer", buf, len(buf))
                self.compressor = Compressor()
                self.compressed = self.compressor.compress(
                    Data(
                        buf,
                        len(buf),
                    )
                )
                self.compressor = Compressor()
                #  print("Compressed", self.compressed, self.csize)
                self.uncompressed = self.compressor.uncompress(
                    self.compressed,
                    len(buf),
                )
                #  print("Uncompressed", self.uncompressed[0])

                # the comparison is done for the given size of the data and not
                # the entire data because there is a minimal size for the data
                # in output if the decompression, because they work by block
                #  print("Number", i)
                self.assertEqual(
                    buf[:len(buf)],
                    self.uncompressed.to_bytes()[:len(buf)],
                )
                #  print("")
                #  print("#################")
                #  print("\n"*3)
