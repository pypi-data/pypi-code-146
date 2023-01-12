# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'signmessagedialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SignMessageDialog(object):
    def setupUi(self, SignMessageDialog):
        if not SignMessageDialog.objectName():
            SignMessageDialog.setObjectName(u"SignMessageDialog")
        SignMessageDialog.resize(600, 260)
        self.gridLayout = QGridLayout(SignMessageDialog)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.msg_textedit = QPlainTextEdit(SignMessageDialog)
        self.msg_textedit.setObjectName(u"msg_textedit")
        self.msg_textedit.setMinimumSize(QSize(0, 50))
        self.msg_textedit.setMaximumSize(QSize(16777215, 100))

        self.gridLayout.addWidget(self.msg_textedit, 0, 1, 1, 2)

        self.path_lineedit = QLineEdit(SignMessageDialog)
        self.path_lineedit.setObjectName(u"path_lineedit")
        self.path_lineedit.setMinimumSize(QSize(300, 30))
        self.path_lineedit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.path_lineedit, 1, 1, 1, 1)

        self.label_3 = QLabel(SignMessageDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label = QLabel(SignMessageDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.signmsg_button = QPushButton(SignMessageDialog)
        self.signmsg_button.setObjectName(u"signmsg_button")
        self.signmsg_button.setMaximumSize(QSize(150, 16777215))
        self.signmsg_button.setAutoDefault(False)

        self.gridLayout.addWidget(self.signmsg_button, 1, 2, 1, 1)

        self.sig_textedit = QPlainTextEdit(SignMessageDialog)
        self.sig_textedit.setObjectName(u"sig_textedit")
        self.sig_textedit.setMinimumSize(QSize(0, 30))
        self.sig_textedit.setMaximumSize(QSize(16777215, 50))
        self.sig_textedit.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.sig_textedit, 2, 1, 1, 2)

        self.label_2 = QLabel(SignMessageDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(SignMessageDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(80, 0))
        self.buttonBox.setMaximumSize(QSize(80, 16777215))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1, Qt.AlignRight)


        self.retranslateUi(SignMessageDialog)
        self.buttonBox.accepted.connect(SignMessageDialog.accept)
        self.buttonBox.rejected.connect(SignMessageDialog.reject)

        self.signmsg_button.setDefault(True)


        QMetaObject.connectSlotsByName(SignMessageDialog)
    # setupUi

    def retranslateUi(self, SignMessageDialog):
        SignMessageDialog.setWindowTitle(QCoreApplication.translate("SignMessageDialog", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("SignMessageDialog", u"Signature", None))
        self.label.setText(QCoreApplication.translate("SignMessageDialog", u"Message", None))
        self.signmsg_button.setText(QCoreApplication.translate("SignMessageDialog", u"Sign Message", None))
        self.label_2.setText(QCoreApplication.translate("SignMessageDialog", u"Derivation Path", None))
    # retranslateUi

