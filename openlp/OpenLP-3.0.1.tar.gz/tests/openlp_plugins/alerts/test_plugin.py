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
This module contains tests for the plugin class Alerts plugin.
"""
import pytest
from unittest.mock import MagicMock, patch

from openlp.plugins.alerts.alertsplugin import AlertsPlugin


@pytest.fixture
@patch('openlp.plugins.alerts.alertsplugin.Manager')
def plugin_env(mocked_manager, settings, state, registry):
    """An instance of the AlertsPlugin"""
    mocked_manager.return_value = MagicMock()
    return AlertsPlugin(), settings


def test_plugin_about():
    """Test the Abput text string"""
    # GIVEN an environment
    result = AlertsPlugin.about()

    assert result == (
        '<strong>Alerts Plugin</strong>'
        '<br />The alert plugin controls the displaying of alerts on the display screen.'
    )


def test_plugin_state(plugin_env):
    """Test changing state"""
    # GIVEN an environment
    plugin = plugin_env[0]
    settings = plugin_env[1]
    plugin.alerts_active = settings.value('alerts/status')
    # WHEN: I toggle the settings
    plugin.toggle_alerts_state()
    # THEN: the state has changed
    assert settings.value('alerts/status') != plugin.alerts_active


def test_alerts_trigger(plugin_env):
    """Test triggering the Alerts dialog"""
    # GIVEN an environment
    plugin = plugin_env[0]
    plugin.alert_form = MagicMock()
    # WHEN: I request the form
    plugin.on_alerts_trigger()
    # THEN: the form is loaded
    plugin.alert_form.load_list.assert_called_once()
    plugin.alert_form.exec.assert_called_once()


def test_alerts_initialise(plugin_env):
    """Test the initialise functionality"""
    # GIVEN an environment
    plugin = plugin_env[0]
    plugin.tools_alert_item = MagicMock()
    # WHEN: I request the form
    with patch('openlp.core.common.actions.ActionList') as mocked_actionlist:
        plugin.initialise()
        # THEN: the form is loaded
        mocked_actionlist.instance.add_action.assert_called_once()
        plugin.tools_alert_item.setVisible.assert_called_once_with(True)


def test_alerts_finalise(plugin_env):
    """Test the finalise functionality"""
    # GIVEN an environment
    plugin = plugin_env[0]
    plugin.tools_alert_item = MagicMock()
    # WHEN: I request the form
    with patch('openlp.core.common.actions.ActionList') as mocked_actionlist:
        plugin.finalise()
        # THEN: the form is loaded
        mocked_actionlist.instance.remove_action.assert_called_once()
        plugin.tools_alert_item.setVisible.assert_called_once_with(False)
