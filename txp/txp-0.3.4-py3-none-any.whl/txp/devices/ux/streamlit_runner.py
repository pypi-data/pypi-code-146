"""
This module defines the StreamlitRunner class, which is a
custom class created to run the streamlit application programmatically
in another process.
"""
# ============================ imports =========================================
import streamlit.bootstrap as bootstrap
import txp.devices.ux.remote_gateway_client
from txp.common.config import settings as txp_settings
from txp.devices.ux.remote_gateway_client import remote_gateway_client
import multiprocessing as mp
import streamlit as st
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Definition of StreamlitRunner class
# ==============================================================================
class StreamlitRunner(mp.Process):
    """This class is the Process designed to start the Gateway UX
    streamlit application programmatically.

    It can receive the necessary objects to perform IPC communication
    with the main Gateway process.
    """

    def __init__(self, kwargs):
        """
        Args:
            kwargs: Mapping of str->values, expected to be used in the streamlit process
                app.
                gateway_connection: The multiprocess.Connection end of the pipe to be used
                    in the streamlit process.
        """
        super(StreamlitRunner, self).__init__(kwargs=kwargs)
        self.daemon = True
        self.name = "StreamlitRunnerProcess"

    def run(self) -> None:
        """Starts the Streamlit server application.

        It call the custom command call_streamlit_run, which initializes a CLI context
        and calls the main_run command from streamlit.

        It replicates the internal working of the _main_run method in streamlit.cli module:
            https://github.com/streamlit/streamlit/blob/d00429604bbc319bc44f3a326f8613607310978d/lib/streamlit/cli.py#L204

        This run method will keep running the streamlit server.
        """
        log.info("StreamlitRunner: Initialize streamlit process and objects")

        gateway_conn = self._kwargs["gateway_connection"]
        log.debug(f"StreamlitRunner: Received Gateway Connection: {id(gateway_conn)}")

        remote_gateway_client.set_gateway_connection(gateway_conn)

        remote_gateway_client.wait_for_initial_state()

        st._is_running_with_streamlit = True

        args = []
        flag_options = {}
        command_line = ""
        bootstrap.run(
            txp_settings.ux.streamlit_script, command_line, args, flag_options
        )
