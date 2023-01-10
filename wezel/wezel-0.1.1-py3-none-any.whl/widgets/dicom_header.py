"""This module contains custom widgets for the display DICOM Series Metadata in a table."""


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFileDialog, QLineEdit, QApplication,                           
        QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem,
        QPushButton, QLabel,  QHeaderView,  QTableWidget,  QAbstractItemView, QScrollArea)

import pydicom
import pandas as pd
from wezel import MainWidget


localStyleSheet = """
    QTableWidget {
    alternate-background-color: #dce2f2;background-color: #b6bdd1;
    } 
    """

_localStyleSheet = """
    QTableWidget {
    alternate-background-color: #dce2f2;background-color: #b6bdd1;
                                            }           
    QTableWidget::item {
        border: 1px solid rgba(68, 119, 170, 150);
        }

    QHeaderView, QHeaderView::section {
        background-color: rgba(125, 125, 125, 125);
        font-weight: bold;
        font-size: x-large;}

        QPushButton { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #CCCCBB, stop: 1 #FFFFFF);
                             border-width: 3px;
                             margin: 1px;
                             border-style: solid;
                             border-color: rgb(10, 10, 10);
                             border-radius: 5px;
                             text-align: centre;
                             color: black;
                             font-weight: bold;
                             font-size: 9pt;
                             padding: 3px;} 

                QPushButton:hover {
                                   background-color: rgb(175, 175, 175);
                                   border: 1px solid red;
                                   }
                                   
                QPushButton:pressed {background-color: rgb(112, 112, 112);}

                QLabel {background: transparent;}
                QScrollArea{background: transparent;}
                QWidget{background: transparent;}
            """


class ScrollLabel(QScrollArea):
    """
    A custom composite widget, a label with a vertical scrollbar,
    for the display of long text strings in the metadata table. 
    """
    def __init__(self):
        QScrollArea.__init__(self)
        self.setWidgetResizable(True)

        centralWidget = QWidget(self)
        self.setWidget(centralWidget)

        verticalLayout = QVBoxLayout()
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout.setSpacing(0)
        centralWidget.setLayout(verticalLayout)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        verticalLayout.addWidget(self.label)

   
    def setText(self, text):
        self.label.setText(text)


