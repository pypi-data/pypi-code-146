import logging
import os.path
import traceback
import webbrowser

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import matc.constants
import matc.shared


class BaseModalDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setModal(True)
        self.setWindowIcon(QtGui.QIcon(matc.shared.get_app_icon_path()))
        self.vbox = QtWidgets.QVBoxLayout(self)

        # self.vbox.addWidget(QtWidgets.QLabel("init_wrapper, before __init__"))
        self.init_function(*args, **kwargs)  # <-------------------
        # self.vbox.addWidget(QtWidgets.QLabel("init_wrapper, after __init__"))

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Close, QtCore.Qt.Horizontal, self)
        self.vbox.addWidget(self.button_box)
        self.button_box.rejected.connect(self.reject)
        self.adjustSize()

    @classmethod
    def start(cls, *args, **kwargs):
        dlg = cls(*args, **kwargs)
        dlg.exec()

    def init_function(self, *args, **kwargs):
        raise NotImplementedError


class SysinfoDialog(BaseModalDialog):
    # noinspection PyAttributeOutsideInit
    def init_function(self, *args, **kwargs):
        """
        self._system_info_list = []
        sys_info: dict = matc.shared.get_system_info()
        for descr, value in sys_info.items():
            self._system_info_list.append(descr + ": " + str(value))
        """
        formatted_info_lines_list = [
            descr + ": " + str(value) for descr, value in matc.shared.get_system_info().items()]
        self._system_info_str = '\n'.join(formatted_info_lines_list)

        self.system_info_pqte = QtWidgets.QPlainTextEdit()
        self.vbox.addWidget(self.system_info_pqte)
        self.system_info_pqte.setReadOnly(True)
        self.system_info_pqte.setPlainText(self._system_info_str)

        self.copy_qpb = QtWidgets.QPushButton("Copy to clipboard")
        self.copy_qpb.clicked.connect(self.on_copy_button_clicked)
        self.vbox.addWidget(self.copy_qpb)

    def on_copy_button_clicked(self):
        qclipboard = QtGui.QGuiApplication.clipboard()
        qclipboard.setText(self._system_info_str)
        # -this will copy the text to the system clipboard


class FeedbackDialog(BaseModalDialog):
    # noinspection PyAttributeOutsideInit
    def init_function(self, *args, **kwargs):
        help_request_str = """<h3>Help Us</h3>
        <p>We are grateful for feedback, for example please contact us if you</p>
        <ul>
        <li>find a bug</li>
        <li>have a suggestion for a new feature</li>
        <li>have ideas for how to improve the interface</li>
        <li>have feedback about what you like about the application and how it helps you when 
        using the computer (we are looking for testimonials!)</li>
        </ul>
        <p>You can reach us using this email address:</p>"""

        self.help_request_qll = QtWidgets.QLabel()
        self.help_request_qll.setText(help_request_str)
        self.help_request_qll.setWordWrap(True)
        self.vbox.addWidget(self.help_request_qll)

        self.email_qll = QtWidgets.QLabel()
        font = self.email_qll.font()
        font.setPointSize(font.pointSize() + 8)
        self.email_qll.setFont(font)
        self.email_qll.setText(matc.constants.EMAIL_ADDRESS)
        self.vbox.addWidget(self.email_qll)

        self.emailus_qpb = QtWidgets.QPushButton("Email us!")
        self.emailus_qpb.clicked.connect(self.on_emailus_clicked)
        self.vbox.addWidget(self.emailus_qpb)

    def on_emailus_clicked(self):
        url_string = f"mailto:{matc.constants.EMAIL_ADDRESS}"
        webbrowser.open(url_string)
        # Alt: QtGui.QDesktopServices.openUrl(QtCore.QUrl(url_string))


class AboutDlg(BaseModalDialog):
    # noinspection PyAttributeOutsideInit
    def init_function(self, *args, **kwargs):
        """
        About LICENSE.txt:
        * We cannot use file:// when accessing the file
        * The file is located in the ./ directory. This must be because the active dir

        """
        self.setWindowTitle(
            f"About Mindfulness at the Computer - {matc.constants.APPLICATION_PRETTY_NAME}")

        all_contributors_url = (
            "https://gitlab.com/mindfulness-at-the-computer/mindfulness-at-the-computer/graphs"
            "/master")
        module_path = matc.shared.get_module_path()
        project_path = os.path.dirname(module_path)
        license_file_abs_path: str = os.path.join(module_path, "LICENSE.txt")
        if not os.path.isfile(license_file_abs_path):
            license_file_abs_path: str = os.path.join(project_path, "LICENSE.txt")
        if not os.path.isfile(license_file_abs_path):
            raise Exception("Cannot find license file")
        about_markdown_text: str = f"""
# About {matc.constants.APPLICATION_PRETTY_NAME}

Version: **{matc.shared.get_version()}**

Software License: **GPLv3** (see license file in installation dir)
[license file]({license_file_abs_path})

## Credits

Project started and maintained by Tord Dellsén - [Website](https://sunyatazero.gitlab.io/)

### Design

Shweta Singh Lodhi - [LinkedIn](https://www.linkedin.com/in/lodhishweta)

We have also been helped by feedback from our users

### Programming

Programmers: [All contributors]({all_contributors_url})

### Art

Photography for application icon by Torgny Dellsén

[torgnydellsen.zenfolio.com](https://torgnydellsen.zenfolio.com)

Application logo by Yu Zhou (layout modified by Tord Dellsén)

All audio files used have been released into the public domain (CC0)
        """

        # noinspection PyCallByClass
        self.info_qll = QtWidgets.QLabel()
        self.info_qll.setWordWrap(True)
        self.info_qll.setText(about_markdown_text.strip())
        self.info_qll.setTextFormat(QtCore.Qt.MarkdownText)
        self.info_qll.setOpenExternalLinks(True)
        self.vbox.addWidget(self.info_qll)


