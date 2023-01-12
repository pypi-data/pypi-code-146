from typing import Optional, cast

from .command import Command
from .command_data_type import Integer, IntegerEnum, OptionalInteger
from .const import AromaTherapy, Calefaction, LampMode, Model


class MessageInfo(bytearray):
    LENGTH = -1

    def __init__(self, initial_value: Optional[bytes] = None) -> None:
        if initial_value is None:
            super().__init__(b"\x00" * self.LENGTH)
        elif len(initial_value) == self.LENGTH:
            super().__init__(initial_value)
        else:
            raise ValueError(
                "initial value must have length %d, %d given"
                % (self.LENGTH, len(initial_value))
            )


class StatusInfo(MessageInfo):
    """
      * 0: int(self._power_on),
      * 1: self._current_temperature,
      * 2: 61 if self._power_timer is None else self._power_timer,
      * 3: (64 if self._flow_in else 0) + (16 if self._flow_out else 0) + self._calefaction.value,
     4: int(self._aroma_therapy_on),
     5: int(self._sweep_on),
     6: 0,  # TODO descaling - what is this?
     7: int(self._lamp_on),
     8: self._water_level,
     9: int(self._fan_on),
    10: 61 if self._fan_timer is None else self._fan_timer,
    11: self._current_humidity,
    12: self._tank_temperature,
    13: 0,  # TODO unused?
    14: self._model.value,
    15: self._salt_bath_on,
    16: 0 if self._salt_bath_timer is None else self._salt_bath_timer
    """

    LENGTH = 17

    WATER_LEVELS_PERCENTAGE = {0: 0, 1: 33, 2: 66, 3: 100}

    @property
    def power_on(self) -> bool:
        return cast(bool, Command.SET_POWER_ON.command_data_type.to_typed(self[0]))

    @power_on.setter
    def power_on(self, power_on: bool) -> None:
        self[0] = Command.SET_POWER_ON.command_data_type.to_byte(power_on)

    @property
    def current_temperature(self) -> int:
        return Integer(0, 100).to_typed(self[1])

    @current_temperature.setter
    def current_temperature(self, current_temperature: int) -> None:
        self[1] = Integer(0, 100).to_byte(current_temperature)

    @property
    def power_timer(self) -> Optional[int]:
        return OptionalInteger(0, 60, 61).to_typed(self[2])

    @power_timer.setter
    def power_timer(self, power_timer: Optional[int]) -> None:
        self[2] = OptionalInteger(0, 60, 61).to_byte(power_timer)

    @property
    def flow_in(self) -> bool:
        return bool(self[3] & 64)

    @flow_in.setter
    def flow_in(self, flow_in: bool) -> None:
        self[3] = (self[3] & 191) | (64 if flow_in else 0)

    @property
    def flow_out(self) -> bool:
        return bool(self[3] & 16)

    @flow_out.setter
    def flow_out(self, flow_out: bool) -> None:
        self[3] = (self[3] & 239) | (16 if flow_out else 0)

    @property
    def calefaction(self) -> Calefaction:
        return Calefaction(self[3] & 3)

    @calefaction.setter
    def calefaction(self, calefaction: Calefaction) -> None:
        self[3] = (self[3] & 252) | IntegerEnum(Calefaction).to_byte(calefaction)

    @property
    def aroma_therapy_on(self) -> bool:
        return cast(
            bool, Command.SET_AROMA_THERAPY_ON.command_data_type.to_typed(self[4])
        )

    @aroma_therapy_on.setter
    def aroma_therapy_on(self, aroma_therapy_on: bool) -> None:
        self[4] = Command.SET_AROMA_THERAPY_ON.command_data_type.to_byte(
            aroma_therapy_on
        )

    @property
    def sweep_on(self) -> bool:
        return cast(bool, Command.GET_SWEEP_TIMER.command_data_type.to_typed(self[5]))

    @sweep_on.setter
    def sweep_on(self, sweep_on: bool) -> None:
        self[5] = Command.GET_SWEEP_TIMER.command_data_type.to_byte(sweep_on)

    @property
    def lamp_on(self) -> bool:
        return cast(bool, Command.SET_LAMP_ON.command_data_type.to_typed(self[7]))

    @lamp_on.setter
    def lamp_on(self, lamp_on: bool) -> None:
        self[7] = Command.SET_LAMP_ON.command_data_type.to_byte(lamp_on)

    @property
    def water_level(self) -> int:
        return Integer(0, 3).to_typed(self[8])

    @water_level.setter
    def water_level(self, water_level: int) -> None:
        self[8] = Integer(0, 3).to_byte(water_level)

    @property
    def water_level_percent(self) -> int:
        """Helper method to convert 0..3 water level representation to percent."""
        return self.WATER_LEVELS_PERCENTAGE[self.water_level]

    @property
    def fan_on(self) -> bool:
        return cast(bool, Command.SET_FAN_ON.command_data_type.to_typed(self[9]))

    @fan_on.setter
    def fan_on(self, fan_on: bool) -> None:
        self[9] = Command.SET_FAN_ON.command_data_type.to_byte(fan_on)

    @property
    def fan_timer(self) -> Optional[int]:
        return cast(
            Optional[int], Command.GET_FAN_TIMER.command_data_type.to_typed(self[10])
        )

    @fan_timer.setter
    def fan_timer(self, fan_timer: Optional[int]) -> None:
        self[10] = Command.GET_FAN_TIMER.command_data_type.to_byte(fan_timer)

    @property
    def current_humidity(self) -> int:
        return Integer(0, 100).to_typed(self[11])

    @current_humidity.setter
    def current_humidity(self, current_humidity: int) -> None:
        self[11] = Integer(0, 100).to_byte(current_humidity)

    @property
    def tank_temperature(self) -> int:
        return Integer(0, 255).to_typed(self[12])

    @tank_temperature.setter
    def tank_temperature(self, tank_temperature: int) -> None:
        self[12] = Integer(0, 255).to_byte(tank_temperature)

    @property
    def model(self) -> Model:
        return IntegerEnum(Model).to_typed(self[14])

    @model.setter
    def model(self, model: Model) -> None:
        self[14] = IntegerEnum(Model).to_byte(model)

    @property
    def salt_bath_on(self) -> bool:
        return cast(bool, Command.SET_SALT_BATH_ON.command_data_type.to_typed(self[15]))

    @salt_bath_on.setter
    def salt_bath_on(self, salt_bath_on: bool) -> None:
        self[15] = Command.SET_SALT_BATH_ON.command_data_type.to_byte(salt_bath_on)

    @property
    def salt_bath_timer(self) -> Optional[int]:
        return cast(
            Optional[int],
            Command.GET_SALT_BATH_TIMER.command_data_type.to_typed(self[16]),
        )

    @salt_bath_timer.setter
    def salt_bath_timer(self, salt_bath_timer: Optional[int]) -> None:
        self[16] = Command.GET_SALT_BATH_TIMER.command_data_type.to_byte(
            salt_bath_timer
        )

    def __str__(self) -> str:
        return "\n".join(
            [
                "Power:               %s" % ("ON" if self.power_on else "OFF"),
                "Current Temperature: %d" % self.current_temperature,
                "Power Timer:         %s" % self.power_timer,
                "Flow in:             %s" % ("YES" if self.flow_in else "NO"),
                "Flow out:            %s" % ("YES" if self.flow_out else "NO"),
                "Calefaction:         %s" % self.calefaction.name,
                "Aroma Therapy:       %s" % ("ON" if self.aroma_therapy_on else "OFF"),
                "Sweep:               %s" % ("ON" if self.sweep_on else "OFF"),
                # 'Descaling:           %s' % ('YES' if self.descaling else 'NO'), TODO what is this?
                "Lamp:                %s" % ("ON" if self.lamp_on else "OFF"),
                "Water Level:         %s" % self.water_level,
                "Fan:                 %s" % ("ON" if self.fan_on else "OFF"),
                "Fan Timer:           %s"
                % ("OFF" if self.fan_timer is None else str(self.fan_timer)),
                "Current Humidity:    %s" % self.current_humidity,
                "Tank Temperature:    %s" % self.tank_temperature,
                "Model:               %s" % self.model.name,
                "Salt Bath On:        %s" % ("ON" if self.salt_bath_on else "OFF"),
                "Salt Bath Timer:     %s"
                % (
                    "OFF" if self.salt_bath_timer is None else str(self.salt_bath_timer)
                ),
            ]
        )


