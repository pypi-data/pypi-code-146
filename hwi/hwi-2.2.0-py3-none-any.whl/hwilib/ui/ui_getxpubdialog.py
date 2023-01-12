# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'getxpubdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_GetXpubDialog(object):
    def setupUi(self, GetXpubDialog):
        if not GetXpubDialog.objectName():
            GetXpubDialog.setObjectName(u"GetXpubDialog")
        GetXpubDialog.resize(1050, 125)
        self.gridLayout = QGridLayout(GetXpubDialog)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.buttonBox = QDialogButtonBox(GetXpubDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMaximumSize(QSize(200, 16777215))
        self.buttonBox.setFocusPolicy(Qt.NoFocus)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)

        self.path_label = QLabel(GetXpubDialog)
        self.path_label.setObjectName(u"path_label")

        self.gridLayout.addWidget(self.path_label, 0, 0, 1, 1)

        self.xpub_textedit = QTextEdit(GetXpubDialog)
        self.xpub_textedit.setObjectName(u"xpub_textedit")
        self.xpub_textedit.setMinimumSize(QSize(0, 30))
        self.xpub_textedit.setMaximumSize(QSize(16777215, 30))
        self.xpub_textedit.setLineWrapMode(QTextEdit.NoWrap)
        self.xpub_textedit.setReadOnly(True)

        self.gridLayout.addWidget(self.xpub_textedit, 1, 1, 1, 2)

        self.path_lineedit = QLineEdit(GetXpubDialog)
        self.path_lineedit.setObjectName(u"path_lineedit")
        self.path_lineedit.setMinimumSize(QSize(200, 30))

        self.gridLayout.addWidget(self.path_lineedit, 0, 1, 1, 1)

        self.getxpub_button = QPushButton(GetXpubDialog)
        self.getxpub_button.setObjectName(u"getxpub_button")
        self.getxpub_button.setMaximumSize(QSize(200, 16777215))

        self.gridLayout.addWidget(self.getxpub_button, 0, 2, 1, 1)

        self.xpub_label = QLabel(GetXpubDialog)
        self.xpub_label.setObjectName(u"xpub_label")
        self.xpub_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.xpub_label, 1, 0, 1, 1)


        self.retranslateUi(GetXpubDialog)

        QMetaObject.connectSlotsByName(GetXpubDialog)
    # setupUi

    def retranslateUi(self, GetXpubDialog):
        GetXpubDialog.setWindowTitle(QCoreApplication.translate("GetXpubDialog", u"Dialog", None))
        self.path_label.setText(QCoreApplication.translate("GetXpubDialog", u"Derivation Path", None))
        self.getxpub_button.setText(QCoreApplication.translate("GetXpubDialog", u"Get xpub", None))
        self.xpub_label.setText(QCoreApplication.translate("GetXpubDialog", u"xpub", None))
    # retranslateUi