class UpdateAvailableDlg(BaseModalDialog):
    # noinspection PyAttributeOutsideInit
    def init_function(self, *args, **kwargs):
        self.setMinimumWidth(350)
        self.setMinimumHeight(200)
        self.setWindowTitle(f"Check for Updates - {matc.constants.APPLICATION_PRETTY_NAME}")

        self.update_qll = QtWidgets.QTextBrowser()
        self.vbox.addWidget(self.update_qll)
        # self.update_qll.setTextFormat(QtGui.Qt.TextFormat.RichText)
        # self.update_qll.setWordWrap(True)
        self.update_qll.setOpenExternalLinks(True)
        """
        flags: QtCore.Qt.TextInteractionFlags = self.update_qte.textInteractionFlags()
        flags = flags | int(QtCore.Qt.LinksAccessibleByMouse)
        self.update_qte.setTextInteractionFlags(flags)
        """
        source_forge_url = "https://sourceforge.net/projects/mindfulness-at-the-computer/"

        update_markdown_text: str = f"""
### Please update to the latest version

If you have installed using **pip** you can update using this command:

`pip install -U mindfulness-at-the-computer`

If you are running from a binary file (.exe) you can download the latest version from 
sourceforge: <a href="{source_forge_url}">{source_forge_url}</a>
"""
        self.update_qll.setMarkdown(update_markdown_text.strip())

    @classmethod
    def check_if_update_available_and_start(cls):
        update_available = matc.shared.is_update_available()
        if update_available:
            dlg = cls()
            dlg.exec()
        else:
            logging.info("You are running the latest version of the application")


class AlreadyLatestVersionDialog(BaseModalDialog):
    # noinspection PyAttributeOutsideInit
    def init_function(self, *args, **kwargs):
        self.info_qll = QtWidgets.QLabel("You are running the latest version!")
        self.vbox.addWidget(self.info_qll)


class ErrorDlg(BaseModalDialog):
    # noinspection PyAttributeOutsideInit
    def init_function(self, i_message_title, i_extra_info):
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setWindowTitle(f"Error Dialog - {matc.constants.APPLICATION_PRETTY_NAME}")

        self.message_title: str = i_message_title
        self.extra_info: str = i_extra_info

        # () = sys.exc_info()
        # self.call_stack = "".join(traceback.format_stack()[:-2])

        self.error_qpte = QtWidgets.QPlainTextEdit()
        self.vbox.addWidget(self.error_qpte)
        self.error_qpte.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.error_qpte.setReadOnly(True)
        self.error_qpte.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.error_qpte.setPlainText(f"{self.message_title}\n\n{self.extra_info}")

        hbox_l2 = QtWidgets.QHBoxLayout(self)
        self.vbox.addLayout(hbox_l2)
        self.report_qpb = QtWidgets.QPushButton("Report")
        hbox_l2.addWidget(self.report_qpb)
        self.report_qpb.clicked.connect(self.on_report_clicked)
        self.copy_qpb = QtWidgets.QPushButton("Copy")
        hbox_l2.addWidget(self.copy_qpb)
        self.copy_qpb.clicked.connect(self.on_copy_clicked)
        self.open_log_file_qpb = QtWidgets.QPushButton("Open log file")
        hbox_l2.addWidget(self.open_log_file_qpb)
        self.open_log_file_qpb.clicked.connect(self.on_open_log_file_clicked)

    def on_report_clicked(self):
        extra_info_for_email: str = self.extra_info.replace("\n", "%0D%0A")
        # -using %0D%0A is officially (RFC) the way to include a newline inside the email body
        extra_info_for_email: str = extra_info_for_email.replace(" ", "%20")
        message_for_email: str = self.message_title.replace(" ", "%20")
        url_string = (
            f"mailto:{matc.constants.EMAIL_ADDRESS}"
            f"?subject={message_for_email}&body="
            f"{extra_info_for_email}")
        webbrowser.open(url_string, new=1)

    def on_copy_clicked(self):
        qclipboard = QtGui.QGuiApplication.clipboard()
        qclipboard.setText(self.message_title + '\n' + self.extra_info)

    def on_open_log_file_clicked(self):
        log_file_path: str = matc.shared.get_config_path(matc.constants.LOG_FILE_NAME_STR)
        logging.info(f"{log_file_path=}")
        if not os.path.isfile(log_file_path):
            raise Exception("Log file not found")
        QtGui.QDesktopServices.openUrl(log_file_path)
        # webbrowser.open(log_file_path)

    @classmethod
    def log_and_start(cls, i_log_func, i_message_title: str, i_full_descr: str = ""):
        i_log_func(i_message_title)
        full_descr: str = "".join(traceback.format_stack()[:-2])
        if i_full_descr:
            full_descr = i_full_descr
        i_log_func(full_descr)
        dlg = cls(i_message_title, full_descr)
        dlg.exec()


if __name__ == "__main__":  # pragma no cover
    import sys

    matc_qapplication = QtWidgets.QApplication(sys.argv)
    SysinfoDialog.start()
    FeedbackDialog.start()
    AboutDlg.start()
    ErrorDlg.start("Error message_title to display", "i_extra_info")
    ErrorDlg.log_and_start(logging.debug, "Error message_title to display",
        "description\non\nmultiple\nlines")
    sys.exit(matc_qapplication.exec())
