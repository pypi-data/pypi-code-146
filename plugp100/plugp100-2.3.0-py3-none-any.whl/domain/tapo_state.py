import base64
import dataclasses
import semantic_version
from typing import Optional, Dict, Any

from plugp100.domain.energy_info import EnergyInfo


@dataclasses.dataclass
class TapoDeviceState:
    device_id: str = property(lambda self: self.state["device_id"])
    firmware_version: str = property(lambda self: self.state["fw_ver"])
    hardware_version: str = property(lambda self: self.state["hw_ver"])
    mac: str = property(lambda self: self.state["mac"])
    nickname: str = property(lambda self: base64.b64decode(self.state["nickname"]).decode("UTF-8"))
    model: str = property(lambda self: self.state["model"])
    type: str = property(lambda self: self.state["type"])
    device_on: bool = property(lambda self: self.state["device_on"])
    brightness: Optional[int] = property(lambda self: self.state["brightness"] if "brightness" in self.state else None)
    hue: Optional[int] = property(lambda self: self.state["hue"] if "hue" in self.state else None)
    saturation: Optional[int] = property(lambda self: self.state["saturation"] if "saturation" in self.state else None)
    color_temp: Optional[int] = property(lambda self: self.state["color_temp"] if "color_temp" in self.state else None)
    overheated: bool = property(lambda self: self.state["overheated"])
    signal_level: int = property(lambda self: self.state["signal_level"])
    rssi: int = property(lambda self: self.state["rssi"])
    energy_info: EnergyInfo = property(lambda self: self._energy_info)
    is_hardware_v2: bool = property(lambda self: self.firmware_version == "2.0")

    def __init__(self, state: Dict[str, Any], energy_info: Dict[str, any]):
        self.state = state
        self._energy_info = EnergyInfo(energy_info) if energy_info is not None else None

    def get_unmapped_state(self) -> Dict[str, Any]:
        return self.state

    def get_energy_unmapped_state(self) -> Dict[str, Any]:
        return self._energy_info.get_unmapped_state() if self.energy_info is not None else {}

    def get_semantic_firmware_version(self) -> semantic_version.Version:
        pieces = self.firmware_version.split("Build")
        try:
            if len(pieces) > 0:
                return semantic_version.Version(pieces[0].strip())
            else:
                return semantic_version.Version('0.0.0')
        except ValueError:
            return semantic_version.Version('0.0.0')
