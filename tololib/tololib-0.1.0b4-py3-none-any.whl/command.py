from enum import Enum
from typing import Any, NamedTuple, Type, Union

from .command_data_type import (
    Boolean,
    CommandDataType,
    Integer,
    IntegerEnum,
    OptionalInteger,
)
from .const import AromaTherapy, LampMode, SettingsMessageLength, StatusMessageLength

CommandTypeHint = Union[Type[int], Type[bool], int, None]


class CommandDefinition(NamedTuple):
    code: int
    default_value: Any
    command_data_type: CommandDataType[Any]


class Command(CommandDefinition, Enum):
    """
    Set target temperature.

    App allowss setting it from -20(?!) to 60 degrees.
    """

    SET_TARGET_TEMPERATURE = CommandDefinition(4, 40, Integer(-20, 60))

    SET_POWER_TIMER = CommandDefinition(8, None, OptionalInteger(1, 60, 61))

    SET_POWER_ON = CommandDefinition(14, False, Boolean())

    SET_AROMA_THERAPY_ON = CommandDefinition(18, False, Boolean())

    SET_AROMA_THERAPY = CommandDefinition(20, AromaTherapy.A, IntegerEnum(AromaTherapy))

    GET_AROMA_THERAPY = CommandDefinition(21, AromaTherapy.A, IntegerEnum(AromaTherapy))

    GET_SWEEP_TIMER = CommandDefinition(26, False, Integer(0, 8))

    SET_SWEEP_TIMER = CommandDefinition(28, None, Integer(0, 8))

    SET_LAMP_ON = CommandDefinition(30, False, Boolean())

    SET_FAN_ON = CommandDefinition(34, False, Boolean())

    SET_FAN_TIMER = CommandDefinition(36, None, OptionalInteger(1, 60, 61))

    SET_TARGET_HUMIDITY = CommandDefinition(38, 95, Integer(60, 99))

    SET_SWEEP_ON = CommandDefinition(51, False, Boolean())

    GET_FAN_TIMER = CommandDefinition(53, None, OptionalInteger(0, 60, 61))

    SET_SALT_BATH_ON = CommandDefinition(54, False, Boolean())

    SET_SALT_BATH_TIMER = CommandDefinition(56, None, OptionalInteger(1, 60, 255))

    GET_SALT_BATH_TIMER = CommandDefinition(59, None, OptionalInteger(0, 60, 61))

    SET_LAMP_MODE = CommandDefinition(60, LampMode.MANUAL, IntegerEnum(LampMode))

    GET_LAMP_MODE = CommandDefinition(61, False, Boolean())

    LAMP_CHANGE_COLOR = CommandDefinition(62, 1, Integer(1, 1))

    """
    Request/reply with status information of the sauna.

    Data byte is used to indicate message length (0 for request, 17 for reply).
    """
    STATUS = CommandDefinition(
        97, StatusMessageLength.REQUEST, IntegerEnum(StatusMessageLength)
    )

    """
    Request/reply with settings information of the sauna.

    Data byte is used to indicate message length (0 for request, 8 for reply).
    """
    SETTINGS = CommandDefinition(
        99, SettingsMessageLength.REQUEST, IntegerEnum(SettingsMessageLength)
    )

    @classmethod
    def from_code(cls, code: int) -> "Command":
        for command in cls:
            if command.code == code:
                return command
        else:
            raise ValueError("unknown command code %s" % code)
