# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sendpindialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SendPinDialog(object):
    def setupUi(self, SendPinDialog):
        if not SendPinDialog.objectName():
            SendPinDialog.setObjectName(u"SendPinDialog")
        SendPinDialog.resize(250, 250)
        self.verticalLayout = QVBoxLayout(SendPinDialog)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.pin_lineedit = QLineEdit(SendPinDialog)
        self.pin_lineedit.setObjectName(u"pin_lineedit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.pin_lineedit.sizePolicy().hasHeightForWidth())
        self.pin_lineedit.setSizePolicy(sizePolicy)
        self.pin_lineedit.setMinimumSize(QSize(0, 30))
        self.pin_lineedit.setReadOnly(False)

        self.verticalLayout.addWidget(self.pin_lineedit)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 0)
        self.p7_button = QPushButton(SendPinDialog)
        self.p7_button.setObjectName(u"p7_button")

        self.gridLayout.addWidget(self.p7_button, 0, 0, 1, 1)

        self.p1_button = QPushButton(SendPinDialog)
        self.p1_button.setObjectName(u"p1_button")

        self.gridLayout.addWidget(self.p1_button, 2, 0, 1, 1)

        self.p4_button = QPushButton(SendPinDialog)
        self.p4_button.setObjectName(u"p4_button")

        self.gridLayout.addWidget(self.p4_button, 1, 0, 1, 1)

        self.p9_button = QPushButton(SendPinDialog)
        self.p9_button.setObjectName(u"p9_button")

        self.gridLayout.addWidget(self.p9_button, 0, 2, 1, 1)

        self.p3_button = QPushButton(SendPinDialog)
        self.p3_button.setObjectName(u"p3_button")

        self.gridLayout.addWidget(self.p3_button, 2, 2, 1, 1)

        self.p6_button = QPushButton(SendPinDialog)
        self.p6_button.setObjectName(u"p6_button")

        self.gridLayout.addWidget(self.p6_button, 1, 2, 1, 1)

        self.p2_button = QPushButton(SendPinDialog)
        self.p2_button.setObjectName(u"p2_button")

        self.gridLayout.addWidget(self.p2_button, 2, 1, 1, 1)

        self.p5_button = QPushButton(SendPinDialog)
        self.p5_button.setObjectName(u"p5_button")

        self.gridLayout.addWidget(self.p5_button, 1, 1, 1, 1)

        self.p8_button = QPushButton(SendPinDialog)
        self.p8_button.setObjectName(u"p8_button")

        self.gridLayout.addWidget(self.p8_button, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(SendPinDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SendPinDialog)
        self.buttonBox.accepted.connect(SendPinDialog.accept)
        self.buttonBox.rejected.connect(SendPinDialog.reject)

        QMetaObject.connectSlotsByName(SendPinDialog)
    # setupUi

    def retranslateUi(self, SendPinDialog):
        SendPinDialog.setWindowTitle(QCoreApplication.translate("SendPinDialog", u"Dialog", None))
        self.p7_button.setText(QCoreApplication.translate("SendPinDialog", u"?", None))
        self.p1_button.setText(QCoreApplication.translate("SendPinDialog", u"?", None))
        self.p4_button.setText(QCoreApplication.translate("SendPinDialog", u"?", None))
        self.p9_button.setText(QCoreApplication.translate("SendPinDialog", u"?", None))
        self.p3_button.setText(QCoreApplication.translate("SendPinDialog", u"?", None))
        self.p6_button.setText(QCoreApplication.translate("SendPinDialog", u"?", None))
        self.p2_button.setText(QCoreApplication.translate("SendPinDialog", u"?", None))
        self.p5_button.setText(QCoreApplication.translate("SendPinDialog", u"?", None))
        self.p8_button.setText(QCoreApplication.translate("SendPinDialog", u"?", None))
    # retranslateUi

