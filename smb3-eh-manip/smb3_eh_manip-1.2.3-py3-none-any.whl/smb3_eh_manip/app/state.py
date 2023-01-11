from dataclasses import dataclass
import logging
from typing import Optional

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.nohands import NoHands
from smb3_eh_manip.app.hbs.w1_bro_left import W1BroLeft
from smb3_eh_manip.app.hbs.w3_bro_down import W3BroDown
from smb3_eh_manip.app.hbs.w4_cloud_bro_manip import W4CloudBroManip
from smb3_eh_manip.util import events, settings, wizard_mixins


@dataclass
class Section:
    name: str
    lag_frames: Optional[int] = None
    action: Optional[str] = None
    complete_frame: Optional[int] = None
    wait_frames: Optional[int] = None


@dataclass
class Category(wizard_mixins.YAMLWizard):
    sections: list[Section]

    @classmethod
    def load(cls, category_name):
        return Category.from_yaml_file(f"data/categories/{category_name}.yml")


def get_expected_lag_latency_frames():
    # practically, there is only one way to triger completed sections, and
    # it ultimately is from the serial server. while this class should be
    # implementation independent, we need to still offset here, so this
    # method (unfortunately) holds the details specific to serial server.
    if not settings.get_boolean("auto_detect_lag_frames_serial"):
        return 0
    from smb3_eh_manip.app.servers.serial_server import SERIAL_LATENCY_MS

    return round(SERIAL_LATENCY_MS / settings.NES_MS_PER_FRAME)


