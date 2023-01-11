import unittest

from smb3_eh_manip.app.state import Category, Section, State
from smb3_eh_manip.util import events


class TestState(unittest.TestCase):
    def test_rng_at_frame_120(self):
        state = State()
        state.tick(110)
        state.tick(120)
        self.assertEqual(129, state.lsfr.get(0))
        self.assertEqual(102, state.lsfr.get(1))
        self.assertEqual(100, state.lsfr.get(2))
        state.reset()
        state.tick(120)
        self.assertEqual(129, state.lsfr.get(0))
        self.assertEqual(102, state.lsfr.get(1))
        self.assertEqual(100, state.lsfr.get(2))

    def test_trigger_framerngincrement(self):
        state = State(category_name="nww")
        state.handle_lag_frames_observed(events.LagFramesObserved(1, 0, 12))
        self.assertEqual("1-1 enter", state.active_section().name)
        state.handle_lag_frames_observed(events.LagFramesObserved(2, 0, 63))
        # would be 75, but frames of rng increment during 1-1 enter, so we
        # trigger framerngincrement
        self.assertEqual(87, state.total_observed_load_frames)

    def test_load_frames_trigger(self):
        section = Section(name="testsection", wait_frames=5)
        state = State(expected_lag_latency_frames=1)
        state.category = Category([section])
        self.assertEqual(False, state.check_wait_frames_trigger(100))
        self.assertEqual(False, state.check_wait_frames_trigger(101))
        self.assertEqual(False, state.check_wait_frames_trigger(102))
        self.assertEqual(False, state.check_wait_frames_trigger(103))
        self.assertEqual(True, state.check_wait_frames_trigger(104))

    def test_wait_frames_trigger(self):
        state = State(category_name="nww")
        state.handle_lag_frames_observed(events.LagFramesObserved(1, 0, 12))
        state.handle_lag_frames_observed(events.LagFramesObserved(2, 0, 63))
        state.handle_lag_frames_observed(events.LagFramesObserved(3, 1, 0))
        self.assertEqual("1-1 exit", state.active_section().name)

    def test_frame_completed_trigger(self):
        state = State(category_name="warpless")
        current_frame = 10
        state.tick(current_frame)
        self.assertEqual("w1 enter", state.active_section().name)
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 1, 12))
        current_frame += 90
        state.tick(current_frame)
        self.assertEqual("1-1 enter", state.active_section().name)
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 1, 63))
        self.assertEqual("1-1 broleft", state.active_section().name)
        current_frame = 1
        state.tick(current_frame)
        current_frame += 80
        state.tick(current_frame)
        self.assertEqual("w2 airship mid", state.active_section().name)
        current_frame += 100
        state.tick(current_frame)
        self.assertEqual("w2 airship mid", state.active_section().name)
        current_frame += 28000
        state.tick(current_frame)
        self.assertEqual("w2 airship koopaling enter", state.active_section().name)

        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 0, 10))
        current_frame += 10
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 0, 10))
        current_frame += 10
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 0, 13))
        current_frame += 10
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 0, 71))
        current_frame += 10
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 0, 10))
        current_frame += 10
        state.tick(current_frame)
        self.assertEqual("3-1 brodown", state.active_section().name)
        current_frame += 80
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 0, 80))
        state.tick(current_frame)
        self.assertEqual("3-1 exit", state.active_section().name)
        current_frame += 13
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 0, 13))
        current_frame += 61
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 0, 61))
        current_frame += 11
        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 0, 11))
        state.tick(current_frame)
        current_frame += 80
        state.tick(current_frame)
        self.assertEqual("3-3 enter", state.active_section().name)

        state.handle_lag_frames_observed(events.LagFramesObserved(current_frame, 1, 63))
        current_frame += 1
        state.tick(current_frame)
        self.assertEqual("w3 airship mid", state.active_section().name)
        current_frame += 25000
        state.tick(current_frame)
        self.assertEqual("w3 airship koopaling enter", state.active_section().name)

    def test_lsfr(self):
        state = State()
        state.tick(12)
        self.assertEqual(136, state.lsfr.get(0))
        state.tick(13)
        self.assertEqual(68, state.lsfr.get(0))
        state.tick(16)
        self.assertEqual(72, state.lsfr.get(0))
        state.handle_lag_frames_observed(events.LagFramesObserved(1, 1, 0))
        state.tick(17)
        self.assertEqual(72, state.lsfr.get(0))
