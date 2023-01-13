#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################
from __future__ import absolute_import

__all__ = ["TaurusTrend"]

import copy
from time import localtime, strftime

import numpy as np
from pyqtgraph import PlotWidget
from taurus.core.util.containers import LoopList
from taurus.core.util.log import Logger
from taurus.external.qt import QtGui, PYSIDE2
from taurus.qt.qtcore.configuration import BaseConfigurableClass

from .autopantool import XAutoPanTool
from .buffersizetool import BufferSizeTool
from .curveproperties import CURVE_COLORS
from .curvespropertiestool import CurvesPropertiesTool
from .datainspectortool import DataInspectorTool
from .dateaxisitem import DateAxisItem
from .forcedreadtool import ForcedReadTool
from .legendtool import PlotLegendTool
from .taurusmodelchoosertool import TaurusXYModelChooserTool
from .taurustrendset import TaurusTrendSet
from .y2axis import Y2ViewBox

try:
    from pyhdbpp import get_default_reader

    archiving_reader = get_default_reader()
except Exception:
    archiving_reader = None

SECONDS_48_HOURS = 172800


class TaurusTrend(PlotWidget, BaseConfigurableClass):
    """
    TaurusTrend is a general widget for plotting the evolution of a value
    over time. It is an extended taurus-aware version of
    :class:`pyqtgraph.PlotWidget`.

    Apart from all the features already available in a regulat PlotWidget,
    TaurusTrend incorporates the following tools/features:

        - Secondary Y axis (right axis)
        - Time X axis
        - A plot configuration dialog, and save/restore configuration
          facilities
        - A menu option for adding/removing taurus  models
        - A menu option for showing/hiding the legend
        - Automatic color change of curves for newly added models

    """

    def __init__(self, parent=None, **kwargs):

        buffer_size = kwargs.pop("buffer_size", 65536)

        if PYSIDE2:
            # Workaround for https://bugreports.qt.io/browse/PYSIDE-1564
            BaseConfigurableClass.__init__(self)
            PlotWidget.__init__(self, parent=parent, **kwargs)
        else:
            super(TaurusTrend, self).__init__(parent=parent, **kwargs)

        # Compose with a Logger
        self._logger = Logger(name=self.__class__.__name__)
        self.debug = self._logger.debug
        self.info = self._logger.info
        self.warning = self._logger.warning
        self.error = self._logger.error

        # set up cyclic color generator
        self._curveColors = LoopList(CURVE_COLORS)
        self._curveColors.setCurrentIndex(-1)

        plot_item = self.getPlotItem()
        menu = plot_item.getViewBox().menu

        # add trends clear action
        clearTrendsAction = QtGui.QAction("Clear trends", menu)
        clearTrendsAction.triggered.connect(self.clearTrends)
        menu.addAction(clearTrendsAction)

        # add save & retrieve configuration actions
        saveConfigAction = QtGui.QAction("Save configuration", menu)
        saveConfigAction.triggered.connect(self._onSaveConfigAction)
        menu.addAction(saveConfigAction)

        loadConfigAction = QtGui.QAction("Retrieve saved configuration", menu)
        loadConfigAction.triggered.connect(self._onLoadConfigAction)
        menu.addAction(loadConfigAction)

        # set up archiving functionality
        self._archiving_enabled = False
        self._archiving_reader = None
        self._auto_reload_checkbox = None
        self._dismiss_archive_message = False
        if self._setArchivingReader():
            self._loadArchivingContextActions()

        self.registerConfigProperty(self._getState, self.restoreState, "state")

        # add legend tool
        legend_tool = PlotLegendTool(self)
        legend_tool.attachToPlotItem(plot_item)

        # add model chooser
        self._model_chooser_tool = TaurusXYModelChooserTool(
            self, itemClass=TaurusTrendSet, showX=False
        )
        self._model_chooser_tool.attachToPlotItem(
            self.getPlotItem(), self, self._curveColors
        )

        # add Y2 axis
        self._y2 = Y2ViewBox()
        self._y2.attachToPlotItem(plot_item)

        # Add time X axis
        axis = DateAxisItem(orientation="bottom")
        axis.attachToPlotItem(plot_item)

        # add plot configuration dialog
        self._cprop_tool = CurvesPropertiesTool(self)
        self._cprop_tool.attachToPlotItem(plot_item, y2=self._y2)

        # add data inspector widget
        inspector_tool = DataInspectorTool(self)
        inspector_tool.attachToPlotItem(self.getPlotItem())

        # add force read tool
        self._fr_tool = ForcedReadTool(self)
        self._fr_tool.attachToPlotItem(self.getPlotItem())

        # add buffer size tool
        self.buffer_tool = BufferSizeTool(self, buffer_size=buffer_size)
        self.buffer_tool.attachToPlotItem(self.getPlotItem())

        # Add the auto-pan ("oscilloscope mode") tool
        self._autopan = XAutoPanTool()
        self._autopan.attachToPlotItem(self.getPlotItem())

        # Register config properties
        self.registerConfigDelegate(self._model_chooser_tool, "XYmodelchooser")
        # self.registerConfigDelegate(self._y2, "Y2Axis")
        self.registerConfigDelegate(self._cprop_tool, "CurvePropertiesTool")
        self.registerConfigDelegate(legend_tool, "legend")
        self.registerConfigDelegate(self._fr_tool, "forceread")
        self.registerConfigDelegate(self.buffer_tool, "buffer")
        self.registerConfigDelegate(inspector_tool, "inspector")

    def __getitem__(self, idx):
        """
        Provides a list-like interface: items can be accessed using slice
        notation
        """
        return self._getCurves()[idx]

    def __len__(self):
        return len(self._getCurves())

    def __bool__(self):
        return True

    def _loadArchivingContextActions(self):
        """Loads archiving options to context menu on the trend (right-click)
        and enables triggers regarding archiving.
        """
        menu = self.plotItem.getViewBox().menu

        archiving_menu = QtGui.QMenu("Archiving", menu)
        menu.addMenu(archiving_menu)

        self._auto_reload_checkbox = QtGui.QAction(
            "Autoreload", archiving_menu
        )
        self._auto_reload_checkbox.setCheckable(True)
        self._auto_reload_checkbox.setChecked(False)
        self._auto_reload_checkbox.triggered.connect(
            self._onEnableDisableArchivingClicked
        )

        load_once_action = QtGui.QAction("Load Once", archiving_menu)
        load_once_action.triggered.connect(self._loadArchivingDataOnce)

        shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+r"), self)
        shortcut.activated.connect(self._loadArchivingDataOnce)

        archiving_menu.addAction(self._auto_reload_checkbox)
        archiving_menu.addAction(load_once_action)

    def _loadArchivingDataOnce(self):
        self._loadArchivingData(loadOnce=True)

    def _onEnableDisableArchivingClicked(self):
        """Change the state of boolean archiving_enabled to the opposite
        of their actual value. If it's set to True a connection between
        sigRangeChanged and local function on_changed_trend is set,
        otherwise, the connection gets disconnected.
        """
        self._archiving_enabled = not self._archiving_enabled

        if self._archiving_enabled:
            self.sigRangeChanged\
                .connect(lambda: self._loadArchivingData(loadOnce=False))
            self.info("Archiving option set to enabled")
            self._loadArchivingData(loadOnce=False)  # Force first data query
        else:
            self.sigRangeChanged.disconnect()
            self.info("Archiving option set to disabled")

    def _setArchivingReader(self):
        """Try to set up a reader and return if it was possible or not
        (True/False). :return: True if reader is set or False if not
        """
        if archiving_reader:
            self._archiving_reader = archiving_reader
            self.info("Archiving reader set")
            return True
        else:
            self.info("Archiving reader not set")
            return False

    def _loadArchivingData(self, loadOnce=False):
        """When there is a change on the Range of view perform
        a query to get archiving data and append it to the left.
        """

        for taurus_trend_set in self.plotItem.dataItems:
            if not isinstance(taurus_trend_set, TaurusTrendSet):
                continue
            try:
                left_time_range_value = self.visibleRange().left()
                right_time_range_value = self.visibleRange().right()
                plot_time_range = \
                    right_time_range_value - left_time_range_value
                elder_buffer_value = (taurus_trend_set._xBuffer[0]
                                      if len(
                    taurus_trend_set._xBuffer) else right_time_range_value)
                query_window = elder_buffer_value - left_time_range_value

                if query_window > (.15 * plot_time_range) > 1:

                    from_date = strftime('%Y-%m-%dT%H:%M:%S',
                                         localtime(left_time_range_value))
                    to_date = strftime('%Y-%m-%dT%H:%M:%S',
                                       localtime(elder_buffer_value))
                    if self._checkForQuerySizeAndUserConfirmation(
                        left_time_range_value, elder_buffer_value,
                            taurus_trend_set.modelName):
                        try:
                            values = self._archiving_reader \
                                .get_attribute_values(
                                    taurus_trend_set.modelName
                                    , from_date, to_date)
                            self.debug(
                                'loadArchivingData(%s, %s, %s): %d values' % (
                                    taurus_trend_set.modelName, from_date,
                                    to_date, len(values)))

                        except KeyError as ke:
                            values = None
                            self.debug(
                                "Attribute '{}' has no archiving data".format(
                                    ke))

                        if values is not None and len(values):
                            if (len(values) + len(taurus_trend_set._xBuffer)) \
                                    < self.buffer_tool.bufferSize():
                                self.debug(
                                    "left-appending historical data from {} "
                                    "to {}".format(from_date, to_date))
                                x, y, _, _ = zip(*values)
                                x = np.array(x)
                                y = np.array([[val] for val in y])
                                try:
                                    taurus_trend_set._xBuffer.extendLeft(x)
                                    taurus_trend_set._yBuffer.extendLeft(y)
                                except ValueError as e:
                                    self.error("Error left-appending data to "
                                               "buffer.\n", e)
                            else:
                                msg = ("Buffer size is surpassing limit and "
                                       "data has been discarded.\n "
                                       "You can change the buffer size at "
                                       "your "
                                       "own responsibility and try again.")
                                if loadOnce:
                                    self._askForConfirmation(msg, buttons=QtGui
                                                             .QMessageBox.Ok)
                                else:
                                    msg += "\nAuto reload has been disabled"
                                    self._disableAutoReloadAndDiscardData(msg)
                                    return
                    else:
                        if not loadOnce:
                            msg = "Data from archiving has been discarded " \
                                  "and reload disabled"
                            self._disableAutoReloadAndDiscardData(msg)
                        break
            except Exception as e:
                self.warning("Error updating trend set of model {} "
                             "with error {}".format(taurus_trend_set.modelName
                                                    , e))

    def _disableAutoReloadAndDiscardData(self, message):
        self._askForConfirmation(message, buttons=QtGui.QMessageBox.Ok)
        self.info(message)
        self._auto_reload_checkbox.setChecked(False)
        self._onEnableDisableArchivingClicked()  # Force a trigger

    def _getCurves(self):
        """returns a flat list with all items from all trend sets"""
        ret = []
        for ts in self.getTrendSets():
            ret += ts[:]
        return ret

    def getTrendSets(self):
        """Returns all the trend sets attached to this plot item"""
        return [
            e
            for e in self.getPlotItem().listDataItems()
            if isinstance(e, TaurusTrendSet)
        ]

    def clearTrends(self):
        """Clear the buffers of all the trend sets in the plot"""
        for ts in self.getTrendSets():
            ts.clearBuffer()

    def setModel(self, names):
        """Set a list of models"""
        # support passing a string  in names instead of a sequence
        if isinstance(names, str):
            names = [names]
        self._model_chooser_tool.updateModels(names or [])

    def addModels(self, names):
        """Reimplemented to delegate to the  model chooser"""
        # support passing a string in names
        if isinstance(names, str):
            names = [names]
        self._model_chooser_tool.addModels(names)

    def _getState(self):
        """Same as PlotWidget.saveState but removing viewRange conf to force
        a refresh with targetRange when loading
        """
        state = copy.deepcopy(self.saveState())
        # remove viewRange conf
        del state["view"]["viewRange"]
        return state

    def setXAxisMode(self, x_axis_mode):
        """Required generic TaurusTrend API """
        if x_axis_mode != "t":
            raise NotImplementedError(  # TODO
                'X mode "{}" not yet supported'.format(x_axis_mode)
            )

    def setForcedReadingPeriod(self, period):
        """Required generic TaurusTrend API """
        self._fr_tool.setPeriod(period)

    def setMaxDataBufferSize(self, buffer_size):
        """Required generic TaurusTrend API """
        self.buffer_tool.setBufferSize(buffer_size)

    def _onSaveConfigAction(self):
        """wrapper to avoid issues with overloaded signals"""
        return self.saveConfigFile()

    def _onLoadConfigAction(self):
        """wrapper to avoid issues with overloaded signals"""
        return self.loadConfigFile()

    def _checkForQuerySizeAndUserConfirmation(self, from_date, to_date,
                                              model_name):
        if to_date - from_date > SECONDS_48_HOURS:
            if not self._dismiss_archive_message:
                buttonClicked = self._askForConfirmation(
                    "You are querying more than 48 hours for "
                    "{}, this may take a while.\nContinue? (Yes to All "
                    "disables "
                    "this message) ".format(model_name))
                self._dismiss_archive_message = \
                    buttonClicked == QtGui.QMessageBox.YesToAll
                return buttonClicked in [QtGui.QMessageBox.Ok,
                                         QtGui.QMessageBox.YesToAll]

        return True

    def _askForConfirmation(self, message,
                            buttons=QtGui.QMessageBox.Ok | QtGui.QMessageBox
                            .YesToAll | QtGui.QMessageBox.Cancel):
        warn_user = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warning!",
                                      message, buttons)
        return warn_user.exec_()


def trend_main(
    models=(), config_file=None, demo=False, window_name="TaurusTrend (pg)"
):
    """Launch a TaurusTrend"""
    import sys
    from taurus.qt.qtgui.application import TaurusApplication

    app = TaurusApplication(cmd_line_parser=None, app_name="taurustrend(pg)")

    w = TaurusTrend()

    w.setWindowTitle(window_name)

    if demo:
        models = list(models)
        models.extend(["eval:rand()", "eval:1+rand(2)"])

    if config_file is not None:
        w.loadConfigFile(config_file)

    if models:
        w.setModel(models)

    w.show()
    ret = app.exec_()

    sys.exit(ret)


if __name__ == "__main__":
    trend_main(models=("eval:rand()", "sys/tg_test/1/ampli"))
