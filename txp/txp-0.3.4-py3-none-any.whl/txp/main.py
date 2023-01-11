# ============================ imports =========================================
from txp.devices.gateway import Gateway
from txp.common.config import settings
import logging
import signal


log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# Transitions are verbose. Enable a lower level only if debugging the Gateway State
# Machine transitions.
logging.getLogger('transitions').setLevel(logging.WARNING)


_gateway: Gateway = None


def _graceful_quit(signal_received, frame):
    _gateway.stop()


# ==============================================================================
# Main function to be called from the CLI module.
# ==============================================================================
def main():
    """The main application flow for the first Beta release.

    Currently this main entrypoint is a hardcoded to ensure that
    the Rapsberry image is properly working.

    The expected behavior is to initialize the Gateway Process and create
    the processes for:
        - Hardcoded DriversHost (By hand)
        - The streamlit web UI. (By the gateway)
    """
    log.info("Start main application for the Gateway process")

    log.info("Configuring DriversHostManager class")

    log.info(f"Samples processing mode set to: {settings.gateway.streaming_mode}")

    log.info("Creating the Gateway object instance")
    gateway = Gateway()
    global _gateway
    _gateway = gateway

    signal.signal(signal.SIGINT, _graceful_quit)

    # Starts the Gateway. Currently this starts loads all the hardwired configurations in memory
    # TODO: We should catch global exceptions and runtime errors here, and clear resources.
    gateway.start()

    # Move the gateway to Ready State.
    # In Ready state the Gateway should wait for the configuration to arrive,
    #   because harcoded configurations were removed.
    # When production phase is done, this can be removed.
    # gateway._preparing_devices_completed()

    while True:
        pass
