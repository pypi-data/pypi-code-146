# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'displayaddressdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DisplayAddressDialog(object):
    def setupUi(self, DisplayAddressDialog):
        if not DisplayAddressDialog.objectName():
            DisplayAddressDialog.setObjectName(u"DisplayAddressDialog")
        DisplayAddressDialog.resize(500, 200)
        self.gridLayout = QGridLayout(DisplayAddressDialog)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.type_groupbox = QGroupBox(DisplayAddressDialog)
        self.type_groupbox.setObjectName(u"type_groupbox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_groupbox.sizePolicy().hasHeightForWidth())
        self.type_groupbox.setSizePolicy(sizePolicy)
        self.type_groupbox.setMinimumSize(QSize(300, 50))
        self.type_groupbox.setMaximumSize(QSize(500, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.type_groupbox)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.sh_wpkh_radio = QRadioButton(self.type_groupbox)
        self.sh_wpkh_radio.setObjectName(u"sh_wpkh_radio")
        self.sh_wpkh_radio.setChecked(True)

        self.horizontalLayout_2.addWidget(self.sh_wpkh_radio)

        self.wpkh_radio = QRadioButton(self.type_groupbox)
        self.wpkh_radio.setObjectName(u"wpkh_radio")

        self.horizontalLayout_2.addWidget(self.wpkh_radio)

        self.radioButton = QRadioButton(self.type_groupbox)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_2.addWidget(self.radioButton)


        self.gridLayout.addWidget(self.type_groupbox, 1, 0, 1, 2)

        self.label_2 = QLabel(DisplayAddressDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.address_lineedit = QLineEdit(DisplayAddressDialog)
        self.address_lineedit.setObjectName(u"address_lineedit")
        self.address_lineedit.setMinimumSize(QSize(100, 30))
        self.address_lineedit.setReadOnly(True)

        self.gridLayout.addWidget(self.address_lineedit, 2, 1, 1, 2)

        self.path_lineedit = QLineEdit(DisplayAddressDialog)
        self.path_lineedit.setObjectName(u"path_lineedit")
        self.path_lineedit.setMinimumSize(QSize(200, 30))

        self.gridLayout.addWidget(self.path_lineedit, 0, 1, 1, 2)

        self.go_button = QPushButton(DisplayAddressDialog)
        self.go_button.setObjectName(u"go_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.go_button.sizePolicy().hasHeightForWidth())
        self.go_button.setSizePolicy(sizePolicy1)
        self.go_button.setMinimumSize(QSize(40, 40))
        self.go_button.setMaximumSize(QSize(50, 40))
        self.go_button.setAutoDefault(False)

        self.gridLayout.addWidget(self.go_button, 1, 2, 1, 1, Qt.AlignHCenter)

        self.buttonBox = QDialogButtonBox(DisplayAddressDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 25))
        self.buttonBox.setMaximumSize(QSize(80, 25))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)

        self.label = QLabel(DisplayAddressDialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.retranslateUi(DisplayAddressDialog)
        self.buttonBox.accepted.connect(DisplayAddressDialog.accept)
        self.buttonBox.rejected.connect(DisplayAddressDialog.reject)

        self.go_button.setDefault(True)


        QMetaObject.connectSlotsByName(DisplayAddressDialog)
    # setupUi

    def retranslateUi(self, DisplayAddressDialog):
        DisplayAddressDialog.setWindowTitle(QCoreApplication.translate("DisplayAddressDialog", u"Dialog", None))
        self.type_groupbox.setTitle("")
        self.sh_wpkh_radio.setText(QCoreApplication.translate("DisplayAddressDialog", u"P2SH-P2WPKH", None))
        self.wpkh_radio.setText(QCoreApplication.translate("DisplayAddressDialog", u"P2WPKH", None))
        self.radioButton.setText(QCoreApplication.translate("DisplayAddressDialog", u"P2PKH", None))
        self.label_2.setText(QCoreApplication.translate("DisplayAddressDialog", u"Address", None))
        self.go_button.setText(QCoreApplication.translate("DisplayAddressDialog", u"Go", None))
        self.label.setText(QCoreApplication.translate("DisplayAddressDialog", u"Derivation Path", None))
    # retranslateUi

