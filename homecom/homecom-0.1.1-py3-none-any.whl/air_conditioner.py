from enum import StrEnum

from .abstract_auth import AbstractAuth


class AcControl(StrEnum):
    ON = "on"
    OFF = "off"


class OperationMode(StrEnum):
    AUTO = "auto"
    DRY = "dry"
    HEAT = "heat"
    COOL = "cool"


class AirConditioner:
    """Class that represents a AirConditioner object in the HomeCom API."""

    def __init__(self, raw_data: dict, auth: AbstractAuth):
        """Initialize a air conditioner object."""
        self.raw_data = raw_data
        self.auth = auth

    # Note: each property name maps the name in the returned data

    @property
    def id(self) -> int:
        """Return the ID of the AC."""
        return self.raw_data["deviceId"]

    async def async_set_temperature(self, temperature: float):
        """Set the target temperature."""
        resp = await self.auth.request(
            "put",
            f"pointt-api/api/v1/gateways/{self.id}/resource/airConditioning/temperatureSetpoint",
            json={"value": temperature},
        )
        print(await resp.text())
        resp.raise_for_status()

    async def async_set_operation_mode(self, operation_mode: OperationMode):
        """Set the operation mode, like `heat`, `cool`, etc."""
        resp = await self.auth.request(
            "put",
            f"pointt-api/api/v1/gateways/{self.id}/resource/airConditioning/operationMode",
            json={"value": operation_mode},
        )
        print(await resp.text())
        resp.raise_for_status()

    async def async_set_ac_control(self, ac_control: AcControl):
        """Turn the AC on/off."""
        resp = await self.auth.request(
            "put",
            f"pointt-api/api/v1/gateways/{self.id}/resource/airConditioning/acControl",
            json={"value": ac_control},
        )
        print(await resp.text())
        resp.raise_for_status()
