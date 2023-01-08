import os.path

from PySide6.QtCore import QObject
from PySide6.QtGui import QImage


class Resources(QObject):
    resources_directory = os.path.split(__file__)[0]

    delete_marker = QImage(os.path.join(resources_directory, 'edit-delete.svg'))
