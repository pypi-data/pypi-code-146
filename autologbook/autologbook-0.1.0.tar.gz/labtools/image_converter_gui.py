#  Copyright (c) 2022.  Antonio Bulgheroni.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import ctypes
import sys
import time
from pathlib import Path

from PIL import Image
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QAction, QApplication, QDialog, QFileDialog, QListView, QMainWindow, QMenu

from labtools.about_image_converter_ui import Ui_About
from labtools.main_window_image_converter_ui import Ui_main_window_image_converter
from labtools.qt_exception_handler import UncaughtHook
from labtools.util import convert_image_format, get_image_list_from_directory_list, get_image_list_from_file_list

Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot

DEFAULT_OUTPUT_FORMAT = 'JPEG'

program_name = 'image-converter-gui'
program_version = 'v0.0.1'

# create a global instance of our class to register the hook
qt_exception_hook = UncaughtHook(prog=program_name)


class Worker(QtCore.QObject):
    """
    A worker class to perform the job in a separate thread.

    """
    progress = Signal(int, name='progress')
    work_done = Signal(name='work_done')
    work_aborted = Signal(name='work_aborted')
    image_processed = Signal(str, name='image_processed')

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.parent = parent
        self.required_parameters = [
            'image_list', 'output_format', 'preferred_ext']
        self.params = {}
        self.job_is_cancelled = False
        self.progress.connect(self.parent.conversion_progress_bar.setValue)
        self.work_done.connect(self.parent.conversion_completed)
        self.image_processed.connect(self.parent.remove_processed_image)

    def update_parameters(self, *args, **kwargs):
        """
        Received updated parameters for job execution.

        Parameters
        ----------
        args
        kwargs
        """
        for param in self.required_parameters:
            if param in kwargs:
                self.params[param] = kwargs[param]

    def start(self):
        """
        Start the worker job.

        Returns
        -------

        """
        self.job_is_cancelled = False
        if len(self.params['image_list']) == 0:
            self.work_done.emit()
            return
        for i, image in enumerate(self.params['image_list']):
            if self.job_is_cancelled:
                self.work_aborted.emit()
                break
            self.progress.emit(i)
            output_file_name = image.parent / \
                Path(image.stem + self.params['preferred_ext'])
            convert_image_format(
                input_img=image, format=self.params['output_format'], output_img=output_file_name)
            self.image_processed.emit(str(image))

        if not self.job_is_cancelled:
            self.progress.emit(len(self.params['image_list']))
            self.work_done.emit()

    @Slot()
    def stop(self):
        """
        Stop the conversion job.
        """
        self.job_is_cancelled = True


