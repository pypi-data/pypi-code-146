# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QLayout, QListView, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QStackedWidget, QStatusBar, QVBoxLayout,
    QWidget)

from picture_comparator_muri.view.comparator_view import CompareWidget
from picture_comparator_muri.view.group_list_view import GroupListView
from picture_comparator_muri.view.matches_view import (MatchesListView, MatchesStackView)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1145, 815)
        self.action_quit = QAction(MainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.action_show_log = QAction(MainWindow)
        self.action_show_log.setObjectName(u"action_show_log")
        self.action_rename = QAction(MainWindow)
        self.action_rename.setObjectName(u"action_rename")
        self.action_rename.setEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.matches_stack = QStackedWidget(self.verticalLayoutWidget)
        self.matches_stack.setObjectName(u"matches_stack")
        self.matches_stack.setFrameShape(QFrame.NoFrame)
        self.full_view_page = MatchesListView()
        self.full_view_page.setObjectName(u"full_view_page")
        self.full_view_page.setLayoutDirection(Qt.LeftToRight)
        self.full_view_page.setStyleSheet(u"")
        self.full_view_page.setLayoutMode(QListView.SinglePass)
        self.full_view_page.setBatchSize(100)
        self.matches_stack.addWidget(self.full_view_page)
        self.thumbnails_page = MatchesStackView()
        self.thumbnails_page.setObjectName(u"thumbnails_page")
        self.matches_stack.addWidget(self.thumbnails_page)

        self.verticalLayout.addWidget(self.matches_stack)

        self.pager_layout = QHBoxLayout()
        self.pager_layout.setObjectName(u"pager_layout")

        self.verticalLayout.addLayout(self.pager_layout)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.splitter_2 = QSplitter(self.splitter)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.splitter_2.setHandleWidth(1)
        self.comparator_and_buttons = QWidget(self.splitter_2)
        self.comparator_and_buttons.setObjectName(u"comparator_and_buttons")
        self.comparator_layout = QVBoxLayout(self.comparator_and_buttons)
        self.comparator_layout.setObjectName(u"comparator_layout")
        self.comparator_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.comparator_layout.setContentsMargins(0, 0, 0, 0)
        self.compare_widget = CompareWidget(self.comparator_and_buttons)
        self.compare_widget.setObjectName(u"compare_widget")
        self.compare_widget.setMinimumSize(QSize(300, 100))

        self.comparator_layout.addWidget(self.compare_widget)

        self.action_buttons = QHBoxLayout()
        self.action_buttons.setObjectName(u"action_buttons")
        self.display_multiple_button = QPushButton(self.comparator_and_buttons)
        self.display_multiple_button.setObjectName(u"display_multiple_button")
        icon = QIcon()
        iconThemeName = u"object-columns"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u"", QSize(), QIcon.Normal, QIcon.Off)
        
        self.display_multiple_button.setIcon(icon)
        self.display_multiple_button.setCheckable(True)
        self.display_multiple_button.setChecked(True)
        self.display_multiple_button.setFlat(False)

        self.action_buttons.addWidget(self.display_multiple_button)

        self.display_single_button = QPushButton(self.comparator_and_buttons)
        self.display_single_button.setObjectName(u"display_single_button")
        icon1 = QIcon()
        iconThemeName = u"page-simple"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u"", QSize(), QIcon.Normal, QIcon.Off)
        
        self.display_single_button.setIcon(icon1)
        self.display_single_button.setCheckable(True)

        self.action_buttons.addWidget(self.display_single_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.action_buttons.addItem(self.horizontalSpacer_2)

        self.show_info_button = QPushButton(self.comparator_and_buttons)
        self.show_info_button.setObjectName(u"show_info_button")
        icon2 = QIcon()
        iconThemeName = u"help-about-symbolic"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u"", QSize(), QIcon.Normal, QIcon.Off)
        
        self.show_info_button.setIcon(icon2)
        self.show_info_button.setCheckable(True)
        self.show_info_button.setChecked(True)
        self.show_info_button.setFlat(False)

        self.action_buttons.addWidget(self.show_info_button)

        self.show_zoom_button = QPushButton(self.comparator_and_buttons)
        self.show_zoom_button.setObjectName(u"show_zoom_button")
        icon3 = QIcon()
        iconThemeName = u"label"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u"", QSize(), QIcon.Normal, QIcon.Off)
        
        self.show_zoom_button.setIcon(icon3)
        self.show_zoom_button.setCheckable(True)
        self.show_zoom_button.setChecked(True)

        self.action_buttons.addWidget(self.show_zoom_button)

        self.deleting_mode_button = QPushButton(self.comparator_and_buttons)
        self.deleting_mode_button.setObjectName(u"deleting_mode_button")
        icon4 = QIcon()
        iconThemeName = u"trash-empty"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u"", QSize(), QIcon.Normal, QIcon.Off)
        
        self.deleting_mode_button.setIcon(icon4)
        self.deleting_mode_button.setCheckable(True)

        self.action_buttons.addWidget(self.deleting_mode_button)

        self.delete_button = QPushButton(self.comparator_and_buttons)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setEnabled(False)
        icon5 = QIcon()
        iconThemeName = u"edit-delete"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(u"", QSize(), QIcon.Normal, QIcon.Off)
        
        self.delete_button.setIcon(icon5)

        self.action_buttons.addWidget(self.delete_button)


        self.comparator_layout.addLayout(self.action_buttons)

        self.comparator_layout.setStretch(0, 1)
        self.comparator_layout.setStretch(1, 1)
        self.splitter_2.addWidget(self.comparator_and_buttons)
        self.current_group_list_view = GroupListView(self.splitter_2)
        self.current_group_list_view.setObjectName(u"current_group_list_view")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_group_list_view.sizePolicy().hasHeightForWidth())
        self.current_group_list_view.setSizePolicy(sizePolicy)
        self.current_group_list_view.setBaseSize(QSize(0, 500))
        self.current_group_list_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.current_group_list_view.setAutoScroll(True)
        self.current_group_list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.current_group_list_view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.current_group_list_view.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.current_group_list_view.setMovement(QListView.Static)
        self.current_group_list_view.setFlow(QListView.LeftToRight)
        self.current_group_list_view.setSpacing(5)
        self.splitter_2.addWidget(self.current_group_list_view)
        self.splitter.addWidget(self.splitter_2)

        self.verticalLayout_3.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1145, 35))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.action_quit)
        self.menuHelp.addAction(self.action_show_log)
        self.menuEdit.addAction(self.action_rename)

        self.retranslateUi(MainWindow)

        self.matches_stack.setCurrentIndex(0)
        self.display_multiple_button.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Picture Comparator", None))
        self.action_quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.action_quit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_show_log.setText(QCoreApplication.translate("MainWindow", u"Show log", None))
        self.action_rename.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
#if QT_CONFIG(shortcut)
        self.action_rename.setShortcut(QCoreApplication.translate("MainWindow", u"F2", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.display_multiple_button.setToolTip(QCoreApplication.translate("MainWindow", u"Display images next to each other.", None))
#endif // QT_CONFIG(tooltip)
        self.display_multiple_button.setText(QCoreApplication.translate("MainWindow", u"Multiple", None))
#if QT_CONFIG(tooltip)
        self.display_single_button.setToolTip(QCoreApplication.translate("MainWindow", u"Display single image at the time.", None))
#endif // QT_CONFIG(tooltip)
        self.display_single_button.setText(QCoreApplication.translate("MainWindow", u"Single", None))
        self.show_info_button.setText(QCoreApplication.translate("MainWindow", u"Show info", None))
        self.show_zoom_button.setText(QCoreApplication.translate("MainWindow", u"Show zoom", None))
#if QT_CONFIG(tooltip)
        self.deleting_mode_button.setToolTip(QCoreApplication.translate("MainWindow", u"Enables marking for deletion mode.", None))
#endif // QT_CONFIG(tooltip)
        self.deleting_mode_button.setText(QCoreApplication.translate("MainWindow", u"Makr for deleting", None))
        self.delete_button.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

