from typing import List

from picture_comparator_muri.controller.action_buttons import ActionButtonsController
from picture_comparator_muri.model.image_info import ImageInfo
from picture_comparator_muri.view.comparator_view import CompareWidget


class Comparator:
    def __init__(self, main_window_controller):
        self.main_window_controller = main_window_controller
        self.action_buttons: ActionButtonsController = main_window_controller.action_buttons
        self.compare_widget: CompareWidget = main_window_controller.window.ui.compare_widget
        self.images = []
        self.action_buttons.ShowInfoChanged.connect(self.update_view)
        self.action_buttons.ShowZoomChanged.connect(self.update_view)

    def clear(self):
        self.images.clear()
        self.compare_widget.clear()

    def reset(self):
        # Clearing leading_section is enough to reset zoom.
        self.compare_widget.leading_section = None

    def set_images(self, images: List[ImageInfo], group_changed: bool):
        self.images = images
        self.compare_widget.set_display_settings(self.action_buttons.display_settings)
        self.compare_widget.set_images(images, group_changed)

    def update_view(self):
        self.compare_widget.repaint()