class SeriesViewerMetaData(MainWidget):
    """Display DICOM Series Metadata in a table."""

    rowHeight = 4

    def __init__(self, series):  
        """
        Constructs the composite widget for displaying a table of DICOM series metadata
        """
        super().__init__()
        #Get the DICOM object for the first image in the series
        #The DICOM object for an image contains the metadata for the whole series
        instances = series.children()
        if instances == []:
            self.setError('Series ' + series.label() + ' is empty. \n\n Nothing to show here..')
            return 
        self._objectDICOM = instances[0].get_dataset()
        self.series = series

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
        self.setAttribute(Qt.WA_DeleteOnClose)

        #Add table to display rows of metadata
        self.tableWidget = QTableWidget()
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget.horizontalScrollBar().setEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)
        #self.tableWidget.setStyleSheet(localStyleSheet) 
        #self.tableWidget.setShowGrid(True)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)
        self.populateTable()

        # Add Search Bar
        self.searchField = QLineEdit()
        self.searchField.textEdited.connect(lambda x=self.searchField.text(): self.searchTable( x))
        
        # Add export to Excel/CSV buttons
        self.export_csv_button = QPushButton('&Export To CSV', clicked=lambda: self.exportToFile(self))

        self.horizontalBox = QHBoxLayout()
        self.horizontalBox.setContentsMargins(0, 0, 0, 0)
        self.horizontalBox.setSpacing(0)
        self.horizontalBox.addWidget(self.searchField)
        self.horizontalBox.addWidget(self.export_csv_button)

        self.layout().addLayout(self.horizontalBox)
        self.layout().addWidget(self.tableWidget) 
        
    
    def resizeColumnsToContents(self):
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode(QHeaderView.AdjustToContentsOnFirstShow))


    def createScrollableLabel(self, rowPosition, valueMetadata):
        scrollableLabel = ScrollLabel()
        scrollableLabel.setText(valueMetadata)
        self.tableWidget.setCellWidget(rowPosition, 3, scrollableLabel)
        self.tableWidget.resizeRowToContents(rowPosition)


    def populateTable(self):
        """Builds a Table View displaying DICOM image metadata
        as Tag, name, VR & Value"""
    
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.createHeaderRow()
        
        if self._objectDICOM:
            # Loop through the DICOM group (0002, XXXX) first
            for meta_element in self._objectDICOM.file_meta:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                self.tableWidget.setRowHeight(rowPosition, self.rowHeight)
                self.tableWidget.setItem(rowPosition , 0, 
                                QTableWidgetItem(str(meta_element.tag)))
                self.tableWidget.setItem(rowPosition , 1, 
                                QTableWidgetItem(meta_element.name))
                self.tableWidget.setItem(rowPosition , 2, 
                                QTableWidgetItem(meta_element.VR))

                if meta_element.VR == "OW" or meta_element.VR == "OB" or meta_element.VR == "UN":
                    try:
                        valueMetadata = str(list(meta_element))
                    except:
                        valueMetadata = str(meta_element.value)
                else:
                    valueMetadata = str(meta_element.value)

                if meta_element.VR == "OB" or meta_element.VR == "OW":
                    self.createScrollableLabel(rowPosition, valueMetadata)
                elif meta_element.VR == "SQ":
                    self.iterateSequenceTag(self.tableWidget, meta_element)
                else:
                    self.tableWidget.setItem(rowPosition , 3, QTableWidgetItem(valueMetadata))
            
            for data_element in self._objectDICOM:
                # Exclude pixel data from metadata listing
                if data_element.name == 'Pixel Data':
                    continue
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                self.tableWidget.setRowHeight(rowPosition, self.rowHeight)
                self.tableWidget.setItem(rowPosition , 0, 
                                QTableWidgetItem(str(data_element.tag)))
                self.tableWidget.setItem(rowPosition , 1, 
                                QTableWidgetItem(data_element.name))
                self.tableWidget.setItem(rowPosition , 2, 
                                QTableWidgetItem(data_element.VR))

                if data_element.VR == "OW" or data_element.VR == "OB" or data_element.VR == "UN":
                    try:
                        valueMetadata = str(list(data_element))
                    except:
                        try:
                            valueMetadata = str(data_element.value.decode('utf-8'))
                        except:
                            valueMetadata = str(data_element.value)
                else:
                    valueMetadata = str(data_element.value)

                if data_element.VR == "OB" or data_element.VR == "OW":
                    self.createScrollableLabel(rowPosition, valueMetadata)
                elif data_element.VR == "SQ":
                    self.iterateSequenceTag(self.tableWidget, data_element)
                else:
                    self.tableWidget.setItem(rowPosition , 3, QTableWidgetItem(valueMetadata))
        self.resizeColumnsToContents()
        QApplication.restoreOverrideCursor()



    def createHeaderRow(self):
        headerItem = QTableWidgetItem(QTableWidgetItem("Tag\n")) 
        headerItem.setTextAlignment(Qt.AlignLeft)
        self.tableWidget.setHorizontalHeaderItem(0,headerItem)
        headerItem = QTableWidgetItem(QTableWidgetItem("Name \n")) 
        headerItem.setTextAlignment(Qt.AlignLeft)
        self.tableWidget.setHorizontalHeaderItem(1, headerItem)
        headerItem = QTableWidgetItem(QTableWidgetItem("VR \n")) 
        headerItem.setTextAlignment(Qt.AlignLeft)
        self.tableWidget.setHorizontalHeaderItem(2, headerItem)
        headerItem = QTableWidgetItem(QTableWidgetItem("Value\n")) 
        headerItem.setTextAlignment(Qt.AlignLeft)
        self.tableWidget.setHorizontalHeaderItem(3 , headerItem)


    def iterateSequenceTag(self, table, dataset, level=''):

        for data_element in dataset:
            if isinstance(data_element, pydicom.dataset.Dataset):
                self.iterateSequenceTag(table, data_element, level='    ')
            else:
                rowPosition = table.rowCount()
                table.insertRow(rowPosition)
                table.setItem(rowPosition , 0, QTableWidgetItem(level + ' ' + str(data_element.tag)))
                table.setItem(rowPosition , 1, QTableWidgetItem(data_element.name))
                table.setItem(rowPosition , 2, QTableWidgetItem(data_element.VR))
                if data_element.VR == "OW" or data_element.VR == "OB":
                    try:
                        valueMetadata = str(data_element.value.decode('utf-8'))
                    except:
                        try:
                            valueMetadata = str(list(data_element))
                        except:
                            valueMetadata = str(data_element.value)
                    self.createScrollableLabel(rowPosition, valueMetadata)
                else:
                    valueMetadata =  str(data_element.value)
                
                if data_element.VR == "SQ":
                    level+=' > '
                    self.iterateSequenceTag(table, data_element, level)
                else:
                    table.setItem(rowPosition , 3, QTableWidgetItem(valueMetadata))



    def exportToFile(self, parent):
    
        columHeaders = []
        for i in range(self.tableWidget.model().columnCount()):
            columHeaders.append(self.tableWidget.horizontalHeaderItem(i).text())
        df = pd.DataFrame(columns=columHeaders)
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item is None:
                    #item = self.tableWidget.cellWidget(row, col) 
                    pass # THIS NEEDS FIXING
                else:
                    text = item.text()
                df.at[row, columHeaders[col]] = text
        filename, _ = QFileDialog.getSaveFileName(parent, 'Save CSV file as ...', self.series.label()+'.csv', "CSV files (*.csv)") 
        if filename != '':
            df.to_csv(filename, index=False)



    def searchTable(self, expression):

        self.tableWidget.clearSelection()
        if expression:
            items = self.tableWidget.findItems(expression, Qt.MatchContains)
            if items:  # we have found something
                for item in items:
                    item.setSelected(True)
                    #self.tableWidget.item(item).setSelected(True)
                self.tableWidget.scrollToItem(items[0])
                #item = items[0]  # take the first
                #table.table.setCurrentItem(item)





