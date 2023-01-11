# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_container.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QSizePolicy,
    QTableView, QWidget)

class Ui_DataContainer(object):
    def setupUi(self, DataContainer):
        if not DataContainer.objectName():
            DataContainer.setObjectName(u"DataContainer")
        DataContainer.resize(400, 300)
        self.gridLayout = QGridLayout(DataContainer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.data_view = QTableView(DataContainer)
        self.data_view.setObjectName(u"data_view")
        self.data_view.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.data_view, 0, 0, 1, 1)


        self.retranslateUi(DataContainer)

        QMetaObject.connectSlotsByName(DataContainer)
    # setupUi

    def retranslateUi(self, DataContainer):
        DataContainer.setWindowTitle(QCoreApplication.translate("DataContainer", u"Form", None))
    # retranslateUi

