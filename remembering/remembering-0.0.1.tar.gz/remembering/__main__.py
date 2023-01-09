#!/usr/bin/env python3
import logging
import os.path
import sys

from PySide6 import QtWidgets

import remembering.gui.settings_win
import remembering.model_old
import remembering.rg_global


def on_about_to_quit_fired():
    print("on_about_to_quit_fired")
    # anxiety.model.History.close()
    remembering.model_old.backup_db_file()


def main():
    # Setting the path of the file to the current directory
    abs_path_str = os.path.abspath(__file__)
    dir_name_str = os.path.dirname(abs_path_str)
    os.chdir(dir_name_str)

    logging.basicConfig(level=logging.DEBUG)  # -by default only warnings and higher are shown

    """
    if not os.path.isfile(rg.model.DATABASE_FILE_NAME_STR):
        rg.model.setup_test_data()
    #rg.nn_global.active_rememberance_id =
    """

    application = QtWidgets.QApplication(sys.argv)

    application.setQuitOnLastWindowClosed(False)
    application.aboutToQuit.connect(on_about_to_quit_fired)
    main_window = remembering.gui.settings_win.SettingsWin()
    # main_window.showMaximized()

    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
