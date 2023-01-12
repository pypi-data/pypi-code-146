from typing import Union

from .command import Command, CommandTypeHint
from .const import MESSAGE_PREFIX, MESSAGE_SUFFIX
from .errors import CommandParseError


class Message(object):
    """Class representing a message sent over network.

    By default, the TOLO App Box listens on UDP port 51500 for receiving control messages.
    Each messaged received by TOLO App Box is answered with a message with the same structure, but different values.
    This class represents such request/response messages and provides functionality for parsing, validating and
    creating messages.

    Each message has the following structure:
      * 2 bytes fixed `0xAAAA`
      * 1 byte command (see Command enumeration)
      * 1 byte data (according to the command)
      * x bytes response message (depends on the command and the reply from TOLO App Box)
      * 2 bytes fixed `0x5555`
      * 1 byte checksum, byte-wise XOR of all previously mentioned data
    """

    PREFIX = MESSAGE_PREFIX
    SUFFIX = MESSAGE_SUFFIX

    def __init__(
        self,
        command: Command,
        data: CommandTypeHint,
        info: Union[bytes, bytearray] = b"",
    ):
        command.command_data_type.validate(data, raise_error=True)

        self._command = command
        self._data = data
        self._info = bytes(info)

    @property
    def command(self) -> Command:
        return self._command

    @property
    def data(self) -> CommandTypeHint:
        return self._data

    @property
    def info(self) -> bytes:
        return self._info

    def __str__(self) -> str:
        return "<%s: cmd: %s, data: %d, info: %s>" % (
            self.__class__.__name__,
            self._command.name,
            self._command.command_data_type.to_byte_any(self._data),
            self._info.hex(),
        )

    def __bytes__(self) -> bytes:
        data = (
            self.PREFIX
            + bytes(
                [
                    self._command.code,
                    self._command.command_data_type.to_byte(self._data),
                ]
            )
            + self._info
            + self.SUFFIX
        )
        return data + bytes([self.generate_crc(data)])

    @staticmethod
    def from_bytes(b: bytes) -> "Message":
        if not Message.validate_meta(b):
            raise ValueError("invalid meta information")

        command = Command.from_code(b[2])
        try:
            data = command.command_data_type.to_typed(b[3])
        except ValueError as e:
            raise CommandParseError(
                "Cannot parse data for command %s: %s" % (command.name, str(e))
            )

        return Message(command=command, data=data, info=b[4:-3])

    @staticmethod
    def generate_crc(data: bytes) -> int:
        crc = 0x00
        for b in data:
            crc = crc ^ b
        return crc

    @staticmethod
    def validate_crc(raw_bytes: bytes) -> bool:
        return Message.generate_crc(raw_bytes[:-1]) == raw_bytes[-1]

    @classmethod
    def validate_meta(cls, raw_bytes: bytes) -> bool:
        """Validates meta data of message bytes.

        The validation will check for prefix, suffix and CRC.
        It will NOT check for valid code or payload.

        Args:
            raw_bytes (bytes): binary data to be checked

        Returns:
            True if the check was successful and the meta data is as expected, False otherwise.
        """
        if not raw_bytes.startswith(cls.PREFIX):
            return False
        if not raw_bytes[:-1].endswith(cls.SUFFIX):
            return False
        return cls.validate_crc(raw_bytes)
