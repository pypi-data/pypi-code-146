from http import client
from typing import List
from .cool_automation_client import CoolAutomationClient
from .unit import HVACUnit


class HVACUnitsFactory:
    @classmethod
    async def create(cls, token: str = None):
        if token is None:
            raise ValueError("token is required")

        client = await CoolAutomationClient.create(token)
        return cls(client)

    def __init__(self, client=None, event_loop=None) -> None:
        self._client = client
        self._event_loop = event_loop

    async def generate_units_from_api(self) -> List[HVACUnit]:
        units = await self._client.get_controllable_units()
        hvac_units: List[HVACUnit] = []
        for id, unit in units.data.items():
            if unit["type"] == 1:
                hvac_unit = HVACUnit(
                    id,
                    unit["name"],
                    active_fan_mode=self._client.fan_modes.get(unit["activeFanMode"]),
                    active_operation_mode=self._client.operation_modes.get(unit["activeOperationMode"]),
                    active_operation_status=self._client.operation_statuses.get(unit["activeOperationStatus"]),
                    active_setpoint=unit["activeSetpoint"],
                    active_swing_mode=self._client.swing_modes.get(unit["activeSwingMode"]),
                    ambient_temperature=unit["ambientTemperature"],
                    temerature_range=unit["temperatureLimits"],
                    supported_fan_modes=[self._client.fan_modes.get(mode) for mode in unit["supportedFanModes"]],
                    supported_operation_modes=[
                        self._client.operation_modes.get(mode) for mode in unit["supportedOperationModes"]
                    ],
                    supported_operation_statuses=[
                        self._client.operation_statuses.get(status) for status in unit["supportedOperationStatuses"]
                    ],
                    supported_swing_modes=[self._client.swing_modes.get(mode) for mode in unit["supportedSwingModes"]],
                    is_half_degree=unit["isHalfCDegreeEnabled"],
                    client=self._client,
                    event_loop=self._event_loop,
                )
                hvac_units.append(hvac_unit)
        return hvac_units
