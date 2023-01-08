from enum import Enum


class DisplayMode(Enum):
    SINGLE = 1
    ONE_BY_ONE = 2


class Zoom(Enum):
    SCALED = 1
    FLAT = 2


class DisplaySettings:
    def __init__(self, action_buttons_controller):
        from picture_comparator_muri.controller.action_buttons import ActionButtonsController
        self.action_buttons_controller: ActionButtonsController = action_buttons_controller
        self.zoom = Zoom.SCALED
        self.display_mode = DisplayMode.ONE_BY_ONE
        self.show_info: bool = True
        self.show_zoom: bool = True

    @property
    def delete_mode(self) -> bool:
        return self.action_buttons_controller.delete_mode_button.isChecked()
