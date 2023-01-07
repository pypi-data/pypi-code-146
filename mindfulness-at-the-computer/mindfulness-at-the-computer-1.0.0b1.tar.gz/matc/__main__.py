import argparse
import faulthandler
import logging
import logging.handlers
import os
import sys

from PySide6 import QtCore
from PySide6 import QtWidgets

import matc.constants
import matc.main_object
# The following import looks like it isn't used, but it is necessary for importing the images.
import matc.matc_rc  # pylint: disable=unused-import
import matc.shared
import matc.state

JSON_SETTINGS_FILE_NAME = "settings.json"


def on_about_to_quit():
    matc.state.save_settings_to_json_file()
    logging.info("Exiting application gracefully")


def main():
    logger = logging.getLogger()
    # -if we set a name here for the logger the file handler will no longer work, unknown why
    logger.handlers = []  # -removing the default stream handler first
    # logger.propagate = False
    log_path_str = matc.shared.get_config_path(matc.constants.LOG_FILE_NAME_STR)
    rfile_handler = logging.handlers.RotatingFileHandler(log_path_str, maxBytes=8192, backupCount=2)
    rfile_handler.setLevel(logging.INFO)
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    # log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    rfile_handler.setFormatter(formatter)
    logger.addHandler(rfile_handler)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    stream_handler.setFormatter(formatter)
    if sys.flags.dev_mode:
        stream_handler.setLevel(logging.DEBUG)
    else:
        stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    if sys.flags.dev_mode:
        # logging.debug(f"{faulthandler.is_enabled()=}")
        # fh_file_path=matc.shared.get_config_path("filehandler_output.log")
        log_file_fd = open(log_path_str, "a")
        faulthandler.enable(log_file_fd)
        logging.debug("Running with sys.flags.dev_mode activated")
        """
        > By default, the Python traceback is written to sys.stderr. To see tracebacks,
        applications must be run in the terminal. A log file can alternatively be passed to
        faulthandler.enable().
        https://docs.python.org/3/library/faulthandler.html
        """

    def get_settings_file_path(i_date_text: str = ""):
        config_path = matc.shared.get_config_path()
        json_file_name: str = JSON_SETTINGS_FILE_NAME
        if i_date_text:
            json_file_name = json_file_name + "_" + i_date_text
        json_file_path = os.path.join(config_path, json_file_name)
        return json_file_path

    default_settings_file_path = get_settings_file_path()

    argument_parser = argparse.ArgumentParser(prog=matc.constants.APPLICATION_PRETTY_NAME,
        description=matc.constants.SHORT_DESCR)
    argument_parser.add_argument("--settings-file", "-s", default=default_settings_file_path,
        help="Path to a settings file (json format). If only a file name is given, the default "
             "directory will be used")
    parsed_args = argument_parser.parse_args()
    matc.state.initiate_state(parsed_args.settings_file)

    matc_qapplication = QtWidgets.QApplication(sys.argv)
    logging.info("Starting application")

    # Application information
    sys_info: dict = matc.shared.get_system_info()
    logging.debug("##### System Information #####")
    for descr_str, value in sys_info.items():
        logging.debug(descr_str + ": " + str(value))
    logging.debug("#####")

    # Set stylesheet
    stream = QtCore.QFile(os.path.join(matc.shared.get_module_path(), "matc.qss"))
    stream.open(QtCore.QIODevice.ReadOnly)
    matc_qapplication.setStyleSheet(QtCore.QTextStream(stream).readAll())

    matc_qapplication.setQuitOnLastWindowClosed(False)
    matc_qapplication.aboutToQuit.connect(on_about_to_quit)

    logging.debug(f"{sys.flags.dev_mode=}")
    # print(f"{matc.shared.testing_bool=}")

    is_first_time_ever_started = not matc.state.settings_file_exists()
    matc_main_object = matc.main_object.MainObject(is_first_time_ever_started)
    # -please note that this has to be stored in a variable, or the application will exit silently
    sys.exit(matc_qapplication.exec())


if __name__ == "__main__":
    main()

"""
def initialize(self, i_is_first_time_started: bool = False):
    # Initialization
    if i_is_first_time_started:
        matc.shared.do_extra_setup()
        matc.state.save_settings_to_json_file()
        self.show_intro_dialog()
    phrase = matc.state.get_breathing_phrase(self.active_phrase_id)
    self.br_dlg.show_breathing_dlg(phrase)
"""
