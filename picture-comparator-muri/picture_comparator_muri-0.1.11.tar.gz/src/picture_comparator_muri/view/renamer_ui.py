# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'renamer.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from picture_comparator_muri.view.renamer_file_tree_view import RenamerFileTreeView

class Ui_Renamer(object):
    def setupUi(self, Renamer):
        if not Renamer.objectName():
            Renamer.setObjectName(u"Renamer")
        Renamer.resize(1000, 468)
        self.verticalLayout = QVBoxLayout(Renamer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Renamer)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.show_selected_button = QPushButton(Renamer)
        self.show_selected_button.setObjectName(u"show_selected_button")
        self.show_selected_button.setCheckable(True)
        self.show_selected_button.setChecked(True)

        self.horizontalLayout.addWidget(self.show_selected_button)

        self.show_group_button = QPushButton(Renamer)
        self.show_group_button.setObjectName(u"show_group_button")
        self.show_group_button.setCheckable(True)

        self.horizontalLayout.addWidget(self.show_group_button)

        self.show_images_button = QPushButton(Renamer)
        self.show_images_button.setObjectName(u"show_images_button")
        self.show_images_button.setCheckable(True)

        self.horizontalLayout.addWidget(self.show_images_button)

        self.show_all_button = QPushButton(Renamer)
        self.show_all_button.setObjectName(u"show_all_button")
        self.show_all_button.setCheckable(True)

        self.horizontalLayout.addWidget(self.show_all_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.show_hidden_button = QPushButton(Renamer)
        self.show_hidden_button.setObjectName(u"show_hidden_button")
        self.show_hidden_button.setCheckable(True)

        self.horizontalLayout.addWidget(self.show_hidden_button)

        self.enable_all_button = QPushButton(Renamer)
        self.enable_all_button.setObjectName(u"enable_all_button")
        self.enable_all_button.setCheckable(True)

        self.horizontalLayout.addWidget(self.enable_all_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.file_view = RenamerFileTreeView(Renamer)
        self.file_view.setObjectName(u"file_view")
        self.file_view.setAcceptDrops(True)
        self.file_view.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.file_view.setDragEnabled(True)
        self.file_view.setDragDropMode(QAbstractItemView.InternalMove)
        self.file_view.setDefaultDropAction(Qt.MoveAction)
        self.file_view.setSortingEnabled(False)
        self.file_view.header().setVisible(True)
        self.file_view.header().setDefaultSectionSize(200)

        self.verticalLayout.addWidget(self.file_view)

        self.buttonBox = QDialogButtonBox(Renamer)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Renamer)
        self.buttonBox.accepted.connect(Renamer.accept)
        self.buttonBox.rejected.connect(Renamer.reject)

        QMetaObject.connectSlotsByName(Renamer)
    # setupUi

    def retranslateUi(self, Renamer):
        Renamer.setWindowTitle(QCoreApplication.translate("Renamer", u"Rename Files", None))
        self.label.setText(QCoreApplication.translate("Renamer", u"Show", None))
        self.show_selected_button.setText(QCoreApplication.translate("Renamer", u"Selected", None))
        self.show_group_button.setText(QCoreApplication.translate("Renamer", u"Group", None))
        self.show_images_button.setText(QCoreApplication.translate("Renamer", u"All Images", None))
        self.show_all_button.setText(QCoreApplication.translate("Renamer", u"All Files", None))
        self.show_hidden_button.setText(QCoreApplication.translate("Renamer", u"Show Hidden", None))
#if QT_CONFIG(tooltip)
        self.enable_all_button.setToolTip(QCoreApplication.translate("Renamer", u"Allow editing of all visible files.", None))
#endif // QT_CONFIG(tooltip)
        self.enable_all_button.setText(QCoreApplication.translate("Renamer", u"Enable All", None))
    # retranslateUi

