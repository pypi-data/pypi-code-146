

import sys
import logging

#from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, 
    QApplication, 
    QMainWindow, 
    QAction, 
    QMenu, 
    QMenuBar, 
    QDockWidget, 
    QMessageBox) 
from PyQt5.QtGui import QIcon

import dbdicom as db
import wezel

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


# Examples of style sheets
# https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html
# 

STYLESHEET = """ 
    QMdiArea {
        background-color: rgb(32, 32, 32);
    }
    QDockWidget {
        border: 0px;
    }
    QScrollBar:vertical {
        border: 0px ;
        background: black;
        width: 10px;
    }
    QScrollBar::handle:vertical {
        background: rgb(32, 32, 32);
        min-height: 20px;
    }
    QMainWindow {
        background: rgb(128, 128, 128);
    }
    QMainWindow::separator {
        width: 2px; /* when vertical */
        height: 2px; /* when horizontal */
    }
    QMenuBar {
        background-color: rgb(128, 128, 128); 
    }
    QTreeView {
        background: rgb(32, 32, 32);
    }
    QTreeView::item { 
        color: rgb(128, 128, 128);
    }
    QTreeView::item:selected { 
        background-color: rgb(32, 32, 64);
    }
    """


class Wezel:

    def __init__(self):
        self.log = logger()
        self.QApp = QApplication(sys.argv)
        self.QApp.setWindowIcon(QIcon(wezel.icons.favicon))
        self.main = Main(self)

    def open(self, path):
        self.main.open(path)

    def show(self):    
        self.log.info('Launching Wezel!')
        try:
            self.main.show()
            self.QApp.exec()
            #sys.exit(self.QApp.exec())
        except Exception as e:
            print('Error: ' + str(e))
            self.log.exception('Error: ' + str(e))


class Main(QMainWindow):

    def __init__(self, wzl): 
        super().__init__()
        self.wezel = wzl
        #self.setStyleSheet(STYLESHEET)
        self.setWindowTitle("Wezel")
        #self.setWindowIcon(QIcon(wezel.icons.favicon))

        self.dialog = wezel.widgets.Dialog(self)
        self.status = wezel.widgets.StatusBar()
        self.setStatusBar(self.status)

        self.toolBar = {}
        self.toolBarDockWidget = QDockWidget()
        self.addDockWidget(Qt.RightDockWidgetArea, self.toolBarDockWidget)
        self.toolBarDockWidget.hide()

        self.treeView = None
        self.treeViewDockWidget = QDockWidget()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.treeViewDockWidget)
        self.treeViewDockWidget.hide()

        self.folder = None # should be in TreeView
        self.central = wezel.widgets.MainMultipleDocumentInterface()
        self.central.subWindowActivated.connect(lambda subWindow: self.activateSubWindow(subWindow))
        self.setCentralWidget(self.central)

        self.set_menu(wezel.menus.dicom)

    def closeEvent(self, event): #main
        accept = self.close()
        if accept:
            event.accept()
        else:
            event.ignore()

    def set_menu(self, menu):
        self.menubar = MenuBar(self, menu)
        self.setMenuBar(self.menubar)

    def open(self, path):
        self.folder = db.database(path=path, 
            status = self.status, 
            dialog = self.dialog)
        self.display(self.folder)
        self.status.hide()

    def close(self):
        """Closes the application."""
        if self.folder is None:
            return True
        accept = self.folder.close()
        if accept:
            self.folder = None
            self.toolBarDockWidget.hide()
            self.treeViewDockWidget.hide()
            for subWindow in self.central.subWindowList():
                self.central.removeSubWindow(subWindow)
            self.menuBar().enable()
        return accept

    def refresh(self):
        """
        Refreshes the Wezel display.
        """
        self.status.message('Refreshing display..')
        self.treeView.setFolder()
        self.menuBar().enable()
        self.status.hide()
        
    def display(self, object):
        if object.type() == 'Database':
            self.treeView = wezel.widgets.DICOMFolderTree(object)
            self.treeView.itemSelectionChanged.connect(self.menuBar().enable)
            self.treeViewDockWidget.setWidget(self.treeView)
            self.treeViewDockWidget.show()
            self.menuBar().enable()
        elif object.type() == 'Patient': # No Patient Viewer yet
            pass
        elif object.type() == 'Study': # No Study Viewer yet
            pass
        elif object.type() == 'Series':
            seriesDisplay = wezel.widgets.SeriesDisplay()
            seriesDisplay.setSeries(object)
            self.addWidget(seriesDisplay, title=object.label())
        elif object.type() == 'Instance':
            pass

    def addWidget(self, widget, title):
        # rename to addMainWidget()
        # widget needs to be subclassed from MainWidget
        if widget.error:
            return
        subWindow = self.central.addWidget(widget, title)
        subWindow.closed.connect(lambda: self.closeSubWindow(subWindow))
        self.central.tileSubWindows()
        if widget.toolBarClass is not None:
            toolBarName =  widget.toolBarClass.__name__
            if toolBarName in self.toolBar:
                toolBar = self.toolBar[toolBarName]
                widget.setToolBar(toolBar)
            else:
                toolBar =  widget.toolBarClass()
                self.toolBar[toolBarName] = toolBar
                self.toolBarDockWidget.setWidget(toolBar)
                widget.setToolBar(toolBar)
                self.toolBarDockWidget.show()

    def closeSubWindow(self, subWindow):
        self.central.removeSubWindow(subWindow)
        self.central.tileSubWindows()
        widget = subWindow.widget().__class__.__name__
        if 0 == self.central.countSubWindow(widget):
            self.toolBarDockWidget.hide()
        self.refresh()

    def activateSubWindow(self, subWindow):
        if self.central.activeWindow == subWindow:
            return
        activeWindow = self.central.activeWindow
        if activeWindow is not None:
            activeWindow.widget().setActive(False)
        self.central.activeWindow = subWindow
        if subWindow is not None:
            subWindow.widget().setActive(True)

    def get_selected(self, generation):   
        if self.treeView is None: 
            return []
        return self.treeView.get_selected(generation)

    def selected(self, generation):
        if self.treeView is None: 
            return []
        return self.treeView.selected(generation)
 
    def nr_selected(self, generation):
        if self.treeView is None: 
            return 0
        return self.treeView.nr_selected(generation)


