import unittest

from smb3_eh_manip.app.lsfr import LSFR


class TestLSFR(unittest.TestCase):
    def test_next(self):
        lsfr = LSFR()
        for next_expected in [68, 34, 145, 72, 36, 18, 137, 68]:
            self.assertEqual(lsfr.next()[0], next_expected)

    def test_clone(self):
        lsfr = LSFR()
        lsfr.next_n(5)
        lsfr_clone = lsfr.clone()
        lsfr_clone.next()
        self.assertNotEqual(lsfr.get(0), lsfr_clone.get(0))

    def test_hand_check(self):
        lsfr = LSFR([156, 167, 158, 209, 236, 79, 151, 8, 38])
        self.assertFalse(lsfr.hand_check())
        lsfr = LSFR([201, 142, 29, 1, 59, 57, 79, 61, 163])
        self.assertTrue(lsfr.hand_check())

        lsfr = LSFR([103, 41, 231, 180, 123, 19, 229, 194, 9])
        self.assertFalse(lsfr.hand_check())
        lsfr = LSFR([242, 99, 135, 64, 78, 206, 83, 207, 104])
        self.assertFalse(lsfr.hand_check())
        lsfr = LSFR([221, 72, 242, 99, 135, 64, 78, 206, 83])
        self.assertTrue(lsfr.hand_check())
