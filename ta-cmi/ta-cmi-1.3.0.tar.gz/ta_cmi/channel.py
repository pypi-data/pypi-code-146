from typing import Any, Dict

from .const import (
    UNITS_DE,
    UNITS_EN,
    ChannelMode,
    ChannelType,
    Languages,
    ReadOnlyClass,
)


class Channel(metaclass=ReadOnlyClass):
    """Class to display an input or output."""

    def __init__(self, mode: ChannelType, json: Dict[str, Any]) -> None:
        """Initialize and parse json to get properties."""
        self.mode: ChannelType = mode
        self.type: ChannelMode = json["AD"]
        self.index: int = json["Number"]
        self.value: float = json["Value"]["Value"]
        self.unit: str = json["Value"]["Unit"]

    def get_unit(self, language: Languages = Languages.EN) -> str:
        """Get the unit of the channel."""
        if language == Languages.EN:
            return UNITS_EN.get(self.unit, "Unknown")
        else:
            return UNITS_DE.get(self.unit, "Unknown")

    def __eq__(self, other) -> bool:
        return (
            self.mode == other.mode
            and self.type == other.type
            and self.index == other.index
            and self.value == other.value
            and self.unit == other.unit
        )

    def __repr__(self) -> str:
        return f"Channel {self.index}: Type: {self.type}, Mode: {self.mode}, Value: {self.value} {self.get_unit()}"
