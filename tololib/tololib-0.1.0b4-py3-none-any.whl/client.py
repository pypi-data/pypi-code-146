import logging
import socket
from select import select
from typing import List, Optional, Tuple, Union

from .command import Command
from .const import (
    DEFAULT_RETRY_COUNT,
    DEFAULT_RETRY_TIMEOUT,
    AromaTherapy,
    LampMode,
    SettingsMessageLength,
    StatusMessageLength,
)
from .errors import ResponseTimedOutError
from .message import Message
from .message_info import SettingsInfo, StatusInfo

logger = logging.getLogger(__name__)


class ToloClient(object):
    def __init__(self, address: str, port: int = 51500) -> None:
        self._address = address
        self._port = port

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message: Message) -> int:
        """Send a message to the server.

        Args:
            message (Message): The message to be send to the server.

        Returns:
            Number of bytes sent.
        """
        raw_bytes = bytes(message)
        logger.debug(
            "sending %s to %s" % (raw_bytes.hex(), (self._address, self._port))
        )
        return self._socket.sendto(raw_bytes, (self._address, self._port))

    def receive_message(self, wait_timeout: Optional[float] = None) -> Message:
        incoming = select([self._socket], [], [], wait_timeout)
        if incoming[0]:
            raw_bytes, sender = self._socket.recvfrom(4096)
            logger.debug("received %s from %s" % (raw_bytes.hex(), sender))
            return Message.from_bytes(raw_bytes)
        else:
            raise ResponseTimedOutError()

    def send_wait_response(
        self, message: Message, resend_timeout: Optional[float] = None, retries: int = 3
    ) -> Message:
        for _ in range(retries):
            self.send_message(message)
            try:
                response = self.receive_message(wait_timeout=resend_timeout)
                return response
            except ResponseTimedOutError:
                continue
        raise ResponseTimedOutError()

    def get_status_info(
        self, resend_timeout: Optional[float] = None, retries: int = 3
    ) -> StatusInfo:
        response = self.send_wait_response(
            Message(Command.STATUS, StatusMessageLength.REQUEST, b"\xFF"),
            resend_timeout,
            retries,
        )
        return StatusInfo(response.info)

    def get_settings_info(
        self, resend_timeout: Optional[float] = None, retries: int = 3
    ) -> SettingsInfo:
        response = self.send_wait_response(
            Message(Command.SETTINGS, SettingsMessageLength.REQUEST, b"\xFF"),
            resend_timeout,
            retries,
        )
        return SettingsInfo(response.info)

    @staticmethod
    def discover(
        address: str = "255.255.255.255", port: int = 51500, wait_timeout: float = 1
    ) -> List[Tuple[Message, Union[str, Tuple[str, int]]]]:
        devices = []

        discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        discovery_socket.sendto(
            bytes(Message(Command.STATUS, StatusMessageLength.REQUEST, b"\xFF")),
            (address, port),
        )

        while True:
            incoming_data = select([discovery_socket], [], [], wait_timeout)
            if incoming_data[0]:
                raw_bytes, sender = discovery_socket.recvfrom(4096)
                message = Message.from_bytes(raw_bytes)
                devices.append((message, sender))
            else:
                discovery_socket.close()
                return devices

    def close(self) -> None:
        self._socket.close()

    def set_power_on(
        self,
        power_on: bool,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_POWER_ON, power_on, b"\xFF"), retry_timeout, retry_count
        )

    def set_fan_on(
        self,
        fan_on: bool,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_FAN_ON, fan_on, b"\xFF"), retry_timeout, retry_count
        )

    def set_aroma_therapy_on(
        self,
        aroma_therapy_on: bool,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_AROMA_THERAPY_ON, aroma_therapy_on, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def set_lamp_on(
        self,
        lamp_on: bool,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_LAMP_ON, lamp_on, b"\xFF"), retry_timeout, retry_count
        )

    def set_sweep_on(
        self,
        sweep_on: bool,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_SWEEP_ON, sweep_on, b"\xFF"), retry_timeout, retry_count
        )

    def set_salt_bath_on(
        self,
        salt_bath_on: bool,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_SALT_BATH_ON, salt_bath_on, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def set_target_temperature(
        self,
        target_temperature: int,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_TARGET_TEMPERATURE, target_temperature, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def set_target_humidity(
        self,
        target_humidity: int,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_TARGET_HUMIDITY, target_humidity, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def set_power_timer(
        self,
        power_timer: Optional[int],
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_POWER_TIMER, power_timer, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def set_salt_bath_timer(
        self,
        salt_bath_timer: Optional[int],
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_SALT_BATH_TIMER, salt_bath_timer, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def set_aroma_therapy(
        self,
        aroma_therapy: AromaTherapy,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_AROMA_THERAPY, aroma_therapy, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def set_sweep_timer(
        self,
        sweep_timer: int,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_SWEEP_TIMER, sweep_timer, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def set_lamp_mode(
        self,
        lamp_mode: LampMode,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_LAMP_MODE, lamp_mode, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def set_fan_timer(
        self,
        fan_timer: Optional[int],
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.SET_FAN_TIMER, fan_timer, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def lamp_change_color(
        self,
        retry_timeout: Optional[float] = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ) -> Optional[Message]:
        return self.send_wait_response(
            Message(Command.LAMP_CHANGE_COLOR, 1, b"\xFF"),
            retry_timeout,
            retry_count,
        )

    def __del__(self) -> None:
        self.close()
