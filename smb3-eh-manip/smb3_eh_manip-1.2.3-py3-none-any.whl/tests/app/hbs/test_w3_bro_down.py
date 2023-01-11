import unittest

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Window
from smb3_eh_manip.app.hbs.w3_bro_down import W3BroDown


class TestW3BroDown(unittest.TestCase):
    def test_move_down(self):
        subject = W3BroDown()
        lsfr = LSFR([20, 32, 8, 72, 88, 200, 121, 233, 26])
        self.assertEqual(Window(156, 2), subject.calculate_3_1_window(lsfr))
