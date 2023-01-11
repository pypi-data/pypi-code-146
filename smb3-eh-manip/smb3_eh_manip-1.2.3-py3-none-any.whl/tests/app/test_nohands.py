import unittest
from unittest.mock import patch

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app import nohands as nohands_module


class TestNoHands(unittest.TestCase):
    @patch.object(nohands_module, "MAXIMUM_FRAMES_TO_LOOK_FORWARD", 120)
    def test_window_162665(self):
        lsfr = LSFR([81, 237, 78, 148, 9, 33, 51, 113, 23])
        nohands = nohands_module.NoHands()
        optimal_frame_offset = nohands.calculate_optimal_window(lsfr)
        self.assertEqual(226, optimal_frame_offset.action_frame)
        self.assertEqual(2, optimal_frame_offset.window)