class SettingsInfo(MessageInfo):
    """
    0: self._target_temperature,
    1: 255 if self._power_timer is None else self._power_timer,
    2: self._aroma_therapy.value,
    3: self._sweep_timer,
    4: 61 if self._fan_timer is None else self._fan_timer,
    5: self._target_humidity,
    6: 255 if self._salt_bath_timer is None else self._salt_bath_timer,
    7: self._lamp_mode.value

    """

    LENGTH = 8

    @property
    def target_temperature(self) -> int:
        return cast(
            int, Command.SET_TARGET_TEMPERATURE.command_data_type.to_typed(self[0])
        )

    @target_temperature.setter
    def target_temperature(self, target_temperature: int) -> None:
        self[0] = Command.SET_TARGET_TEMPERATURE.command_data_type.to_byte(
            target_temperature
        )

    @property
    def power_timer(self) -> Optional[int]:
        return cast(
            Optional[int], Command.SET_POWER_TIMER.command_data_type.to_typed(self[1])
        )

    @power_timer.setter
    def power_timer(self, power_timer: Optional[int]) -> None:
        self[1] = Command.SET_POWER_TIMER.command_data_type.to_byte(power_timer)

    @property
    def aroma_therapy(self) -> AromaTherapy:
        return cast(
            AromaTherapy, Command.SET_AROMA_THERAPY.command_data_type.to_typed(self[2])
        )

    @aroma_therapy.setter
    def aroma_therapy(self, aroma_therapy: AromaTherapy) -> None:
        self[2] = Command.SET_AROMA_THERAPY.command_data_type.to_byte(aroma_therapy)

    @property
    def sweep_timer(self) -> int:
        return cast(int, Command.SET_SWEEP_TIMER.command_data_type.to_typed(self[3]))

    @sweep_timer.setter
    def sweep_timer(self, sweep_timer: int) -> None:
        self[3] = Command.SET_SWEEP_TIMER.command_data_type.to_byte(sweep_timer)

    @property
    def fan_timer(self) -> Optional[int]:
        return cast(
            Optional[int], Command.SET_FAN_TIMER.command_data_type.to_typed(self[4])
        )

    @fan_timer.setter
    def fan_timer(self, fan_timer: Optional[int]) -> None:
        self[4] = Command.SET_FAN_TIMER.command_data_type.to_byte(fan_timer)

    @property
    def target_humidity(self) -> int:
        return cast(
            int, Command.SET_TARGET_HUMIDITY.command_data_type.to_typed(self[5])
        )

    @target_humidity.setter
    def target_humidity(self, target_humidity: int) -> None:
        self[5] = Command.SET_TARGET_HUMIDITY.command_data_type.to_byte(target_humidity)

    @property
    def salt_bath_timer(self) -> Optional[int]:
        return cast(
            Optional[int],
            Command.SET_SALT_BATH_TIMER.command_data_type.to_typed(self[6]),
        )

    @salt_bath_timer.setter
    def salt_bath_timer(self, salt_bath_timer: Optional[int]) -> None:
        self[6] = Command.SET_SALT_BATH_TIMER.command_data_type.to_byte(salt_bath_timer)

    @property
    def lamp_mode(self) -> LampMode:
        return cast(LampMode, Command.SET_LAMP_MODE.command_data_type.to_typed(self[7]))

    @lamp_mode.setter
    def lamp_mode(self, lamp_mode: LampMode) -> None:
        self[7] = Command.SET_LAMP_MODE.command_data_type.to_byte(lamp_mode)

    def __str__(self) -> str:
        return "\n".join(
            [
                "Target Temperature: %d" % self.target_temperature,
                "Power Timer:        %s" % self.power_timer,
                "Aroma Therapy:      %s" % self.aroma_therapy,
                "Sweep Timer:        %s" % self.sweep_timer,
                "Fan Timer:          %s" % self.fan_timer,
                "Target Humidity:    %s" % self.target_humidity,
                "Salt Bath Timer:    %s" % self.salt_bath_timer,
                "Lamp Mode:          %s" % self.lamp_mode,
            ]
        )
