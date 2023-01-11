# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'open_csv_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QRadioButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_OpenCSVDialog(object):
    def setupUi(self, OpenCSVDialog):
        if not OpenCSVDialog.objectName():
            OpenCSVDialog.setObjectName(u"OpenCSVDialog")
        OpenCSVDialog.resize(480, 328)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OpenCSVDialog.sizePolicy().hasHeightForWidth())
        OpenCSVDialog.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(OpenCSVDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 32, -1, -1)
        self.groupBox = QGroupBox(OpenCSVDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radio_comma = QRadioButton(self.groupBox)
        self.radio_comma.setObjectName(u"radio_comma")
        self.radio_comma.setChecked(True)

        self.verticalLayout.addWidget(self.radio_comma)

        self.radio_semicolon = QRadioButton(self.groupBox)
        self.radio_semicolon.setObjectName(u"radio_semicolon")

        self.verticalLayout.addWidget(self.radio_semicolon)

        self.radio_space = QRadioButton(self.groupBox)
        self.radio_space.setObjectName(u"radio_space")

        self.verticalLayout.addWidget(self.radio_space)

        self.radio_tab = QRadioButton(self.groupBox)
        self.radio_tab.setObjectName(u"radio_tab")

        self.verticalLayout.addWidget(self.radio_tab)

        self.radio_other = QRadioButton(self.groupBox)
        self.radio_other.setObjectName(u"radio_other")

        self.verticalLayout.addWidget(self.radio_other)

        self.textbox_custom_splitter = QLineEdit(self.groupBox)
        self.textbox_custom_splitter.setObjectName(u"textbox_custom_splitter")
        self.textbox_custom_splitter.setEnabled(False)
        sizePolicy.setHeightForWidth(self.textbox_custom_splitter.sizePolicy().hasHeightForWidth())
        self.textbox_custom_splitter.setSizePolicy(sizePolicy)
        self.textbox_custom_splitter.setMaxLength(1)

        self.verticalLayout.addWidget(self.textbox_custom_splitter)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(OpenCSVDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.widget = QWidget(OpenCSVDialog)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.formLayout_2 = QFormLayout(self.widget)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.combo_header_type = QComboBox(self.widget)
        self.combo_header_type.addItem("")
        self.combo_header_type.addItem("")
        self.combo_header_type.addItem("")
        self.combo_header_type.setObjectName(u"combo_header_type")
        self.combo_header_type.setEditable(False)
        self.combo_header_type.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.combo_header_type)


        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 1)


        self.retranslateUi(OpenCSVDialog)
        self.buttonBox.accepted.connect(OpenCSVDialog.accept)
        self.buttonBox.rejected.connect(OpenCSVDialog.reject)

        QMetaObject.connectSlotsByName(OpenCSVDialog)
    # setupUi

    def retranslateUi(self, OpenCSVDialog):
        OpenCSVDialog.setWindowTitle(QCoreApplication.translate("OpenCSVDialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("OpenCSVDialog", u"Select Splitter", None))
        self.radio_comma.setText(QCoreApplication.translate("OpenCSVDialog", u"Comma (,)", None))
        self.radio_semicolon.setText(QCoreApplication.translate("OpenCSVDialog", u"Semi Colon (;)", None))
        self.radio_space.setText(QCoreApplication.translate("OpenCSVDialog", u"Space", None))
        self.radio_tab.setText(QCoreApplication.translate("OpenCSVDialog", u"Tab", None))
        self.radio_other.setText(QCoreApplication.translate("OpenCSVDialog", u"Other:", None))
        self.textbox_custom_splitter.setText(QCoreApplication.translate("OpenCSVDialog", u",", None))
        self.textbox_custom_splitter.setPlaceholderText(QCoreApplication.translate("OpenCSVDialog", u"Input Splitter...", None))
        self.label.setText(QCoreApplication.translate("OpenCSVDialog", u"Header", None))
        self.combo_header_type.setItemText(0, QCoreApplication.translate("OpenCSVDialog", u"Auto (Infer)", None))
        self.combo_header_type.setItemText(1, QCoreApplication.translate("OpenCSVDialog", u"First Row", None))
        self.combo_header_type.setItemText(2, QCoreApplication.translate("OpenCSVDialog", u"No Header", None))

    # retranslateUi

