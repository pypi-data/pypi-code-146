# SPDX-FileCopyrightText: 2023 Yann Büchau <nobodyinperson@posteo.de>
# SPDX-License-Identifier: GPL-3.0-or-later

# system modules
import os
import unittest

# internal modules
from hledger_utils import utils

# external modules


class UtilsTest(unittest.TestCase):
    def test_two_at_a_time(self):
        self.assertSequenceEqual(
            list(utils.two_at_a_time([1, 2, 3])), [(1, 2)]
        )
        self.assertSequenceEqual(list(utils.two_at_a_time([1])), [])
        self.assertSequenceEqual(
            list(utils.two_at_a_time([1, 2, 3, 4])), [(1, 2), (3, 4)]
        )

    def test_splitlines_roundtrip_join(self):
        for linesep in ["\n", "\r\n"]:
            for s in [
                linesep.join("abc"),
                linesep.join("abc") + linesep,
                "",
                linesep,
                linesep * 2,
                linesep * 3,
            ]:
                with self.subTest(linesep=linesep, string=s):
                    self.assertEqual(
                        linesep.join(utils.splitlines(s, linesep=linesep)), s
                    )
