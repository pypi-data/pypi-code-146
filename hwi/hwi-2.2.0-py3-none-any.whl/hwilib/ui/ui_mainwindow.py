# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(650, 400)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(130, 20))
        self.label.setMaximumSize(QSize(200, 20))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)

        self.enumerate_combobox = QComboBox(self.centralwidget)
        self.enumerate_combobox.setObjectName(u"enumerate_combobox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.enumerate_combobox.sizePolicy().hasHeightForWidth())
        self.enumerate_combobox.setSizePolicy(sizePolicy1)
        self.enumerate_combobox.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.enumerate_combobox)

        self.enumerate_refresh_button = QPushButton(self.centralwidget)
        self.enumerate_refresh_button.setObjectName(u"enumerate_refresh_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.enumerate_refresh_button.sizePolicy().hasHeightForWidth())
        self.enumerate_refresh_button.setSizePolicy(sizePolicy2)
        self.enumerate_refresh_button.setMaximumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.enumerate_refresh_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.setpass_button = QPushButton(self.centralwidget)
        self.setpass_button.setObjectName(u"setpass_button")

        self.gridLayout.addWidget(self.setpass_button, 2, 0, 1, 1)

        self.getxpub_button = QPushButton(self.centralwidget)
        self.getxpub_button.setObjectName(u"getxpub_button")
        self.getxpub_button.setEnabled(False)

        self.gridLayout.addWidget(self.getxpub_button, 3, 0, 1, 1)

        self.signmsg_button = QPushButton(self.centralwidget)
        self.signmsg_button.setObjectName(u"signmsg_button")
        self.signmsg_button.setEnabled(False)

        self.gridLayout.addWidget(self.signmsg_button, 3, 2, 1, 1)

        self.signtx_button = QPushButton(self.centralwidget)
        self.signtx_button.setObjectName(u"signtx_button")
        self.signtx_button.setEnabled(False)

        self.gridLayout.addWidget(self.signtx_button, 3, 1, 1, 1)

        self.getkeypool_opts_button = QPushButton(self.centralwidget)
        self.getkeypool_opts_button.setObjectName(u"getkeypool_opts_button")
        self.getkeypool_opts_button.setEnabled(False)

        self.gridLayout.addWidget(self.getkeypool_opts_button, 2, 2, 1, 1)

        self.sendpin_button = QPushButton(self.centralwidget)
        self.sendpin_button.setObjectName(u"sendpin_button")
        self.sendpin_button.setEnabled(False)

        self.gridLayout.addWidget(self.sendpin_button, 2, 1, 1, 1)

        self.toggle_passphrase_button = QPushButton(self.centralwidget)
        self.toggle_passphrase_button.setObjectName(u"toggle_passphrase_button")
        self.toggle_passphrase_button.setEnabled(False)

        self.gridLayout.addWidget(self.toggle_passphrase_button, 4, 1, 1, 1)

        self.display_addr_button = QPushButton(self.centralwidget)
        self.display_addr_button.setObjectName(u"display_addr_button")
        self.display_addr_button.setEnabled(False)

        self.gridLayout.addWidget(self.display_addr_button, 4, 0, 1, 1)

        self.actions_label = QLabel(self.centralwidget)
        self.actions_label.setObjectName(u"actions_label")
        self.actions_label.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.actions_label.sizePolicy().hasHeightForWidth())
        self.actions_label.setSizePolicy(sizePolicy3)
        self.actions_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.actions_label, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)
        self.keypool_label = QLabel(self.centralwidget)
        self.keypool_label.setObjectName(u"keypool_label")
        self.keypool_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.keypool_label, 0, 0, 1, 1)

        self.keypool_textedit = QPlainTextEdit(self.centralwidget)
        self.keypool_textedit.setObjectName(u"keypool_textedit")
        self.keypool_textedit.setReadOnly(True)

        self.gridLayout_2.addWidget(self.keypool_textedit, 0, 1, 1, 1)

        self.desc_label = QLabel(self.centralwidget)
        self.desc_label.setObjectName(u"desc_label")
        self.desc_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.desc_label, 1, 0, 1, 1)

        self.desc_textedit = QPlainTextEdit(self.centralwidget)
        self.desc_textedit.setObjectName(u"desc_textedit")
        self.desc_textedit.setReadOnly(True)

        self.gridLayout_2.addWidget(self.desc_textedit, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Connected devices", None))
        self.enumerate_refresh_button.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.setpass_button.setText(QCoreApplication.translate("MainWindow", u"Set Passphrase", None))
        self.getxpub_button.setText(QCoreApplication.translate("MainWindow", u"Get an xpub", None))
        self.signmsg_button.setText(QCoreApplication.translate("MainWindow", u"Sign Message", None))
        self.signtx_button.setText(QCoreApplication.translate("MainWindow", u"Sign PSBT", None))
#if QT_CONFIG(tooltip)
        self.getkeypool_opts_button.setToolTip(QCoreApplication.translate("MainWindow", u"Change the options used for getkeypool", None))
#endif // QT_CONFIG(tooltip)
        self.getkeypool_opts_button.setText(QCoreApplication.translate("MainWindow", u"Change getkeypool options", None))
        self.sendpin_button.setText(QCoreApplication.translate("MainWindow", u"Send Pin", None))
        self.toggle_passphrase_button.setText(QCoreApplication.translate("MainWindow", u"Toggle Passphrase", None))
        self.display_addr_button.setText(QCoreApplication.translate("MainWindow", u"Display Address", None))
        self.actions_label.setText(QCoreApplication.translate("MainWindow", u"Actions", None))
        self.keypool_label.setText(QCoreApplication.translate("MainWindow", u"Keypool", None))
        self.desc_label.setText(QCoreApplication.translate("MainWindow", u"Descriptors", None))
    # retranslateUi

