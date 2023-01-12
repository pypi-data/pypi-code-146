# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'signpsbtdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SignPSBTDialog(object):
    def setupUi(self, SignPSBTDialog):
        if not SignPSBTDialog.objectName():
            SignPSBTDialog.setObjectName(u"SignPSBTDialog")
        SignPSBTDialog.resize(650, 400)
        self.gridLayout = QGridLayout(SignPSBTDialog)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.label = QLabel(SignPSBTDialog)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label_2 = QLabel(SignPSBTDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)


        self.gridLayout.addLayout(self.verticalLayout, 3, 0, 1, 1)

        self.psbt_in_textedit = QPlainTextEdit(SignPSBTDialog)
        self.psbt_in_textedit.setObjectName(u"psbt_in_textedit")
        self.psbt_in_textedit.setMinimumSize(QSize(300, 120))

        self.gridLayout.addWidget(self.psbt_in_textedit, 1, 2, 1, 1)

        self.psbt_out_textedit = QPlainTextEdit(SignPSBTDialog)
        self.psbt_out_textedit.setObjectName(u"psbt_out_textedit")
        self.psbt_out_textedit.setMinimumSize(QSize(300, 120))
        self.psbt_out_textedit.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.psbt_out_textedit, 3, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.sign_psbt_button = QPushButton(SignPSBTDialog)
        self.sign_psbt_button.setObjectName(u"sign_psbt_button")
        self.sign_psbt_button.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.sign_psbt_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(SignPSBTDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.gridLayout.addWidget(self.buttonBox, 4, 2, 1, 1)


        self.retranslateUi(SignPSBTDialog)
        self.buttonBox.accepted.connect(SignPSBTDialog.accept)
        self.buttonBox.rejected.connect(SignPSBTDialog.reject)

        self.sign_psbt_button.setDefault(True)


        QMetaObject.connectSlotsByName(SignPSBTDialog)
    # setupUi

    def retranslateUi(self, SignPSBTDialog):
        SignPSBTDialog.setWindowTitle(QCoreApplication.translate("SignPSBTDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("SignPSBTDialog", u"PSBT To Sign", None))
        self.label_2.setText(QCoreApplication.translate("SignPSBTDialog", u"PSBT Result", None))
        self.sign_psbt_button.setText(QCoreApplication.translate("SignPSBTDialog", u"Sign PSBT", None))
    # retranslateUi

