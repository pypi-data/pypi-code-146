#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 19:42:57 2022

@author: aguimera
"""

import argparse
import sys
import os
import warnings

import numpy as np

from matplotlib import pyplot as plt
import matplotlib as mpl

from qtpy.QtWidgets import QFileDialog
from qtpy import QtWidgets, uic
from qtpy.QtCore import QSortFilterProxyModel
from qtpy.QtCore import QAbstractTableModel, QModelIndex
from qtpy.QtCore import Qt
import pandas as pd
import seaborn as sns
import math
from scipy import stats


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)
        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            data = self._dataframe.iloc[index.row(), index.column()]
            if type(data) == str:
                return data
            st = str(data)
            return st
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])
        return None

LogPars = ('Zabs', 'Zre', 'Zim', 'Rp', 'Rs')

def FormatAxis(PlotPars, dfAttrs):
    # figure generation
    nRows = math.ceil(np.sqrt(len(PlotPars)))
    nCols = math.ceil(len(PlotPars) / nRows)
    fig, Axs = plt.subplots(nrows=nRows, ncols=nCols)
    if nRows == 1 and nCols == 1:
        Axs = [Axs, ]
    else:
        Axs = Axs.flatten()

    # Format axis
    AxsDict = {}
    for ip, par in enumerate(PlotPars):
        ax = Axs[ip]
        AxsDict[par] = ax
        ax.set_xscale('log')
        ax.set_xlabel('Frequency [Hz]')
        slabel = '{}'.format(par)
        ax.set_ylabel(slabel)
        if par in LogPars:
            ax.set_yscale('log')

    return fig, AxsDict


class DataExplorer(QtWidgets.QMainWindow):
    BoxPlotFunctions = {'Boxplot': sns.boxplot,
                        'violinplot': sns.violinplot,
                        'swarmplot': sns.swarmplot,
                        'boxenplot': sns.boxenplot,
                        'barplot': sns.barplot,
                        'stripplot': sns.stripplot,
                        }

    def __init__(self, dfDat):
        QtWidgets.QMainWindow.__init__(self)

        uipath = os.path.join(os.path.dirname(__file__), 'GuiDataExplorer_v2.ui')
        uic.loadUi(uipath, self)

        self.setWindowTitle('Zelect DataExplorer')

        self.dfDat = dfDat

        self.modelData = PandasModel(self.dfDat.copy())
        self.proxyData = QSortFilterProxyModel()
        self.proxyData.setSourceModel(self.modelData)
        self.TblData.setModel(self.proxyData)
        self.TblData.show()

        self.LstBoxYPars.addItems(self.dfDat.attrs['ScalarCols'])

        includetypes = ('float', 'category', 'bool', 'datetime64[ns]')
        catCols = list(dfDat.select_dtypes(include=includetypes).columns)
        self.CmbBoxX.addItems(catCols)
        self.CmbBoxX.setCurrentText('Device')
        self.CmbBoxHue.addItems(catCols)
        self.CmbBoxHue.setCurrentText('Device')
        self.CmbBoxType.addItems(self.BoxPlotFunctions.keys())

        self.LstLinesPars.addItems(self.dfDat.attrs['ArrayCols'])
        self.CmbLinesGroup.addItems(catCols)
        self.CmbLinesGroup.setCurrentText('Device')

        self.ButBoxPlot.clicked.connect(self.ButBoxPlot_Click)
        self.ButPlotVect.clicked.connect(self.ButPlotVect_Click)
        self.ButExportPkl.clicked.connect(self.ButExportPkl_Click)
        self.ButExportCSV.clicked.connect(self.ButExportCSV_Click)

        self.TxtSelQueries.textChanged.connect(self.TxtSelQueries_Changed)

    def TxtSelQueries_Changed(self):        
        self.TxtTitleName.setText(self.TxtSelQueries.toPlainText().replace('\n','-'))

    def GetSelection(self):
        Sel = self.TblData.selectedIndexes()
        rows = set([self.proxyData.mapToSource(s).row() for s in Sel])
        dSel = self.dfDat.loc[list(rows)]

        if not self.ChckQueries.isChecked():
            return dSel

        for q in self.TxtSelQueries.toPlainText().split('\n'):
            try:
                dSel.query(q, inplace=True)
            except:
                print(q)
                print("Error in query execution")

        return dSel

    def ButBoxPlot_Click(self):
        Sel = self.LstBoxYPars.selectedItems()
        if len(Sel) == 0:
            print('Select Y var')
            return
        PlotPars = [s.text() for s in Sel]

        dSel = self.GetSelection()

        nRows = math.ceil(np.sqrt(len(PlotPars)))
        nCols = math.ceil(len(PlotPars) / nRows)
        fig, Axs = plt.subplots(nrows=nRows, ncols=nCols)
        if nRows == 1 and nCols == 1:
            Axs = [Axs, ]
        else:
            Axs = Axs.flatten()

        fig.suptitle(self.TxtTitleName.toPlainText())

        PltFunct = self.BoxPlotFunctions[self.CmbBoxType.currentText()]

        for ic, p in enumerate(PlotPars):
            PltFunct(x=self.CmbBoxX.currentText(),
                     y=p,
                     hue=self.CmbBoxHue.currentText(),
                     data=dSel,
                     ax=Axs[ic])
            if p in LogPars:
                Axs[ic].set_yscale('log')

            plt.setp(Axs[ic].get_legend().get_texts(),
                     fontsize='xx-small')
            plt.setp(Axs[ic].get_legend().get_title(),
                     fontsize='xx-small')
            plt.setp(Axs[ic].get_xticklabels(),
                     rotation=45,
                     ha="right",
                     fontsize='xx-small',
                     rotation_mode="anchor")

        plt.show()

    def ButPlotVect_Click(self):
        Sel = self.LstLinesPars.selectedItems()
        if len(Sel) == 0:
            print('Select Y var')
            return
        PlotPars = [s.text() for s in Sel]

        dSel = self.GetSelection()
        GroupBy = self.CmbLinesGroup.currentText()
        dgroups = dSel.groupby(GroupBy, observed=True)

        # Colors iteration
        Norm = mpl.colors.Normalize(vmin=0, vmax=len(dgroups))
        cmap = mpl.cm.ScalarMappable(norm=Norm, cmap='jet')

        fig, AxsDict = FormatAxis(PlotPars, self.dfDat.attrs)
        fig.suptitle(self.TxtTitleName.toPlainText())

        for ic, gn in enumerate(dgroups.groups):
            gg = dgroups.get_group(gn)
            Col = cmap.to_rgba(ic)
            for parn in PlotPars:
                xVar = self.dfDat.attrs['FreqVals']

                Vals = np.array([])
                ax = AxsDict[parn]
                for index, row in gg.iterrows():
                    v = row[parn]
                    if type(v) == float:
                        continue
                    try:
                        if self.CheckLines.isChecked():
                            ax.plot(xVar, v.transpose(),
                                    color=Col,
                                    alpha=0.8,
                                    label=gn)
                        Vals = np.vstack((Vals, v)) if Vals.size else v
                    except:
                        pass

                if Vals.size == 0:
                    continue

                Vals = Vals.transpose()
                if self.CheckLinesMean.isChecked():
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        mean = np.nanmedian(Vals, axis=1)
                    ax.plot(xVar, mean, '-.', color=Col, lw=1.5, label=gn)

                if self.CheckLinesStd.isChecked():
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        std = stats.tstd(Vals, axis=1)  # changed to mad for robustness
                    ax.fill_between(xVar, mean + std, mean - std, color=Col, alpha=0.2)

                handles, labels = ax.get_legend_handles_labels()
                by_label = dict(zip(labels, handles))
                ax.legend(by_label.values(), by_label.keys(), fontsize='xx-small')

        plt.show()

    def ButExportPkl_Click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save PKl file", "", "All Files (*);; (*.pkl)", options=options)
        if fileName:
            dSel = self.GetSelection()
            dSel.to_pickle(fileName)

    def ButExportCSV_Click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save CSV file", "", "All Files (*);; (*.csv)", options=options)
        if fileName:
            dSel = self.GetSelection()
            dSel.to_csv(fileName)


def LaunchDataExp(Data):
    app = QtWidgets.QApplication(sys.argv)
    w = DataExplorer(Data)
    w.show()
    app.exec_()
    