class State:
    def __init__(
        self,
        category_name=settings.get("category", fallback="nww"),
        expected_lag_latency_frames=get_expected_lag_latency_frames(),
    ):
        self.category_name = category_name
        self.enable_nohands = settings.get_boolean("enable_nohands", fallback=False)
        self.enable_w1broleft = settings.get_boolean("enable_w1broleft", fallback=False)
        self.enable_w3brodown = settings.get_boolean("enable_w3brodown", fallback=False)
        self.enable_w4cloudbromanip = settings.get_boolean(
            "enable_w4cloudbromanip", fallback=False
        )
        self.nohands = NoHands() if self.enable_nohands else None
        self.w1broleft = W1BroLeft() if self.enable_w1broleft else None
        self.w3brodown = W3BroDown() if self.enable_w3brodown else None
        self.w4cloudbromanips = (
            W4CloudBroManip() if self.enable_w4cloudbromanip else None
        )
        self.expected_lag_latency_frames = expected_lag_latency_frames
        self.reset()
        events.listen(events.LagFramesObserved, self.handle_lag_frames_observed)

    def handle_lag_frames_observed(self, event: events.LagFramesObserved):
        self.total_observed_lag_frames += event.observed_lag_frames
        self.total_observed_load_frames += event.observed_load_frames
        if self.check_expected_lag_trigger(event.observed_load_frames):
            self.completed_section(
                round(event.current_frame), self.category.sections.pop(0)
            )

    def check_complete_frame_trigger(self, current_frame: int):
        active_section = self.active_section()
        if not active_section:
            return False
        complete_frame = active_section.complete_frame
        return complete_frame and complete_frame <= current_frame

    def check_expected_lag_trigger(self, observed_load_frames: int):
        active_section = self.active_section()
        if not active_section:
            return False
        expected_section_lag = self.active_section().lag_frames
        return (
            expected_section_lag
            and expected_section_lag >= observed_load_frames - 1
            and expected_section_lag <= observed_load_frames + 1
        )

    def check_wait_frames_trigger(self, current_frame: int):
        active_section = self.active_section()
        if not active_section or active_section.wait_frames is None:
            return False
        if self.target_wait_frame:
            if current_frame >= self.target_wait_frame:
                self.target_wait_frame = 0
                return True
        else:
            self.target_wait_frame = (
                current_frame
                + active_section.wait_frames
                - self.expected_lag_latency_frames
            )
        return False

    def check_and_update_w1broleft_action(self, current_frame: int, section: Section):
        if not self.enable_w1broleft or section.action != "w1broleft":
            return
        window = self.w1broleft.calculate_window(self.lsfr)
        if not window:
            return
        action_frame = current_frame + window.action_frame
        events.emit(self, events.AddActionFrame(action_frame, window.window))
        logging.info(f"w1broleft at frame: {action_frame} with window: {window.window}")

    def check_and_update_nohands_action(self, current_frame: int, section: Section):
        if not self.enable_nohands or section.action != "nohands":
            return
        nohands_window = self.nohands.calculate_optimal_window(self.lsfr)
        if not nohands_window:
            return
        action_frame = current_frame + nohands_window.action_frame
        events.emit(self, events.AddActionFrame(action_frame, nohands_window.window))
        logging.info(
            f"NoHands at frame: {action_frame} with window: {nohands_window.window}"
        )

    def check_and_update_w3brodown_action(self, current_frame: int, section: Section):
        if not self.enable_w3brodown or (
            section.action != "w3brodown31" and section.action != "w3brodown32"
        ):
            return
        if section.action == "w3brodown31":
            window = self.w3brodown.calculate_3_1_window(self.lsfr)
        elif section.action == "w3brodown32":
            window = self.w3brodown.calculate_3_2_window(self.lsfr)
        if not window:
            return
        action_frame = current_frame + window.action_frame
        events.emit(self, events.AddActionFrame(action_frame, window.window))
        logging.info(f"w3brodown at frame: {action_frame} with window: {window.window}")

    def check_and_update_w4cloudbromanip_action(
        self, current_frame: int, section: Section
    ):
        if not self.enable_w4cloudbromanip or (
            section.action != "w4cloud41" and section.action != "w4cloud42"
        ):
            return
        if section.action == "w4cloud41":
            window = self.w4cloudbromanips.calculate_4_1_window(self.lsfr)
        elif section.action == "w4cloud42":
            window = self.w4cloudbromanips.calculate_4_2_window(self.lsfr)
        if not window:
            return
        action_frame = current_frame + window.action_frame
        events.emit(self, events.AddActionFrame(action_frame, window.window))
        logging.info(
            f"w4cloudbromanips at frame: {action_frame} with window: {window.window}"
        )

    def check_and_update_rng_frames_incremented_during_load_action(
        self, section: Section
    ):
        if section.action != "framerngincrement":
            return
        self.total_lag_incremented_frames += 60
        logging.debug(f"RNG frames incremented during load, offsetting")

    def tick(self, current_frame: int):
        # we need to see how much time has gone by and increment RNG that amount
        lsfr_increments = (
            current_frame
            - self.total_observed_lag_frames
            - self.total_observed_load_frames
            + self.total_lag_incremented_frames
            - self.lsfr_frame
        )
        if lsfr_increments > 0:
            # would be cool to go backwards here, but we wait to catch up instead
            self.lsfr.next_n(lsfr_increments)
            self.lsfr_frame += lsfr_increments

        while self.check_complete_frame_trigger(
            current_frame
        ) or self.check_wait_frames_trigger(current_frame):
            self.completed_section(current_frame, self.category.sections.pop(0))

    def completed_section(self, current_frame: int, section: Section):
        logging.debug(f"Completed {section.name}")
        self.check_and_update_rng_frames_incremented_during_load_action(section)
        self.check_and_update_nohands_action(current_frame, section)
        self.check_and_update_w1broleft_action(current_frame, section)
        self.check_and_update_w3brodown_action(current_frame, section)
        self.check_and_update_w4cloudbromanip_action(current_frame, section)

    def reset(self):
        self.total_lag_incremented_frames = 0
        self.total_observed_lag_frames = 0
        self.total_observed_load_frames = 12
        self.lsfr_frame = 0
        self.category = Category.load(self.category_name)
        self.lsfr = LSFR()
        self.target_wait_frame = 0

    def active_section(self):
        if not self.category.sections:
            return None
        return self.category.sections[0]
