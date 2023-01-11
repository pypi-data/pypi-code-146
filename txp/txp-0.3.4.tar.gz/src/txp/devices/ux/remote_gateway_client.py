"""
This module defines the _RemoteGatewayClient class used as a singleton
in the streamlit application process.

It will be used to recevie/send inter process messages from/to the Gateway
process.
"""
import threading
import time
from multiprocessing.connection import Connection
import streamlit as st
from streamlit.script_run_context import add_script_run_ctx as add_report_ctx
from streamlit.server.server import Server
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Definition of the _RemoteGatewayClient.
# ==============================================================================
class _RemoteGatewayClient:
    """This Remote Gateway client encapsulates the necessary multiprocessing utilities
    to communicate with the Gateway main process in streamlit app.

    This object is designed to live in the streamlit application
    process, as a singeton.
    """

    def __init__(self):
        """
        Args:
            gateway_connection: The multiprocessing.Connection object to send/receive IPC objects
                to/from the gateway process.
        """
        self._gateway_connection: Connection = None

        self._connection_update_thread: threading.Thread = None
        """_connection_update_thread: A thread designed to run in background, 
        receiving the newest state from the Gateway."""

        self._finish_update_event: threading.Event = threading.Event()

        self.last_known_state = None
        """last_known_state: This helps to launch the streamlit application, only
        when a state was received from the Gateway."""

    def set_gateway_connection(self, gateway_connection: Connection) -> None:
        """Sets the Gateway connection in the UI process."""
        log.debug(
            f"_RemoteGatewayClient receiving Gateway Connection: "
            f"{id(gateway_connection)}"
        )
        self._gateway_connection = gateway_connection

    def _connection_update_loop(self, pill: threading.Event):
        """A loop to receive states from the Gateway, and refresh the streamlit
        application programmatically.

        Note: Using a workaround to refresh the view. Streamlit doesn't support yet
        a public stable method to re-run the script on command. There's an experimental
        feature: experimental_rerun. But it didn't seem to work outside the main thread.

        Todo: If streamlit moves the experimental_rerun to the stable API, revisit this
            implementation.
        """
        while True:
            while not self._gateway_connection.poll():
                time.sleep(0.5)  # waits 0.1 seconds to ask again if there's a new state
                if pill.is_set():
                    log.debug("Closing update thread")
                    return

            try:
                new_state_from_gateway = (
                    self._gateway_connection.recv()
                )  # blocks until there's something new to receive

            except:
                # The recommended way is for only one client thread to publish states to the streamlit process.
                # Just in case, to avoid runtime problems, catching an exception.
                # TODO: We should implement a recovery strategy of the pipes in the future
                log.error('Error receiving UI in streamlit process. The UI will not be updated')
                continue

            self.last_known_state = new_state_from_gateway
            st.session_state.gateway_state = new_state_from_gateway
            log.debug(f"New Gateway state received: {new_state_from_gateway}")

            # st.experimental_rerun doesn't seems to work properly with threads.
            #try:
            #    st.experimental_rerun()
            #except st.script_runner.RerunException as e:
            #    log.warning("Exception trying to rerun streamlit app.")

            # This refresh snippet is taken from:
            # https://github.com/streamlit/streamlit/issues/3854

            # Streamlit <= 1.3.0 should use this commented code to get the session ID.
            # ctx = st.report_thread.get_report_ctx()
            # session_id = add_report_ctx().streamlit_script_run_ctx.session_id
            current_server = Server.get_current()
            session_id = add_report_ctx().streamlit_script_run_ctx.session_id
            session = current_server.get_session_by_id(session_id)
            log.debug(f"Streamlit session ID: {session_id}")
            if session is None:
                # If the session is None, then a new tab was opened and that's the new
                # session to be updated in real time.
                log.debug("The streamlit session was not found.")
            else:
                session.request_rerun(None)

    def start_refresh_loop(self) -> None:
        """Starts a receive background thread responsible of receiving new states from
        the Gateway process.
        """
        # First, it'll end the running thread for the previous running session.
        # That session is assumed to be closed. It will not receive new real time updates.
        if self._connection_update_thread is not None:
            self._finish_update_event.set()
            while self._connection_update_thread.is_alive():
                pass
            self._connection_update_thread = None
            self._finish_update_event = threading.Event()

        self._connection_update_thread = threading.Thread(
            target=self._connection_update_loop,
            name="_gateway_connection_update_thread",
            daemon=True,
            args=(self._finish_update_event,)
        )
        add_report_ctx(
            self._connection_update_thread
        )  # Add the streamlit context report to the thread
        self._connection_update_thread.start()

    def wait_for_initial_state(self) -> None:
        """Waits to receive the initial state from the Gateway.

        It should be called before starting the streamlit app to
        have a first state to render.
        """
        new_state_from_gateway = (
            self._gateway_connection.recv()
        )  # blocks until there's something new to receive
        self.last_known_state = new_state_from_gateway

    def send_state_to_gateway(self, ux_state) -> None:
        """Sends the ux_state message to the Gateway."""
        log.debug(f"Send UxState to Gateway: {ux_state}")
        self._gateway_connection.send(ux_state)


# ==============================================================================
# Declaration of the _RemoteGatewayClient singleton instance.
# ==============================================================================

remote_gateway_client: _RemoteGatewayClient = _RemoteGatewayClient()
