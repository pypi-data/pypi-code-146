import dataclasses
from dataclasses import dataclass
from typing import Optional, List


# TODO: improve this classes

@dataclass
class DeviceInfoParams:
    def as_dict(self):  # custom as_dict that remove None fields
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}


@dataclass
class SwitchParams(DeviceInfoParams):
    device_on: Optional[bool]


@dataclasses.dataclass
class LightEffectData:
    id: str
    name: str
    brightness: int
    display_colors: List[List[int]]
    enable: int
    bAdjusted: Optional[int] = None
    brightness_range: List[int] = dataclasses.field(default_factory=list)
    backgrounds: List[List[int]] = dataclasses.field(default_factory=list)
    custom: Optional[int] = None
    direction: Optional[int] = None
    duration: Optional[int] = None
    expansion_strategy: Optional[int] = None
    fadeoff: Optional[int] = None
    hue_range: Optional[List[int]] = None
    init_states: List[List[int]] = dataclasses.field(default_factory=list)
    random_seed: Optional[int] = None
    repeat_times: Optional[int] = None
    saturation_range: Optional[List[int]] = None
    segment_length: Optional[int] = None
    segments: Optional[List[int]] = None
    sequence: Optional[List[List[int]]] = None
    spread: Optional[int] = None
    transition: Optional[int] = None
    transition_range: Optional[List[int]] = None
    type: Optional[str] = None
    trans_sequence: Optional[List[int]] = None
    run_time: Optional[int] = None

    def as_dict(self):  # custom as_dict that remove None fields
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}


@dataclasses.dataclass
class LightParams(SwitchParams):
    brightness: Optional[int]
    color_temp: Optional[int]
    saturation: Optional[int]
    hue: Optional[int]
    lighting_effect: Optional[LightEffectData]

    def __init__(self,
                 brightness: Optional[int] = None,
                 color_temperature: Optional[int] = None,
                 saturation: Optional[int] = None,
                 hue: Optional[int] = None,
                 effect: Optional[LightEffectData] = None):
        self.device_on = True
        self.brightness = brightness
        self.color_temp = color_temperature
        self.saturation = saturation
        self.hue = hue
        self.lighting_effect = effect
    #
    # def __enforce_effect_invariant(self):
    #     is_single_prop_set = self.saturation is not None \
    #                          or self.brightness is not None \
    #                          or self.color_temp is not None \
    #                          or self.hue is not None
    #     if self.lighting_effect is not None:
    #         self.lighting_effect.enable = 0 if is_single_prop_set else 1
    #     else:
    #         self.lighting_effect = LightEffectData(enable=0, name=None, brightness=None, display_colors=[])