class AboutDialog(QDialog, Ui_About):
    """
    About Autologog Dialog.

    A very simple dialog message without button to show information about this
    program.
    """

    def __init__(self, parent=None):
        """
        Build an instance of the AboutDialog.

        Parameters
        ----------
        parent : QtObject, optional
            The parent calling QtObject. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(parent)
        self.setupUi(self)


class MainWindowImageConverter(QMainWindow, Ui_main_window_image_converter):
    """
    The Image Converter GUI Main Window.
    """

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setupUi(self)
        self.conversion_aborted = False
        self.is_worker_running = False

        worker = Worker(parent=self)
        worker_thread = QtCore.QThread()
        worker.setObjectName('ConversionWorker')
        worker_thread.setObjectName('ConversionThread')
        worker.moveToThread(worker_thread)
        worker_thread.start()

        # install the event filter
        self.list_view_selected_item.installEventFilter(self)

        self.push_button_start_conversion.clicked.connect(worker.start)
        # self.push_button_abort_conversion.clicked.connect(worker.stop)

        self.workers = {'ConversionWorker': worker}
        self.threads = {'ConversionThread': worker_thread}

        self.image_list = list()
        self.list_view_selected_item.setViewMode(QListView.ListMode)
        self.list_model = QStandardItemModel()
        self.list_view_selected_item.setModel(self.list_model)

        # preload all formats to the combo box output format
        self.ext_format_dict = Image.registered_extensions()
        self.supported_formats = [
            f for ex, f in Image.registered_extensions().items() if f in Image.OPEN]
        self.format_exts_dict = dict()
        for form in sorted(self.supported_formats):
            exts = [key for key, value in self.ext_format_dict.items()
                    if value == form]
            self.format_exts_dict[form] = exts
        self.load_supported_formats()

        self.statusBar().showMessage('Welcome to the Image Converter GUI.')
        self.app.aboutToQuit.connect(self.force_quit)
        # self.push_button_abort_conversion.setEnabled(True)

        self.starting_directory = Path.cwd()

        self.context_menu = QMenu()
        self.delete_action = QAction(self.context_menu)
        self.delete_action.setObjectName('delete_action')
        self.delete_action.setText('Remove selected items')
        self.context_menu.addAction(self.delete_action)
        self.delete_action.triggered.connect(self.remove_element_from_list)

        self.empty_list = QAction(self.context_menu)
        self.empty_list.setObjectName('remove_all_items')
        self.empty_list.setText('Remove all items')
        self.context_menu.addAction(self.empty_list)
        self.empty_list.triggered.connect(self.clear_selection)

        self.action_about_image_converter_gui.triggered.connect(self.display_about)

    def display_about(self):
        """
        Show the about dialog.

        Returns
        -------
        None.

        """
        dialog = AboutDialog(self)
        dialog.exec_()

    def remove_element_from_list(self):
        """
        React to the delete action triggered by context menu.

        """
        index_list = []
        for model_index in self.list_view_selected_item.selectionModel().selectedRows():
            index_list.append(QtCore.QPersistentModelIndex(model_index))
            self.image_list.remove(Path(self.list_view_selected_item.model().itemData(model_index)[0]))

        for index in index_list:
            self.list_model.removeRow(index.row())

        self.workers['ConversionWorker'].update_parameters(image_list=self.image_list,
                                                           output_format=self.combo_box_output_format.currentText(),
                                                           preferred_ext=self.combo_box_preferred_extension.currentText())
        if len(self.image_list):
            self.conversion_progress_bar.setRange(0, len(self.image_list))

    def eventFilter(self, source: 'QObject', event: 'QEvent') -> bool:
        """
        Event filter.

        It catches some of the events originating from the list_view widget.
        In particular, it catches the right click to open the context menu and the delete key pressed.

        Parameters
        ----------
        source: QObject
            The source object from where the event is coming from.
        event: QEvent
            The event being transmitted

        Returns
        -------
        bool

        """
        if event.type() == QtCore.QEvent.ContextMenu and source is self.list_view_selected_item:
            if self.context_menu.exec_(event.globalPos()):
                pass
            return True
        elif event.type() == QEvent.KeyPress and \
                event.key() == QtCore.Qt.Key_Delete and \
                source is self.list_view_selected_item:
            self.remove_element_from_list()
            return True
        return super().eventFilter(source, event)

    def load_supported_formats(self):
        """
        Load the supported format in the format combo box.
        """
        for form, exts in self.format_exts_dict.items():
            self.combo_box_output_format.addItem(form)
        self.combo_box_output_format.setCurrentText(DEFAULT_OUTPUT_FORMAT)
        self.load_corresponding_extensions()

    def load_corresponding_extensions(self):
        """
        Load the default extensions for the selected format.
        """
        self.combo_box_preferred_extension.clear()
        form = self.combo_box_output_format.currentText()
        exts = self.format_exts_dict[form]
        for ext in exts:
            self.combo_box_preferred_extension.addItem(ext)

    @Slot(str)
    def output_format_selection_changed(self, new_format: str):
        """
        React to a change in the format combo box.

        Parameters
        ----------
        new_format: str
            The new format

        """
        self.statusBar().showMessage(f'Output format changed to {new_format}')
        self.workers['ConversionWorker'].update_parameters(image_list=self.image_list,
                                                           output_format=self.combo_box_output_format.currentText(),
                                                           preferred_ext=self.combo_box_preferred_extension.currentText())
        self.load_corresponding_extensions()

    @Slot(str)
    def preferred_extension_changed(self, new_extension):
        """
        React to a change in the preferred extension combo box.

        Parameters
        ----------
        new_extension
        """
        new_format = self.combo_box_output_format.currentText()
        self.statusBar().showMessage(
            f'Output format changed to {new_format} with preferred extension {new_extension}.')
        self.workers['ConversionWorker'].update_parameters(image_list=self.image_list,
                                                           output_format=self.combo_box_output_format.currentText(),
                                                           preferred_ext=self.combo_box_preferred_extension.currentText())

    @Slot()
    def add_files(self):
        """
        Add multiple files to be processed.

        """
        new_files, mimes = QFileDialog.getOpenFileNames(self, 'Add multiple image files',
                                                        directory=str(self.starting_directory),
                                                        filter='All files (*.*)')

        if new_files:
            new_image_list = get_image_list_from_file_list(new_files)
            self.image_list.extend(new_image_list)
            for i, image in enumerate(new_image_list):
                if i == 0:
                    self.starting_directory = image.parent
                item = QStandardItem(str(image))
                self.list_model.appendRow(item)
            self.statusBar().showMessage('Added new files...')
            self.workers['ConversionWorker'].update_parameters(image_list=self.image_list,
                                                               output_format=self.combo_box_output_format.currentText(),
                                                               preferred_ext=self.combo_box_preferred_extension.currentText())
            self.conversion_progress_bar.setValue(0)
            if len(self.image_list):
                self.conversion_progress_bar.setRange(0, len(self.image_list))

    @Slot()
    def add_directory(self):
        """
        Add a whole directory for processing.
        """
        returnpath = QFileDialog.getExistingDirectory(self, 'Select a directory to add all its images',
                                                      directory=str(self.starting_directory))
        dir_list = list()
        if returnpath:
            dir_list.append(Path(returnpath))
            new_image_list = get_image_list_from_directory_list(
                dir_list, recursive=False)
            self.image_list.extend(new_image_list)
            for i, image in enumerate(new_image_list):
                if i == 0:
                    self.starting_directory = image.parent
                item = QStandardItem(str(image))
                self.list_model.appendRow(item)
            self.statusBar().showMessage('Added a new directory')
            self.workers['ConversionWorker'].update_parameters(image_list=self.image_list,
                                                               output_format=self.combo_box_output_format.currentText(),
                                                               preferred_ext=self.combo_box_preferred_extension.currentText())
            self.conversion_progress_bar.setValue(0)
            if len(self.image_list):
                self.conversion_progress_bar.setRange(0, len(self.image_list))

    @Slot()
    def add_directory_recursively(self):
        """
        Add directory recursively for processing.
        """
        returnpath = QFileDialog.getExistingDirectory(self, 'Select a directory to add all its images recursively',
                                                      directory=str(self.starting_directory))
        dir_list = list()
        if returnpath:
            dir_list.append(Path(returnpath))
            new_image_list = get_image_list_from_directory_list(
                dir_list, recursive=True)
            self.image_list.extend(new_image_list)
            for i, image in enumerate(new_image_list):
                if i == 0:
                    self.starting_directory = image.parent
                item = QStandardItem(str(image))
                self.list_model.appendRow(item)
            self.statusBar().showMessage('Added a new directory recursively')
            self.workers['ConversionWorker'].update_parameters(image_list=self.image_list,
                                                               output_format=self.combo_box_output_format.currentText(),
                                                               preferred_ext=self.combo_box_preferred_extension.currentText())
            self.conversion_progress_bar.setValue(0)
            if len(self.image_list):
                self.conversion_progress_bar.setRange(0, len(self.image_list))

    @Slot()
    def start_conversion(self):
        """
        Start the conversion.

        Activated by the push button.

        It produces a facelist.
        """
        self.conversion_aborted = False
        self.statusBar().showMessage('Conversion on going...')
        self.push_button_start_conversion.setEnabled(False)
        self.push_button_abort_conversion.setEnabled(True)
        self.action_start_conversion.setEnabled(False)
        self.action_abort_format_conversion.setEnabled(True)

    @Slot()
    def clear_selection(self):
        """
        Clear the selection
        """
        self.list_model.clear()
        self.image_list = list()
        self.statusBar().showMessage('Cleared all files...')
        self.workers['ConversionWorker'].update_parameters(image_list=self.image_list,
                                                           output_format=self.combo_box_output_format.currentText(),
                                                           preferred_ext=self.combo_box_preferred_extension.currentText())

    @Slot()
    def abort_conversion(self):
        """Abort the conversion job."""
        self.push_button_abort_conversion.setEnabled(False)
        self.push_button_start_conversion.setEnabled(True)
        for key, worker in self.workers.items():
            worker.stop()
        self.statusBar().showMessage('Conversion aborted')

        self.image_list = list()
        for i in range(self.list_model.rowCount()):
            if i != 0:
                self.image_list.append(Path(self.list_model.item(i, 0).text()))
        if len(self.image_list):
            self.conversion_progress_bar.setRange(0, len(self.image_list))
        self.workers['ConversionWorker'].update_parameters(image_list=self.image_list,
                                                           output_format=self.combo_box_output_format.currentText(),
                                                           preferred_ext=self.combo_box_preferred_extension.currentText())

    @Slot()
    def conversion_completed(self):
        """Change the GUI at the end of the conversion job."""
        self.push_button_abort_conversion.setEnabled(False)
        self.push_button_start_conversion.setEnabled(True)
        self.image_list = list()
        self.statusBar().showMessage('Conversion completed')

    @Slot(str)
    def remove_processed_image(self, image):
        """Remove the already processed images."""
        items = self.list_model.findItems(image, QtCore.Qt.MatchExactly)
        for item in items:
            item.model().removeRow(item.row())

    @Slot()
    def force_quit(self):
        """Force quit stopping all threads."""
        for key, worker in self.workers.items():
            worker.stop()
        for key, thread in self.threads.items():
            if thread.isRunning():
                thread.quit()
                thread.wait()


def main_gui():
    """The main method"""
    # to set the icon on the window task bar
    myappid = u'ecjrc.imageconverter.gui.v0.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    win = MainWindowImageConverter(app)
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main_gui()