class MainWidget(QWidget):
    """Base class for widgets that are set as subWindow widgets"""

    def __init__(self):
        super().__init__()
        self.toolBarClass = None
        self.toolBar = None
        self.error = False

    def setError(self, message='Error displaying data!!'):
        self.error = True
        QMessageBox.information(self, 'Information', message)

    def setToolBar(self, toolBar):
        self.toolBar = toolBar
        self.setToolBarState()

    def setToolBarState(self):
        self.toolBar.setWidget(self)
        
    def setActive(self, active):
        if active:
            if self.toolBar is not None:
                self.setToolBarState()
                subWindow = self.parentWidget()
                mdiArea = subWindow.mdiArea()
                mainWindow = mdiArea.parentWidget()
                mainWindow.toolBarDockWidget.setWidget(self.toolBar)
                
    def closeEvent(self, event):
        pass



class MenuBar(QMenuBar):
    """
    Programming interfaces for the Wezel menus. 
    """

    def __init__(self, main, menu):
        super().__init__()

        self._menus = []
        self.main = main
        menu(self)
        self.enable()

    def addMenu(self, menu):
        super().addMenu(menu)
        self._menus.append(menu)
        
    def menu(self, label = "Menu"):
        """
        Creates a top level menu in the menuBar.
        """
        return Menu(self, label)

    def enable(self):
        """
        Refreshes the enabled status of each menu item.
        """
        for menu in self._menus:
            menu.enable()


class Menu(QMenu):

    def __init__(self, parent, title='Menu'):
        super().__init__()

        self._actions = []
        self._menus = []
        self.setTitle(title)
        self.main = parent.main
        if parent is not None:
            parent.addMenu(self)

    def addMenu(self, menu):
        super().addMenu(menu)
        self._menus.append(menu)

    def menu(self, title='Submenu'):
        return Menu(self, title)

    def action(self, action, **kwargs):
        #return action(self, **kwargs)
        action = action(self, **kwargs)
        self.addAction(action)
        self._actions.append(action)
        return action
        
    def separator(self):
        self.addSeparator() 

    def enable(self):
        """
        Refreshes the enabled status of each menu item.
        """
        for submenu in self._menus:
            submenu.enable()
        for action in self._actions:
            enable = action.enable(action.main)
            action.setEnabled(enable)


class Action(QAction):
    """Base class for all wezel actions"""

    def __init__(self, parent,
        text = None,
        shortcut = None,
        tooltip = None, 
        icon = None,  
        **kwargs):
        """parent: App, Menu or MenuBar"""
        super().__init__()

        self.main = parent.main
        # parent.addAction(self)
        # parent._actions.append(self)

        # if hasattr(parent, 'main'):
        #     self.main = parent.main
        #     parent.addAction(self)
        #     parent._actions.append(self)
        # else:
        #     self.main = parent
        if text is None:
            text = self.__class__.__name__
        self.setText(text)
        self.triggered.connect(lambda: self.run(self.main))
    
        if icon is not None: 
            self.setIcon(QIcon(icon))
        if shortcut is not None: 
            self.setShortcut(shortcut)
        if tooltip is not None: 
            self.setToolTip(tooltip)

        # Dictionary with optional settings
        for option in kwargs:
            self.__dict__[option] = kwargs[option]

    def enable(self, app):
        return True

    def run(self, app):
        pass






def logger():
    
    LOG_FILE_NAME = "wezel_log.log"
    # creates some sort of conflict with mdreg - commenting out for now
#    if os.path.exists(LOG_FILE_NAME):
#        os.remove(LOG_FILE_NAME)
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename = LOG_FILE_NAME, 
        level = logging.INFO, 
        format = LOG_FORMAT)
    return logging.getLogger(__name__)


