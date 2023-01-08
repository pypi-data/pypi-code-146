from enum import StrEnum, Flag, IntFlag

from .abstract_auth import AbstractAuth


class AcControl(IntFlag):
    ON = 0
    OFF = 1

    @classmethod
    def from_str(cls, input: str):
        return cls(int(input == "off"))

    def to_str(self):
        if self == AcControl.ON:
            return "on"
        return "off"


class OperationMode(StrEnum):
    AUTO = "auto"
    DRY = "dry"
    HEAT = "heat"
    COOL = "cool"


class AirConditioner:
    """Class that represents a AirConditioner object in the HomeCom API."""

    def __init__(self, device_id: int, raw_data: dict, auth: AbstractAuth):
        """Initialize a air conditioner object."""
        self.device_id = device_id
        self.raw_data = raw_data
        self.auth = auth

    # Note: each property name maps the name in the returned data

    @property
    def id(self) -> int:
        """Return the ID of the AC."""
        return self.device_id

    @property
    def is_on(self) -> AcControl:
        """Return if the light is on."""
        return AcControl.from_str(self.raw_data["references"][1]["value"])

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
            json={"value": ac_control.to_str()},
        )
        print(await resp.text())
        resp.raise_for_status()
