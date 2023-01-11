"""
This module defines classes to be used in the IPC between the Gateway
process and the UI process.

- UxClient: A UxClient class to be used by the Gateway instance in order to start
the streamlit application process and to send messages to it.

- _RemoteGatewayClient: a class to be used as singleton in the streamlit application
process. It will receive/send inter process messages from/to the gateway.
"""
# ============================ imports =========================================
from multiprocessing import Pipe
from multiprocessing.connection import Connection
from txp.devices.ux.streamlit_runner import StreamlitRunner
import time
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Definition of the UxClient class.
# ==============================================================================
class UxClient:
    """The UxClient class provides a client for the gateway to start
    the streamlit app and perform IPC.

    The IPC is performed using Pipes. This allow for a two-way
    communication capability with a high level of abstraction:
        - Gateway can send and receive objects to/from the UX process.
        - Ux process can send and receive messages to/from the Gateway
        - The pipes are easily created: multiprocessing.Pipe()
    """

    def __init__(self):
        self._streamlit_runner: StreamlitRunner = None
        """_streamlit_runner: The StreamlitRunner process class to launch the 
        streamlit application in a separated process"""

        self._parent_connection: Connection
        """_parent_connection: Connection end to use in the Gateway process"""
        self._child_connection: Connection
        """_child_connection: Connection to use in the streamlit app process"""
        self._parent_connection, self._child_connection = Pipe()
        log.debug(
            f"UxClient: Created pipes connections. "
            f"Parent:{id(self._parent_connection)} - "
            f"Child:{id(self._child_connection)}"
        )

    def start_streamlit_app(self) -> None:
        """Starts the streamlit application programmatically.

        It pass down the end of the Pipe (_child_connection) to the StreamlitRunner.
        """
        kwargs = {"gateway_connection": self._child_connection}
        self._streamlit_runner = StreamlitRunner(kwargs)
        self._streamlit_runner.start()
        log.info("UxClient starting streamlit application in a separated process")

    def send_state_to_ui(self, ux_state) -> None:
        """Sends the appropriate UxState to the streamlit process
        based on the current Gateway state.

        Args:
            ux_state: An instance of a UxState defined in the ux.ux_states.py module.
        """
        log.debug(f"UxClient UxState sent to streamlit app.")
        self._parent_connection.send(ux_state)

    def wait_for_ux_state(self):
        """Returns the UXState received from the UI process.

        It'll block until there is something to receive.
        """
        while not self._parent_connection.poll():
            time.sleep(0.5)  # ask again in the next second.

        ux_state = self._parent_connection.recv()
        log.debug("UxClient UxState received from streamlit app")
        return ux_state

