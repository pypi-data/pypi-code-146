import sys

from PySide6.QtCore import QObject

from picture_comparator_muri.controller.directory_picker import DirectoryPickerController
from picture_comparator_muri.controller.main_window import MainWindowController
from picture_comparator_muri.controller.settings import Settings


class Application(QObject):
    def __init__(self, args):
        super().__init__()
        self.settings = Settings(args)
        self.main_window = MainWindowController(self.settings)

    def start(self):
        if not self.settings.directories:
            directory_picker = DirectoryPickerController()
            result = directory_picker.exec()
            if not result:
                sys.exit(0)
            self.settings.directories = directory_picker.directories_list
            self.settings.scan_subdirectories = directory_picker.include_subdirectories
        self.main_window.start()
