"""
A dialog window to be used to compare the remote experiment file with one or more local files.
"""
from __future__ import annotations

from enum import IntEnum, auto
from pathlib import Path

from PyQt5.QtWidgets import QDialog

from expwizard.dialog_compare_experiment_file_ui import Ui_CompareExperimentDialog
from expwizard.ini_syntax_highlighter import IniSyntaxHighlighter


class CompareExperimentDialog(QDialog, Ui_CompareExperimentDialog):
    """
    Implementation of a dialog window to compare experiment files.

    The window is divided in two almost identical parts.

    On the left, the remote experiment file is displayed.
    On the right, one file from the selector can be displayed as text.
    """
    class ReturnValue(IntEnum):
        """Specific dialog return values"""
        AcceptLocal = auto()
        AcceptRemote = auto()

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.local_highlighter = IniSyntaxHighlighter(self.local_experiment_display.document())
        self.remote_highlighter = IniSyntaxHighlighter(self.remote_experiment_display.document())

    def load_remote_experiment(self, name, content):
        """
        Load the content of the remote experiment to the left display.

        Parameters
        ----------
        name: str
            The name of the remote experiment file.
        content: bytearray
            The content of the remote experiment file. This is taken from request response,
            so it is a byte array and needs to be decoded.
        """
        self.remote_exp_field.setText(name)
        self.remote_experiment_display.setPlainText(content.decode('utf-8'))

    def load_local_experiment_list(self, exp_list: list):
        """
        Load a list of local experiment files.

        The list should contain a list of experiment files. Their names are transferred to the
        local file selector and the first one is opened in the local display.

        Parameters
        ----------
        exp_list: list
            A list of local experiment files.
        """
        self.local_experiment_selector.clear()
        for exp in exp_list:
            self.local_experiment_selector.addItem(str(exp))
        self.local_experiment_selector.setCurrentIndex(0)
        self.load_local_experiment(self.local_experiment_selector.currentText())

    def load_local_experiment(self, filename: str | Path):
        """
        Load a local experiment with filename

        Parameters
        ----------
        filename: str | Path
            The filename to be opened and displayed in the local display.
        """
        self.local_experiment_display.clear()
        with open(filename, 'r') as file:
            self.local_experiment_display.setPlainText(file.read())

    def accept_remote(self):
        """Accept the remote file"""
        self.done(CompareExperimentDialog.ReturnValue.AcceptRemote)

    def accept_local(self):
        """Accept the local file"""
        self.done(CompareExperimentDialog.ReturnValue.AcceptLocal)
