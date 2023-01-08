# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QSizePolicy,
    QTableView, QVBoxLayout, QWidget)

class Ui_LogWidget(object):
    def setupUi(self, LogWidget):
        if not LogWidget.objectName():
            LogWidget.setObjectName(u"LogWidget")
        LogWidget.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(LogWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.log_table_view = QTableView(LogWidget)
        self.log_table_view.setObjectName(u"log_table_view")
        self.log_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.log_table_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.log_table_view.setShowGrid(False)
        self.log_table_view.setGridStyle(Qt.DashLine)
        self.log_table_view.setWordWrap(False)
        self.log_table_view.horizontalHeader().setVisible(False)
        self.log_table_view.horizontalHeader().setMinimumSectionSize(60)
        self.log_table_view.horizontalHeader().setDefaultSectionSize(200)
        self.log_table_view.horizontalHeader().setStretchLastSection(True)
        self.log_table_view.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.log_table_view)


        self.retranslateUi(LogWidget)

        QMetaObject.connectSlotsByName(LogWidget)
    # setupUi

    def retranslateUi(self, LogWidget):
        LogWidget.setWindowTitle(QCoreApplication.translate("LogWidget", u"Logs", None))
    # retranslateUi

