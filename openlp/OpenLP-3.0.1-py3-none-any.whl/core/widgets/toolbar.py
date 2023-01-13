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
Provide common toolbar handling for OpenLP
"""
import logging

from PyQt5 import QtCore, QtWidgets

from openlp.core.lib.ui import create_widget_action


log = logging.getLogger(__name__)


class OpenLPToolbar(QtWidgets.QToolBar):
    """
    Lots of toolbars around the place, so it makes sense to have a common way to manage them. This is the base toolbar
    class.
    """
    def __init__(self, parent):
        """
        Initialise the toolbar.
        """
        super().__init__(parent)
        # useful to be able to reuse button icons...
        self.setIconSize(QtCore.QSize(20, 20))
        self.actions = {}
        log.debug('Init done for %s' % parent.__class__.__name__)

    def add_toolbar_action(self, name, **kwargs):
        """
        A method to help developers easily add a button to the toolbar. A new QAction is created by calling
        ``create_action()``. The action is added to the toolbar and the toolbar is set as parent. For more details
        please look at openlp.core.lib.ui.create_action()
        """
        action = create_widget_action(self, name, **kwargs)
        self.actions[name] = action
        return action

    def add_toolbar_widget(self, widget):
        """
        Add a widget and store it's handle under the widgets object name.
        """
        action = self.addWidget(widget)
        self.actions[widget.objectName()] = action

    def set_widget_visible(self, widgets, visible=True):
        """
        Set the visibility for a widget or a list of widgets.

        :param widgets: A list of strings or individual string with widget object names.
        :param visible: The new state as bool.
        """
        if isinstance(widgets, list):
            for handle in widgets:
                if handle in self.actions:
                    self.actions[handle].setVisible(visible)
                else:
                    log.warning('No handle "%s" in actions list.', str(handle))
        else:
            if widgets in self.actions:
                self.actions[widgets].setVisible(visible)
            else:
                log.warning('No handle "%s" in actions list.', str(widgets))

    def set_widget_enabled(self, widgets, enabled=True):
        """
        Set the enabled state for a widget or a list of widgets.

        :param widgets: A list of string with widget object names.
        :param enabled: The new state as bool.
        """
        for handle in widgets:
            if handle in self.actions:
                self.actions[handle].setEnabled(enabled)
            else:
                log.warning('No handle "%s" in actions list.', str(handle))

    def remove_widget(self, name):
        """
        Find and remove an action from the toolbar
        :param name: The name of the action to me removed
        :return:
        """
        try:
            act = self.actions[name]
            self.removeAction(act)
        except KeyError:
            log.warning(f'No handle {name} in actions list.')

    def add_spacer(self):
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        separator = QtWidgets.QWidget()
        separator.setSizePolicy(size_policy)
        self.addWidget(separator)
        pass
