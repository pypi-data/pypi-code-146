import dataclasses
from dataclasses import dataclass
from typing import Optional


# TODO: improve this classes

@dataclass
class DeviceInfoParams:
    def as_dict(self):  # custom as_dict that remove None fields
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}


@dataclass
class SwitchParams(DeviceInfoParams):
    device_on: Optional[bool]


@dataclass
class LightEffectParams:
    enable: int
    name: Optional[str]
    brightness: Optional[int]
    display_colors: [[int]]


@dataclass
class LightParams(SwitchParams):
    brightness: Optional[int]
    color_temp: Optional[int]
    saturation: Optional[int]
    hue: Optional[int]
    lighting_effect: Optional[LightEffectParams]

    def __init__(self,
                 brightness: Optional[int] = None,
                 color_temperature: Optional[int] = None,
                 saturation: Optional[int] = None,
                 hue: Optional[int] = None,
                 effect: Optional[LightEffectParams] = None):
        self.device_on = None
        self.brightness = brightness
        self.color_temp = color_temperature
        self.saturation = saturation
        self.hue = hue
        self.lighting_effect = effect
        self.__enforce_effect_invariant()

    def __enforce_effect_invariant(self):
        is_single_prop_set = self.saturation is not None \
                             or self.brightness is not None \
                             or self.color_temp is not None \
                             or self.hue is not None
        if self.lighting_effect is not None:
            self.lighting_effect.enable = 0 if is_single_prop_set else 1
        else:
            self.lighting_effect = LightEffectParams(enable=0, name=None, brightness=None, display_colors=[])
