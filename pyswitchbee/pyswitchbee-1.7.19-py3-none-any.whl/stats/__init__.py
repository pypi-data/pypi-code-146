from dataclasses import dataclass

@dataclass
class SwitchBeeDeviceStats:
    id: int
    name: str
    iconIndex: int
    zone: str
    type_: int
    unit_id: int
    rssi_ap: int
    rssi_eu: int
    temperature: int
    sesnor2: int
    sesnor3: int
    sesnor4: int
    value: int
    valueLow: int
