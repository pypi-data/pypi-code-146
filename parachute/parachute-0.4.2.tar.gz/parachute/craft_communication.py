import sys
import time
from typing import Generator
from typing import List
from typing import Union

import serial.tools.list_ports
from pymavlink import mavutil

from .data_types import Parameter
from .utils import debug


FORBIDDEN_PARAMETERS = (
    "COMPASS_DEV_ID",
    "COMPASS_DEV_ID2",
    "COMPASS_DEV_ID3",
    "COMPASS_DEV_ID4",
    "COMPASS_DEV_ID5",
    "COMPASS_DEV_ID6",
    "COMPASS_DEV_ID7",
    "COMPASS_DEV_ID8",
    "COMPASS_MOTCT",
    "ESC_CALIBRATION",
    "FENCE_TOTAL",
    "H_SV_MAN",
    "H_SW2_H3_ENABLE",
    "H_SW_H3_ENABLE",
    "INS_GYROFFS_X",
    "INS_GYROFFS_Y",
    "INS_GYROFFS_Z",
    "MIS_TOTAL",
    "SYS_NUM_RESETS",
)


def discover_socket() -> str:
    """Try to autodiscover the socket the craft is on."""
    from pprint import pformat

    devices = [x.__dict__ for x in serial.tools.list_ports.comports()]
    debug("Serial devices:\n" + "\n".join(pformat(x) for x in devices))
    for port in devices:
        manufacturer = port.get("manufacturer")
        hwid = port.get("hwid")
        if (manufacturer and ("ArduPilot" in manufacturer)) or (
            hwid and ("1209:5741" in hwid)
        ):
            return port["device"]

    if not devices:
        sys.exit(
            "Could not autodetect your socket, please specify it "
            "manually with `--socket`."
        )

    # Just return the first device, as we're out of options.
    return devices[0]["device"]


class CraftCommunication:
    def __init__(self, socket: str, baud_rate: int):
        socket = socket if socket != "auto" else discover_socket()
        self._conn = mavutil.mavlink_connection(socket, baud=baud_rate)
        self._conn.wait_heartbeat()
        self._target_system = self._conn.target_system
        self._target_component = self._conn.target_component

    def force_accept_calibration(self, component: str):
        """Force the FC to accept the current calibration."""

        param2 = 0
        param5 = 0
        if component == "accel":
            param5 = 76
        elif component == "compass":
            param2 = 76
        else:
            param2 = 76
            param5 = 76
        self._conn.mav.command_long_send(
            self._target_system,
            self._target_component,
            mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION,
            0,
            0,
            param2,
            0,
            0,
            param5,
            0,
            0,
        )

    def reset_to_default(self):
        """Reset all parameters to their default values."""
        self._conn.mav.command_long_send(
            self._target_system,
            self._target_component,
            mavutil.mavlink.MAV_CMD_PREFLIGHT_STORAGE,
            0,
            2.0,
            0,
            0,
            0,
            0,
            0,
            0,
        )

    def reboot(self) -> None:
        """Reboot the craft."""
        self._conn.reboot_autopilot()

    def get_param(self, parameter: Parameter) -> Parameter:
        """Retrieve a parameter from a craft."""
        # Request the parameter.
        self._conn.mav.param_request_read_send(
            self._target_system,
            self._target_component,
            parameter.name.encode(),
            -1,
        )

        # Wait for the response.
        start = time.time()
        while True:
            if time.time() > start + 5:
                raise ValueError(
                    f"Craft did not respond to a query about {parameter.name}, the"
                    " parameter might not exist."
                )

            message = self._conn.recv_match(blocking=True).to_dict()
            if (
                message.get("mavpackettype", "") == "PARAM_VALUE"
                and message["param_id"] == parameter.name
            ):
                break
        return Parameter.from_message(message)

    def set_param(self, parameter: Parameter) -> None:
        """Set a parameter on a craft."""
        self._conn.mav.param_set_send(
            self._target_system,
            self._target_component,
            parameter.name.encode(),
            parameter.value,
            parameter.type,
        )

    def list_params(self) -> Generator[Union[List[str], int, Parameter], None, None]:
        """
        Read all the parameters from a craft.

        Yields the status as a list in first iteration, a count of all
        parameters in the second, and the parameters after that.
        """
        # From https://www.ardusub.com/developers/pymavlink.html.
        self._conn.mav.param_request_list_send(
            self._target_system, self._target_component, 1
        )
        status = []
        # This keeps track of the FSM state. If it's 0, we need to output the
        # status, 1 we need to output the count, and 2 is parameters until
        # we're done.
        fsm_state = 0
        while True:
            # Read all messages, as AP eventually freezes if we try to
            # ignore too many message types.
            message = self._conn.recv_match(blocking=True).to_dict()

            # The FC sends the status messages first and then starts sending
            # parameters, but it still might send unrelated status messages
            # after that. We're only interested in the first messages.
            if message.get("mavpackettype", "") == "STATUSTEXT" and fsm_state == 0:
                status.append(message["text"])
                continue
            elif message.get("mavpackettype", "") != "PARAM_VALUE":
                continue

            if fsm_state == 0:
                # We're done with status messages, yield the status.
                yield status
                fsm_state = 1
                continue
            elif fsm_state == 1:
                # This is the first parameter, yield the count and then the
                # parameter itself right away.
                yield message["param_count"]
                fsm_state = 2

            if (
                message["param_id"].startswith("STAT_")
                or message["param_id"] in FORBIDDEN_PARAMETERS
            ):
                # Ignore statistical parameters and parameters that should not
                # be changed manually.
                continue

            parameter = Parameter.from_message(message)
            yield parameter
            if parameter.index == message["param_count"] - 1:
                break
