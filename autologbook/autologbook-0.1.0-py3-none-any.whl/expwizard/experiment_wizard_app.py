"""
Main script executing the experiment wizard.
"""
import ctypes
import sys
from argparse import ArgumentParser

import urllib3
from PyQt5.QtWidgets import QApplication

from expwizard.experiment_wizard import ExperimentWizard

urllib3.disable_warnings()


def top_level_parser() -> ArgumentParser:
    """Return the main argument parser"""
    parser = ArgumentParser(
        description='''Graphical Wizard for the generation of a new or for the location of an existing
        microscopy experiment. '''
    )

    # TODO: add parser parameters

    return parser


def main_gui(cli_args: ArgumentParser):
    """Main GUI function"""
    app = QApplication(sys.argv)
    win = ExperimentWizard(parent=None, app=app)
    win.show()

    sys.exit(app.exec())


def main():
    """The MAIN"""
    parser = top_level_parser()
    parser.prog = 'experiment-wizard'
    args = parser.parse_args(sys.argv[1:])

    myappid = u'ecjrc.experimentwizard.gui.v0.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    main_gui(args)


if __name__ == '__main__':
    main()
