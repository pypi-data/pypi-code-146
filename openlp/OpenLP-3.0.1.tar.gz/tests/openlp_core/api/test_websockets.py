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
Functional tests to test the Http Server Class.
"""
import pytest
from unittest.mock import MagicMock, patch

from openlp.core.api.websocketspoll import WebSocketPoller
from openlp.core.api.websockets import WebSocketWorker, WebSocketServer
from openlp.core.common.registry import Registry


@pytest.fixture
def poller(settings):
    poll = WebSocketPoller()
    yield poll


@pytest.fixture
def worker(settings):
    worker = WebSocketWorker()
    yield worker


@patch('openlp.core.api.websockets.WebSocketWorker')
@patch('openlp.core.api.websockets.run_thread')
def test_serverstart(mocked_run_thread, MockWebSocketWorker, registry):
    """
    Test the starting of the WebSockets Server with the disabled flag set off
    """
    # GIVEN: A new WebSocketServer
    Registry().set_flag('no_web_server', False)
    server = WebSocketServer()

    # WHEN: I start the server
    server.start()

    # THEN: the api environment should have been created
    assert mocked_run_thread.call_count == 1, 'The qthread should have been called once'
    assert MockWebSocketWorker.call_count == 1, 'The http thread should have been called once'


@patch('openlp.core.api.websockets.WebSocketWorker')
@patch('openlp.core.api.websockets.run_thread')
def test_serverstart_not_required(mocked_run_thread, MockWebSocketWorker, registry):
    """
    Test the starting of the WebSockets Server with the disabled flag set on
    """
    # GIVEN: A new WebSocketServer and the server is not required
    Registry().set_flag('no_web_server', True)
    server = WebSocketServer()

    # WHEN: I start the server
    server.start()

    # THEN: the api environment should have not been created
    assert mocked_run_thread.call_count == 0, 'The qthread should not have been called'
    assert MockWebSocketWorker.call_count == 0, 'The http thread should not have been called'


def test_poller_get_state(poller, settings):
    """
    Test the get_state function returns the correct JSON
    """
    # GIVEN: the system is configured with a set of data
    mocked_service_manager = MagicMock()
    mocked_service_manager.service_id = 21
    mocked_live_controller = MagicMock()
    mocked_live_controller.selected_row = 5
    mocked_live_controller.service_item = MagicMock()
    mocked_live_controller.service_item.unique_identifier = '23-34-45'
    mocked_live_controller.blank_screen.isChecked.return_value = True
    mocked_live_controller.theme_screen.isChecked.return_value = False
    mocked_live_controller.desktop_screen.isChecked.return_value = False
    Registry().register('live_controller', mocked_live_controller)
    Registry().register('service_manager', mocked_service_manager)
    # WHEN: The poller polls
    poll_json = poller.get_state()
    # THEN: the live json should be generated and match expected results
    assert poll_json['results']['blank'] is True, 'The blank return value should be True'
    assert poll_json['results']['theme'] is False, 'The theme return value should be False'
    assert poll_json['results']['display'] is False, 'The display return value should be False'
    assert poll_json['results']['isSecure'] is False, 'The isSecure return value should be False'
    assert poll_json['results']['twelve'] is True, 'The twelve return value should be True'
    assert poll_json['results']['version'] == 3, 'The version return value should be 3'
    assert poll_json['results']['slide'] == 5, 'The slide return value should be 5'
    assert poll_json['results']['service'] == 21, 'The version return value should be 21'
    assert poll_json['results']['item'] == '23-34-45', 'The item return value should match 23-34-45'


@patch('openlp.core.api.websockets.serve')
@patch('openlp.core.api.websockets.asyncio')
@patch('openlp.core.api.websockets.log')
def test_worker_start(mocked_log, mocked_asyncio, mocked_serve, worker, settings):
    """
    Test the start function of the worker
    """
    # GIVEN: A mocked serve function and event loop
    mocked_serve.return_value = 'server_thing'
    event_loop = MagicMock()
    mocked_asyncio.new_event_loop.return_value = event_loop
    # WHEN: The start function is called
    worker.start()
    # THEN: No error occurs
    mocked_serve.assert_called_once()
    event_loop.run_until_complete.assert_called_once_with('server_thing')
    event_loop.run_forever.assert_called_once_with()
    mocked_log.exception.assert_not_called()
    # Because run_forever is mocked, it doesn't stall the thread so close will be called immediately
    event_loop.close.assert_called_once_with()


@patch('openlp.core.api.websockets.serve')
@patch('openlp.core.api.websockets.asyncio')
@patch('openlp.core.api.websockets.log')
def test_worker_start_fail(mocked_log, mocked_asyncio, mocked_serve, worker, settings):
    """
    Test the start function of the worker handles a error nicely
    """
    # GIVEN: A mocked serve function and event loop. run_until_complete returns a error
    mocked_serve.return_value = 'server_thing'
    event_loop = MagicMock()
    mocked_asyncio.new_event_loop.return_value = event_loop
    event_loop.run_until_complete.side_effect = Exception()
    # WHEN: The start function is called
    worker.start()
    # THEN: An exception is logged but is handled and the event_loop is closed
    mocked_serve.assert_called_once()
    event_loop.run_until_complete.assert_called_once_with('server_thing')
    event_loop.run_forever.assert_not_called()
    mocked_log.exception.assert_called_once()
    event_loop.close.assert_called_once_with()


def test_poller_event_attach(poller, settings):
    """
    Test the event attach of WebSocketPoller
    """
    # GIVEN: A mocked live_controlled, a mocked slide_controller and mocked change signals
    servicemanager_changed_connect = MagicMock()
    service_manager = MagicMock()
    service_manager.servicemanager_changed = MagicMock()
    service_manager.servicemanager_changed.connect = servicemanager_changed_connect
    poller._service_manager = service_manager
    live_controller = MagicMock()
    slidecontroller_changed_connect = MagicMock()
    live_controller.slidecontroller_changed = MagicMock()
    live_controller.slidecontroller_changed.connect = slidecontroller_changed_connect
    poller._live_controller = live_controller

    # WHEN: the hook_signals function is called
    poller.hook_signals()

    # THEN: service_manager and live_controller changed signals should be connected
    servicemanager_changed_connect.assert_called_once()
    slidecontroller_changed_connect.assert_called_once()


def test_poller_on_change_emit(poller, settings):
    """
    Test the change event emission of WebSocketPoller
    """
    # GIVEN: A mocked changed signal and create_state function
    poller_changed_emit = MagicMock()
    poller.create_state = MagicMock(return_value={})
    poller.poller_changed = MagicMock()
    poller.poller_changed.emit = poller_changed_emit

    # WHEN: The on_signal_received function is called
    poller.on_signal_received()

    # THEN: poller_changed signal should be emitted once
    poller_changed_emit.assert_called_once()


def test_poller_get_state_is_never_none(poller):
    """
    Test the get_state call never returns None
    """
    # GIVEN: A mocked poller create_state
    poller.create_state = MagicMock(return_value={"key1": "2"})

    # WHEN: poller.get_state is called
    state = poller.get_state()

    # THEN: state is not None
    assert state is not None, 'get_state() return should not be None'


@patch('openlp.core.api.websockets.poller')
@patch('openlp.core.api.websockets.run_thread')
def test_websocket_server_connects_to_poller(mock_run_thread, mock_poller, settings):
    """
    Test if the websocket_server connects to WebSocketPoller
    """
    # GIVEN: A mocked poller signal and a server
    Registry().set_flag('no_web_server', False)
    mock_poller.poller_changed = MagicMock()
    mock_poller.poller_changed.connect = MagicMock()
    server = WebSocketServer()
    server.handle_poller_signal = MagicMock()

    # WHEN: WebSocketServer is started
    server.start()

    # THEN: poller_changed should be connected with WebSocketServer and correct handler
    mock_poller.poller_changed.connect.assert_called_once_with(server.handle_poller_signal)


@patch('openlp.core.api.websockets.poller')
@patch('openlp.core.api.websockets.WebSocketWorker.add_state_to_queues')
@patch('openlp.core.api.websockets.run_thread')
def test_websocket_worker_register_connections(mock_run_thread, mock_add_state_to_queues, mock_poller, settings):
    """
    Test if the websocket_server can receive poller signals
    """
    # GIVEN: A mocked poller create_state, a mocked server and a mocked worker
    mock_state = {"key1": "2"}
    mock_poller.get_state.return_value = mock_state
    Registry().set_flag('no_web_server', False)
    server = WebSocketServer()
    server.start()

    # WHEN: server.handle_poller_signal is called
    server.handle_poller_signal()

    # THEN: WebSocketWorker state notify function should be called
    mock_add_state_to_queues.assert_called_once_with(mock_state)
