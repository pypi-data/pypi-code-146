import logging
import pkg_resources

import cv2
import numpy as np

from smb3_eh_manip.app.state import State
from smb3_eh_manip.util import events
from smb3_eh_manip.util.settings import get_int, ACTION_FRAMES, FREQUENCY

VERSION = open("data/version.txt", "r").read().strip()
WINDOW_TITLE = f"eh manip ui {VERSION}"
LINE_COUNT = 6
WINDOW_SCALAR = 3
WINDOW_HEIGHT = int(FREQUENCY * WINDOW_SCALAR * 2.5)
VISUAL_CUE_HEIGHT = WINDOW_HEIGHT // 2
WINDOW_WIDTH = FREQUENCY * WINDOW_SCALAR * LINE_COUNT
LINE_COLOR = (255, 255, 255)
FILL_COLOR = (128, 128, 128)
PURPLE_COLOR = (211, 0, 148)
FONT_COLOR = (176, 176, 176)
TYPEFACE = cv2.FONT_HERSHEY_PLAIN
THICKNESS = 2


class UiPlayer:
    def __init__(self):
        self.trigger_frames = list(ACTION_FRAMES)
        self.window_open = True
        self.auto_close_ui_frame = get_int("auto_close_ui_frame", fallback=0)
        cv2.imshow(WINDOW_TITLE, UiPlayer.get_base_frame())
        events.listen(events.AddActionFrame, self.handle_add_action_frame)
        events.listen(events.LagFramesObserved, self.handle_lag_frames_observed)

    def reset(self):
        self.window_open = True
        self.trigger_frames = list(ACTION_FRAMES)

    def tick(self, current_frame, ewma_tick, state: State):
        if self.window_open:
            self.draw(current_frame, ewma_tick, state)

            if (
                self.auto_close_ui_frame > 0
                and current_frame > self.auto_close_ui_frame
            ):
                cv2.destroyWindow(WINDOW_TITLE)
                logging.debug(f"Auto closing ui window at {current_frame}")
                self.window_open = False

    def draw(self, current_frame, ewma_tick, state: State):
        ui = UiPlayer.get_base_frame()
        if self.trigger_frames:
            next_trigger_distance = (
                self.trigger_frames[0] - round(current_frame)
            ) * WINDOW_SCALAR
            if next_trigger_distance < WINDOW_WIDTH:
                left_x = (
                    WINDOW_WIDTH - next_trigger_distance - 2 * FREQUENCY * WINDOW_SCALAR
                )
                start = (left_x, 0)
                end = (left_x + FREQUENCY * WINDOW_SCALAR, VISUAL_CUE_HEIGHT)
                fill_color = PURPLE_COLOR if next_trigger_distance == 0 else FILL_COLOR
                ui = cv2.rectangle(ui, start, end, fill_color, -1)
                ui = cv2.rectangle(ui, start, end, LINE_COLOR, THICKNESS)
            if self.trigger_frames[0] < current_frame - 2 * FREQUENCY:
                trigger_frame = self.trigger_frames.pop(0)
                logging.debug(
                    f"Popped trigger frame {trigger_frame} at {current_frame}"
                )
        self.show_text(ui, current_frame, ewma_tick, state)
        cv2.imshow(WINDOW_TITLE, ui)

    def show_text(self, ui, current_frame, ewma_tick, state: State):
        x0 = 0
        x1 = WINDOW_WIDTH // 2
        y = VISUAL_CUE_HEIGHT + 24
        cv2.putText(ui, str(current_frame), (x0, y), TYPEFACE, 1, FONT_COLOR, 2)
        y += 20
        lag_frames_str = f"Lag frames: {state.total_observed_lag_frames}"
        cv2.putText(ui, lag_frames_str, (x0, y), TYPEFACE, 1, FONT_COLOR, 2)
        tick_str = f"Tick: {round(ewma_tick*1000)}ms"
        cv2.putText(ui, tick_str, (x1, y), TYPEFACE, 1, FONT_COLOR, 2)
        y += 20
        load_frames_str = f"Load frames: {state.total_observed_load_frames}"
        cv2.putText(ui, load_frames_str, (x0, y), TYPEFACE, 1, FONT_COLOR, 2)
        rng_str = f"RNG: {state.lsfr.data}"
        cv2.putText(ui, rng_str, (x1, y), TYPEFACE, 1, FONT_COLOR, 2)
        y += 20
        lag_inc_str = f"Lag RNG Inc: {state.total_lag_incremented_frames}"
        cv2.putText(ui, lag_inc_str, (x0, y), TYPEFACE, 1, FONT_COLOR, 2)
        active_segment_name = (
            state.active_section().name if state.category.sections else "N/A"
        )
        segment_str = f"Segment: {active_segment_name}"
        cv2.putText(ui, segment_str, (x1, y), TYPEFACE, 1, FONT_COLOR, 2)

    def handle_add_action_frame(self, event: events.AddActionFrame):
        self.trigger_frames.append(event.action_frame)
        self.trigger_frames.sort()

    def handle_lag_frames_observed(self, event: events.LagFramesObserved):
        self.trigger_frames = [
            frame + event.observed_lag_frames for frame in self.trigger_frames
        ]

    @classmethod
    def get_base_frame(self):
        frame = np.zeros(shape=[WINDOW_HEIGHT, WINDOW_WIDTH, 3], dtype=np.uint8)
        for x in range(1, LINE_COUNT):
            frame = cv2.line(
                frame,
                (x * FREQUENCY * WINDOW_SCALAR, 0),
                (x * FREQUENCY * WINDOW_SCALAR, VISUAL_CUE_HEIGHT),
                LINE_COLOR,
                THICKNESS,
            )
        return frame
