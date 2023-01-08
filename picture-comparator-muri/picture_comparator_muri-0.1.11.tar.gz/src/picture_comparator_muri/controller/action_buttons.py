from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QButtonGroup, QAbstractButton

from picture_comparator_muri.model.display_settings import DisplaySettings, DisplayMode


class ActionButtonsController(QObject):
    DisplayModeChanged = Signal(DisplayMode)
    ShowInfoChanged = Signal(bool)
    ShowZoomChanged = Signal(bool)

    def __init__(self, main_window_controller):
        super().__init__()
        from picture_comparator_muri.controller.main_window import MainWindowController
        self.main_window_controller: MainWindowController = main_window_controller
        self.display_mode_buttons = QButtonGroup()
        self.display_mode_buttons.addButton(self.main_window_controller.window.ui.display_multiple_button)
        self.display_mode_buttons.addButton(self.main_window_controller.window.ui.display_single_button)

        self.show_info_button = self.main_window_controller.window.ui.show_info_button
        self.show_zoom_button = self.main_window_controller.window.ui.show_zoom_button
        self.delete_mode_button = self.main_window_controller.window.ui.deleting_mode_button

        self.display_settings = DisplaySettings(self)

        self.display_mode_buttons.buttonClicked.connect(self._display_mode_changed)
        self.show_info_button.clicked.connect(self._show_info_changed)
        self.show_zoom_button.clicked.connect(self._show_zoom_changed)
        self.main_window_controller.window.DeleteModifierTriggered.connect(self._delete_modifier_changed)

    @property
    def display_mode(self):
        return self.display_settings.display_mode

    def _display_mode_changed(self, button: QAbstractButton):
        if button is self.main_window_controller.window.ui.display_single_button:
            self.display_settings.display_mode = DisplayMode.SINGLE
        else:
            self.display_settings.display_mode = DisplayMode.ONE_BY_ONE
        self.DisplayModeChanged.emit(self.display_settings.display_mode)

    def _show_info_changed(self, value: bool):
        self.display_settings.show_info = value
        self.ShowInfoChanged.emit(self.display_settings.show_info)

    def _show_zoom_changed(self, value: bool):
        self.display_settings.show_zoom = value
        self.ShowZoomChanged.emit(self.display_settings.show_zoom)

    def _delete_modifier_changed(self, value: bool):
        self.delete_mode_button.setChecked(not self.delete_mode_button.isChecked())
