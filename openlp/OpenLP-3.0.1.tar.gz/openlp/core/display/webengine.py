# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2023 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
Subclass of QWebEngineView. Adds some special eventhandling needed for screenshots/previews
Heavily inspired by https://stackoverflow.com/questions/33467776/qt-qwebengine-render-after-scrolling/33576100#33576100
"""
import logging

from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets

from openlp.core.common.applocation import AppLocation


LOG_LEVELS = {
    QtWebEngineWidgets.QWebEnginePage.InfoMessageLevel: logging.INFO,
    QtWebEngineWidgets.QWebEnginePage.WarningMessageLevel: logging.WARNING,
    QtWebEngineWidgets.QWebEnginePage.ErrorMessageLevel: logging.ERROR
}


log = logging.getLogger(__name__)


class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    """
    A custom WebEngine page to capture Javascript console logging
    """
    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        """
        Override the parent method in order to log the messages in OpenLP
        """
        # The JS log has the entire file location, which we don't really care about
        app_dir = AppLocation.get_directory(AppLocation.AppDir).parent
        if str(app_dir) in source_id:
            source_id = source_id.replace('file://{app_dir}/'.format(app_dir=app_dir), '')
        # Log the JS messages to the Python logger
        log.log(LOG_LEVELS[level], '{source_id}:{line_number} {message}'.format(source_id=source_id,
                                                                                line_number=line_number,
                                                                                message=message))


class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    """
    A sub-classed QWebEngineView to handle paint events of OpenGL (does not seem to work)
    and set some attributtes.
    """
    _child = None  # QtWidgets.QOpenGLWidget or QWidget?
    delegatePaint = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(WebEngineView, self).__init__(parent)
        self.setPage(WebEnginePage(self))
        self.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalStorageEnabled, True)
        self.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.page().settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalStorageEnabled, True)
        self.page().settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.page().settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

    def eventFilter(self, obj, ev):
        """
        Emit delegatePaint on paint event of the last added QOpenGLWidget child
        """
        if obj == self._child:
            if ev.type() == QtCore.QEvent.MouseButtonPress or ev.type() == QtCore.QEvent.TouchBegin:
                self.display_clicked()
            if ev.type() == QtCore.QEvent.Paint:
                self.delegatePaint.emit()
        return super(WebEngineView, self).eventFilter(obj, ev)

    def display_clicked(self):
        """
        Dummy method to be overridden
        """
        pass

    def event(self, ev):
        """
        Handle events
        """
        if ev.type() == QtCore.QEvent.ChildAdded:
            # Only use QWidget child (used to be QOpenGLWidget)
            w = ev.child()
            if w and isinstance(w, QtWidgets.QWidget):
                self._child = w
                w.installEventFilter(self)
        return super(WebEngineView, self).event(ev)
