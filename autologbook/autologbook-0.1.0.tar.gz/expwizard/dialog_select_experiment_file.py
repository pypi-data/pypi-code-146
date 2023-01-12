"""
Display a list of local experiment files and let the user decide which one to use.
"""

from pathlib import Path

from PyQt5.QtWidgets import QDialog

from expwizard.dialog_select_experiment_file_ui import Ui_SelectExperimentDialog
from expwizard.ini_syntax_highlighter import IniSyntaxHighlighter


class SelectExperimentDialog(QDialog, Ui_SelectExperimentDialog):
    """The Select Experiment Dialog"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.syntax_highlighter = IniSyntaxHighlighter(self.local_experiment_display.document())

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

# import sys
# from PyQt5.QtWidgets import QApplication
# def main():
#
#     app = QApplication(sys.argv)
#     win = SelectExperimentDialog(parent=None)
#
#     lista = [ 'C:\\Users\\Antonio\\Documents\\pyenv\\devenv\\autologbook\\autolog-conf.ini', ]
#     win.load_local_experiment_list(lista)
#     win.local_experiment_display.setReadOnly(False)
#
#     win.show()
#
#     sys.exit(app.exec())
#
# if __name__ ==  '__main__':
#     main()
