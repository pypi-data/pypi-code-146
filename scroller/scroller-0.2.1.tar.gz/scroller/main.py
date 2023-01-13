import ctypes
import os
import sys
import shutil
from PySide6.QtCore import QObject, QUrl, Slot, QtMsgType
from PySide6.QtGui import QPixmap
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
from scroller.ImageModel import ImageModel
import scroller.qml_rc

def qt_message_handler(mode, context, message):
    """
    A function that handles messages emitted by the Qt library.

    Args:
        mode (int): The message type.
        context (QtMessageHandlerContext): The message context.
        message (str): The message text.
    """
    if mode == QtMsgType.QtInfoMsg:
        mode = "Info"
    elif mode == QtMsgType.QtWarningMsg:
        mode = "Warning"
    elif mode == QtMsgType.QtCriticalMsg:
        mode = "critical"
    elif mode == QtMsgType.QtFatalMsg:
        mode = "fatal"
    else:
        mode = "Debug"
    print(
        "%s: %s (%s:%d, %s)" % (mode, message, context.file, context.line, context.file)
    )


class Backend(QObject):
    """
    A class that provides functionality to the GUI.
    """
    @Slot(QUrl, QUrl, result=bool)
    def copyFile(self, source: QUrl, destination: QUrl):
        """
        Copy a file from the source path to the destination path.

        Args:
            source (QUrl): The path of the source file.
            destination (QUrl): The path of the destination folder.

        Returns:
            bool: True if the file is copied successfully, False otherwise.
        """
        source = source.toLocalFile()
        name = os.path.basename(source)
        destination = destination.toLocalFile()
        if not os.path.exists(destination):
            os.makedirs(destination)
        
        try:
            shutil.copy(source, os.path.join(destination, name))
            return True
        except PermissionError:
            return False

def main():
    """
    The main entry point of the application.
    """
    app = QApplication(sys.argv)
    app.setOrganizationName("Ziru's Musings")
    app.setOrganizationDomain("github.com/robert-clayton")
    app.setApplicationName("scroller")
    app.setDesktopFileName("scroller")
    app.setWindowIcon(QPixmap('res/logo.png'))
    myappid = f"zirus-musings.scroller.bg.dev"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setApplicationVersion('dev')

    backend = Backend()
    images = ImageModel()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("ImageModel", images)
    engine.rootContext().setContextProperty("Backend", backend)
    engine.load("qrc:/gui")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())

