# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        self.action_file_new = QAction(MainWindow)
        self.action_file_new.setObjectName(u"action_file_new")
        icon = QIcon()
        iconThemeName = u"document-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.action_file_new.setIcon(icon)
        self.action_file_open = QAction(MainWindow)
        self.action_file_open.setObjectName(u"action_file_open")
        self.action_file_save = QAction(MainWindow)
        self.action_file_save.setObjectName(u"action_file_save")
        self.action_file_save_as = QAction(MainWindow)
        self.action_file_save_as.setObjectName(u"action_file_save_as")
        self.action_file_close = QAction(MainWindow)
        self.action_file_close.setObjectName(u"action_file_close")
        self.action_edit_cut = QAction(MainWindow)
        self.action_edit_cut.setObjectName(u"action_edit_cut")
        self.action_edit_copy = QAction(MainWindow)
        self.action_edit_copy.setObjectName(u"action_edit_copy")
        self.action_edit_paste = QAction(MainWindow)
        self.action_edit_paste.setObjectName(u"action_edit_paste")
        self.action_edit_undo = QAction(MainWindow)
        self.action_edit_undo.setObjectName(u"action_edit_undo")
        self.action_edit_redo = QAction(MainWindow)
        self.action_edit_redo.setObjectName(u"action_edit_redo")
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.gridLayout_2 = QGridLayout(self.central_widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.main_data_tab_widget = QTabWidget(self.central_widget)
        self.main_data_tab_widget.setObjectName(u"main_data_tab_widget")
        self.main_data_tab_widget.setTabPosition(QTabWidget.South)
        self.main_data_tab_widget.setTabShape(QTabWidget.Rounded)

        self.gridLayout_2.addWidget(self.main_data_tab_widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.central_widget)
        self.main_menubar = QMenuBar(MainWindow)
        self.main_menubar.setObjectName(u"main_menubar")
        self.main_menubar.setGeometry(QRect(0, 0, 640, 37))
        self.menuFile_F = QMenu(self.main_menubar)
        self.menuFile_F.setObjectName(u"menuFile_F")
        self.menuEdit_E = QMenu(self.main_menubar)
        self.menuEdit_E.setObjectName(u"menuEdit_E")
        MainWindow.setMenuBar(self.main_menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.main_menubar.addAction(self.menuFile_F.menuAction())
        self.main_menubar.addAction(self.menuEdit_E.menuAction())
        self.menuFile_F.addAction(self.action_file_new)
        self.menuFile_F.addAction(self.action_file_open)
        self.menuFile_F.addSeparator()
        self.menuFile_F.addAction(self.action_file_save)
        self.menuFile_F.addAction(self.action_file_save_as)
        self.menuFile_F.addSeparator()
        self.menuFile_F.addAction(self.action_file_close)
        self.menuEdit_E.addAction(self.action_edit_undo)
        self.menuEdit_E.addAction(self.action_edit_redo)
        self.menuEdit_E.addSeparator()
        self.menuEdit_E.addAction(self.action_edit_cut)
        self.menuEdit_E.addAction(self.action_edit_copy)
        self.menuEdit_E.addAction(self.action_edit_paste)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Statsu", None))
        self.action_file_new.setText(QCoreApplication.translate("MainWindow", u"New... (&N)", None))
#if QT_CONFIG(tooltip)
        self.action_file_new.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Create new dataframe</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_file_new.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_file_open.setText(QCoreApplication.translate("MainWindow", u"Open... (&O)", None))
#if QT_CONFIG(tooltip)
        self.action_file_open.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Open or Import files</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_file_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_file_save.setText(QCoreApplication.translate("MainWindow", u"Save (&S)", None))
#if QT_CONFIG(shortcut)
        self.action_file_save.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_file_save_as.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
        self.action_file_close.setText(QCoreApplication.translate("MainWindow", u"Close (&W)", None))
#if QT_CONFIG(tooltip)
        self.action_file_close.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Close window</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_file_close.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_cut.setText(QCoreApplication.translate("MainWindow", u"Cut (&X)", None))
#if QT_CONFIG(shortcut)
        self.action_edit_cut.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_copy.setText(QCoreApplication.translate("MainWindow", u"Copy (&C)", None))
#if QT_CONFIG(shortcut)
        self.action_edit_copy.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_paste.setText(QCoreApplication.translate("MainWindow", u"Paste (&V)", None))
#if QT_CONFIG(shortcut)
        self.action_edit_paste.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_undo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.action_edit_redo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        self.menuFile_F.setTitle(QCoreApplication.translate("MainWindow", u"File (&F)", None))
        self.menuEdit_E.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

