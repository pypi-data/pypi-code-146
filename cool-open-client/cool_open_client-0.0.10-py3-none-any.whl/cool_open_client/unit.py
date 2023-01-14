from abc import ABC, abstractmethod
import asyncio
from functools import cached_property
import logging

from .utils.updatable import Updatable
from .cool_automation_client import CoolAutomationClient, UnitUpdateMessage

LOGGER = logging.getLogger(__package__)


class UnitCallback(ABC):
    @abstractmethod
    def unit_update_callback(self):
        pass


class HVACUnit(Updatable):
    """The logical clas repressentation of the HVAC unit"""

    def __init__(
        self,
        id: str,
        name: str,
        active_setpoint: int,
        active_operation_status: int,
        active_operation_mode: int,
        ambient_temperature: float,
        active_fan_mode: int,
        active_swing_mode: int,
        temerature_range: list[int],
        supported_operation_statuses: list[str],
        supported_operation_modes: list[str],
        supported_fan_modes: list[str],
        supported_swing_modes: list[str],
        is_half_degree: bool,
        client: CoolAutomationClient,
        callbacks: list[UnitCallback] = None,
        event_loop: asyncio.AbstractEventLoop = None,
    ) -> None:
        self._id = id
        self._change_filter_status: bool = False
        self._active_setpoint: int = active_setpoint
        self._ambient_temperature = ambient_temperature
        self._active_operation_status: int = active_operation_status
        self._active_operation_mode: int = active_operation_mode
        self._active_fan_mode: int = active_fan_mode
        self._active_swing_mode: int = active_swing_mode
        self._name: str = name
        self._temperature_range = temerature_range
        self._supported_operation_statuses: list[str] = supported_operation_statuses
        self._supported_operation_modes: list[str] = supported_operation_modes
        self._supported_fan_modes: list[str] = supported_fan_modes
        self._supported_swing_modes: list[str] = supported_swing_modes
        self._is_half_degree: bool = is_half_degree
        self._client = client
        self._client.register_for_updates(self)
        self._callbacks: list[UnitCallback] = callbacks if callbacks is not None else []
        self.logger = client.logger
        self.event_loop = event_loop
        self._update_pending: bool = True

    def regiter_callback(self, unit_callback: UnitCallback) -> None:
        self._callbacks.append(unit_callback)

    async def set_operation_status(self, status: str):
        """Set the operation status of the HVAC unit

        Args:
            status (str): String representation of the operation status
        """
        await self._client.set_operation_status(unit_id=self._id, status=status)

    async def set_opration_mode(self, mode: str):
        """Set the operation mode of the HVAC unit

        Args:
            mode (str): String representation of the operation mode
        """
        await self._client.set_operation_mode(unit_id=self._id, mode=mode)

    async def set_swing_mode(self, mode: str):
        """Set the swing mode of the HVAC unit

        Args:
            mode (str): String representation of the swing mode
        """
        await self._client.set_swing_mode(unit_id=self._id, mode=mode)

    async def set_temperature_set_point(self, setpoint: int):
        """Set the set point temperature of the HVAC unit

        Args:
            setpoint (int): The desired setpoint of the HVAC unit
        """
        await self._client.set_temperature_set_point(unit_id=self._id, temp=setpoint)

    async def set_fan_mode(self, mode: str):
        """Set the fan mode of the HVAC unit

        Args:
            mode (str): String representation of the fan mode
        """
        await self._client.set_fan_mode(unit_id=self._id, mode=mode)

    def notify(self, message: UnitUpdateMessage):
        self._update_unit(message)

    def _update_unit(self, message: UnitUpdateMessage, with_callback: bool = True):
        self._active_operation_mode = message.operation_mode
        self._active_fan_mode = message.fan_mode
        self._active_operation_status = message.operation_status
        self._active_setpoint = message.setpoint
        self._active_swing_mode = message.swing
        self._ambient_temperature = message.ambient_temperature
        self.logger.debug("Unit updated %s", self.name)
        self._update_pending = True
        if with_callback:
            for callback in self._callbacks:
                if not asyncio.iscoroutinefunction(callback.unit_update_callback):
                    callback.unit_update_callback()
                else:
                    self.event_loop.run_until_complete(callback.unit_update_callback())

    async def refresh(self) -> None:
        if not self._update_pending:
            units = await self._client.get_updated_controllable_unit(self._id)
            self._update_unit(units, with_callback=False)

    def reset_update(self) -> None:
        self._update_pending = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    @property
    def is_half_degree(self) -> bool:
        return self._is_half_degree

    @property
    def operation_mode(self):
        return self._active_operation_mode

    @property
    def fan_mode(self):
        return self._active_fan_mode

    @property
    def operation_status(self):
        return self._active_operation_status

    @property
    def setpoint(self):
        return self._active_setpoint

    @property
    def swing_mode(self):
        return self._active_swing_mode

    def get_updatable_id(self):
        return self._id

    @property
    def is_on(self) -> bool:
        return self.operation_status == "on"

    @property
    def is_fan_mode(self) -> bool:
        return bool(self._supported_fan_modes)

    @property
    def is_swing_mode(self) -> bool:
        return bool(self._supported_swing_modes)

    @cached_property
    def operation_modes(self) -> list[str]:
        return self._supported_operation_modes.copy()

    @cached_property
    def fan_modes(self) -> list[str]:
        return self._supported_fan_modes.copy()

    @property
    def swing_modes(self) -> list[str]:
        if self.is_on:
            return self._supported_swing_modes.copy()
        else:
            return ["off"]

    @property
    def ambient_temperature(self) -> float:
        return self._ambient_temperature

    @property
    def min_temp(self) -> float:
        if self._active_operation_mode == "HEAT":
            return self._temperature_range['1'][0]
        return self._temperature_range['0'][0]

    @property
    def max_temp(self) -> float:
        if self._active_operation_mode == "HEAT":
            return self._temperature_range['1'][1]
        return self._temperature_range['0'][1]

    async def turn_on(self):
        await self.set_operation_status("on")

    async def turn_off(self):
        await self.set_operation_status("off")

    def __str__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )
