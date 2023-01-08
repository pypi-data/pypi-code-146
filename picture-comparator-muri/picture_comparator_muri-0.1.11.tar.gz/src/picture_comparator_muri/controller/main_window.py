from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication

from picture_comparator_muri.controller.action_buttons import ActionButtonsController
from picture_comparator_muri.controller.comparator import Comparator
from picture_comparator_muri.controller.group_list import GroupList
from picture_comparator_muri.controller.log import LogController
from picture_comparator_muri.controller.matches import MatchesController
from picture_comparator_muri.controller.settings import Settings
from picture_comparator_muri.model.image_info import ImageInfo
from picture_comparator_muri.model.log_engine import LogMessage, LogType
from picture_comparator_muri.model.search_engine import SearchEngine
from picture_comparator_muri.view.main_window import MainWindow


class MainWindowController:
    def __init__(self, settings: Settings):
        self.settings: Settings = settings
        self.window = MainWindow()
        self.log = LogController(self.window)
        self.search_engine = SearchEngine(settings)
        self.action_buttons = ActionButtonsController(self)

        self.group_list = GroupList(self)
        self.matches = MatchesController(self)

        self.window.ui.action_quit.triggered.connect(self.exit_application)
        self.window.ui.action_rename.triggered.connect(self.group_list.show_rename_dialog)
        self.window.ui.action_show_log.triggered.connect(self.show_log)

        # self.window.ui.list_thumbs_button.clicked.connect(self.set_list_thumbs)
        # self.window.ui.stacked_thumbs_button.clicked.connect(self.set_stack_thumbs)
        self.search_engine.ImageFound.connect(self.image_found)
        self.search_engine.LoadingImageFailed.connect(self.loading_image_failed)

        self.comparator.compare_widget.ImageHoverChanged.connect(self.display_path_on_statusbar)
        self.group_list.list_view.ImageHoverChanged.connect(self.display_path_on_statusbar)

    @property
    def comparator(self) -> Comparator:
        return self.group_list.comparator

    def start(self):
        self.window.show()
        self.search_engine.start_comparison()

    # def set_list_thumbs(self):
    #     self.window.ui.list_thumbs_button.setDown(True)
    #     self.window.ui.stacked_thumbs_button.setDown(False)
    #     self.window.ui.matches_stack.setCurrentIndex(0)
    #
    # def set_stack_thumbs(self):
    #     self.window.ui.list_thumbs_button.setDown(False)
    #     self.window.ui.stacked_thumbs_button.setDown(True)
    #     self.window.ui.matches_stack.setCurrentIndex(1)

    @Slot()
    def image_found(self, image: ImageInfo):
        self.log.log_message(LogMessage(LogType.INFO, f"Image found: {image.path}", True))

    @Slot()
    def loading_image_failed(self, reason: str, path: str):
        self.log.log_message(LogMessage(LogType.ERROR, f"Could not load '{path}'. {reason}.", True))

    @Slot()
    def display_path_on_statusbar(self, path: str):
        self.window.ui.statusbar.showMessage(path)

    @Slot()
    def show_log(self):
        self.log.show()

    @Slot()
    def exit_application(self):
        QApplication.quit()
