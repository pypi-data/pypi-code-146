# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'diff_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_diff_dialog(object):
    def setupUi(self, diff_dialog):
        if not diff_dialog.objectName():
            diff_dialog.setObjectName(u"diff_dialog")
        diff_dialog.resize(715, 460)
        self.verticalLayout = QVBoxLayout(diff_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.diff_dialog_text = QTextBrowser(diff_dialog)
        self.diff_dialog_text.setObjectName(u"diff_dialog_text")

        self.verticalLayout.addWidget(self.diff_dialog_text)

        self.diff_dialog_buttons = QDialogButtonBox(diff_dialog)
        self.diff_dialog_buttons.setObjectName(u"diff_dialog_buttons")
        self.diff_dialog_buttons.setOrientation(Qt.Horizontal)
        self.diff_dialog_buttons.setStandardButtons(QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.diff_dialog_buttons)


        self.retranslateUi(diff_dialog)
        self.diff_dialog_buttons.accepted.connect(diff_dialog.accept)
        self.diff_dialog_buttons.rejected.connect(diff_dialog.reject)

        QMetaObject.connectSlotsByName(diff_dialog)
    # setupUi

    def retranslateUi(self, diff_dialog):
        diff_dialog.setWindowTitle(QCoreApplication.translate("diff_dialog", u"Diff", None))
    # retranslateUi

