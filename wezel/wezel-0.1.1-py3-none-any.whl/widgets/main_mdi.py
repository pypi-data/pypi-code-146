from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush
from PyQt5.QtWidgets import (                         
    QMdiArea, QWidget, QVBoxLayout, 
    QMdiSubWindow, QLabel,
)

class MainMultipleDocumentInterface(QMdiArea):

    def __init__(self):
        super().__init__()
        self.activeWindow = None
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setBackground(QBrush(Qt.black))

    def addSubWindow(self, subWindow):
        super().addSubWindow(subWindow) 
        height = self.height()
        width = self.width()
        subWindow.setGeometry(0, 0, width, height)
        self.tileSubWindows()
        subWindow.show() 

    def countSubWindow(self, class_name):
        """
        Counts all subwindows of a given Class
        """ 
        count = 0
        for subWindow in self.subWindowList():
            widget = subWindow.widget()
            if widget.__class__.__name__ == class_name:
                count += 1
        return count 

    def closeSubWindow(self, class_name):
        """
        Closes all subwindows of a given Class
        """   
        for subWindow in self.subWindowList():
            widget = subWindow.widget()
            if widget.__class__.__name__ == class_name:
                subWindow.close() 

    def addWidget(self, widget, title=None, icon=None):
        """This method takes a composite widget created by an external 
        application, makes it the central widget of an MDI subwindow 
        and displays that subwindow in the Wezel MDI""" 

        subWindow = MainMdiSubWindow()
        subWindow.setWidget(widget)
        #subWindow.setObjectName(widget.__class__.__name__)
        subWindow.setWindowFlags(
            Qt.CustomizeWindowHint | 
            Qt.WindowCloseButtonHint | 
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint)
        if title is not None:
            subWindow.setWindowTitle(title)
        if icon is not None:
            subWindow.setWindowIcon(QIcon(icon))
        self.addSubWindow(subWindow)
        self.activeWindow = subWindow
        return subWindow


class MainMdiSubWindow(QMdiSubWindow):

    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def closeEvent(self, event):
        self.widget().close()
        #self.deleteLater()
        self.closed.emit()
        