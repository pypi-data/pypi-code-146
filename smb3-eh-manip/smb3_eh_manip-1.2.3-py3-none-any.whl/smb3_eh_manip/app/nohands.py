"""
We want to have a manip such that with a second or so upon reaching the map
with the hands, we provide an audio cue where the player only holds left to
go over the hands unscathed with a window of >2 frames (preferably 3).

The time wasted holding left is about 24 frames. The time to wait between
coming out of the pipe and holding left is ideally <30 frames.

This class watches for level changes and times when the hands should occur.
A higher level class should be keeping track of what levels we have beaten.
"""

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Window
from smb3_eh_manip.util import settings

INTRA_PIPE_DURATION = 197
HALFWAY_PIPE_OFFSET = settings.get_int("nohands_intra_pipe_offset", fallback=80)
POST_PIPE_TO_CONTROL_DURATION = 56
PIPE_EXIT_LAG_FRAMES = 13
# When we go in the pipe before hands, we want to start calculating which
# is a good frame to hold left. This is the minimum time between entering
# the pipe and having control of mario on the overworld, minus pipe
# transition lag frames.
SECTION_TRIGGER_TO_OVERWORLD_CONTROL_RNG_FRAMES = (
    INTRA_PIPE_DURATION - HALFWAY_PIPE_OFFSET + POST_PIPE_TO_CONTROL_DURATION
)
# when holding left exiting the pipe, the frame# from origin to specific hand
TO_HAND1_CHECK_FRAME_DURATION = 17
TO_HAND2_CHECK_FRAME_DURATION = 39
TO_HAND3_CHECK_FRAME_DURATION = 16

# How many frames does the window have to be before pressing left?
# 3 is ideal if it happens within a second, otherwise 2 frames likely
LEFT_PRESS_WINDOW = settings.get_int("nohands_left_press_window", fallback=1)
# We cant look to the future, but let's default this as a reasonable
# couple seconds.
MAXIMUM_FRAMES_TO_LOOK_FORWARD = settings.get_int(
    "nohands_max_frames_to_look_forward", fallback=120
)


class NoHands:
    def calculate_optimal_window(self, seed_lsfr: LSFR):
        lsfr = seed_lsfr.clone()
        lsfr.next_n(SECTION_TRIGGER_TO_OVERWORLD_CONTROL_RNG_FRAMES)
        lsfr.next_n(TO_HAND1_CHECK_FRAME_DURATION)
        current_window = 0
        earliest_one_frame_window = None
        earliest_two_frame_window = None
        optimal_frame_offset = None

        # memoize hand check results we need, reducing repetition and
        # computational cycles
        frame_to_hand_check_memo = {}
        for frame in range(
            MAXIMUM_FRAMES_TO_LOOK_FORWARD
            + TO_HAND2_CHECK_FRAME_DURATION
            + TO_HAND3_CHECK_FRAME_DURATION
        ):
            frame_to_hand_check_memo[frame] = lsfr.hand_check()
            lsfr.next()

        for frame_offset in range(MAXIMUM_FRAMES_TO_LOOK_FORWARD):
            first_hand_check = frame_offset
            second_hand_check = first_hand_check + TO_HAND2_CHECK_FRAME_DURATION
            third_hand_check = second_hand_check + TO_HAND3_CHECK_FRAME_DURATION
            if (
                frame_to_hand_check_memo[first_hand_check]
                or frame_to_hand_check_memo[second_hand_check]
                or frame_to_hand_check_memo[third_hand_check]
            ):
                current_window = 0
                continue
            current_window += 1
            candidate_frame_offset = Window.create_centered_window(
                PIPE_EXIT_LAG_FRAMES
                + SECTION_TRIGGER_TO_OVERWORLD_CONTROL_RNG_FRAMES
                + frame_offset,
                current_window,
            )
            if current_window == 3:
                # if we have a 3 frame window we definitely use this immediately
                optimal_frame_offset = candidate_frame_offset
                break
            elif earliest_two_frame_window is None and current_window == 2:
                earliest_two_frame_window = candidate_frame_offset
            elif earliest_one_frame_window is None:
                earliest_one_frame_window = candidate_frame_offset
        if not optimal_frame_offset:
            if earliest_two_frame_window:
                optimal_frame_offset = earliest_two_frame_window
            else:
                optimal_frame_offset = earliest_one_frame_window
        return optimal_frame_offset
