import unittest

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction, FacingDirection
from smb3_eh_manip.app.hbs.w1_hb_test import W1HBTest


class TestW1HBTest(unittest.TestCase):
    def test_left_move(self):
        subject = W1HBTest()
        lsfr = LSFR([232, 229, 52, 254, 151, 106, 68, 144, 25])
        self.assertEqual(
            FacingDirection(Direction.RIGHT, Direction.RIGHT),
            subject.calculate_facing(lsfr),
        )
