from dataclasses import dataclass
from os import PathLike
from typing import List
from typing import Optional
from typing import Union

import numpy as np
import numpy.typing as npt
from dataclasses_json import DataClassJsonMixin

AudioT = npt.NDArray[np.float32]
AudiosT = List[AudioT]

ListAudiosT = List[List[AudioT]]

Truth = npt.NDArray[np.float32]
Segsnr = npt.NDArray[np.float32]

AudioF = npt.NDArray[np.complex64]
AudiosF = List[AudioF]

Feature = npt.NDArray[np.float32]

Predict = npt.NDArray[np.float32]

Location = Union[str, bytes, PathLike]


class DataClassSonusAIMixin(DataClassJsonMixin):
    from typing import Dict
    from typing import Union

    # Json type defined to maintain compatibility with DataClassJsonMixin
    Json = Union[dict, list, str, int, float, bool, None]

    def __str__(self):
        return f'{self.to_dict()}'

    # Override DataClassJsonMixin to remove dictionary keys with values of None
    def to_dict(self, encode_json=False) -> Dict[str, Json]:
        def del_none(d):
            if isinstance(d, dict):
                for key, value in list(d.items()):
                    if value is None:
                        del d[key]
                    elif isinstance(value, dict):
                        del_none(value)
                    elif isinstance(value, list):
                        for item in value:
                            del_none(item)
            elif isinstance(d, list):
                for item in d:
                    del_none(item)
            return d

        return del_none(super().to_dict(encode_json))


@dataclass(frozen=True)
class TruthSetting(DataClassSonusAIMixin):
    config: Optional[dict] = None
    function: Optional[str] = None
    index: Optional[List[int]] = None


TruthSettings = List[TruthSetting]
OptionalNumberStr = Optional[Union[float, int, str]]
OptionalListNumberStr = Optional[List[Union[float, int, str]]]


@dataclass
class Augmentation(DataClassSonusAIMixin):
    normalize: OptionalNumberStr = None
    pitch: OptionalNumberStr = None
    tempo: OptionalNumberStr = None
    gain: OptionalNumberStr = None
    eq1: OptionalListNumberStr = None
    eq2: OptionalListNumberStr = None
    eq3: OptionalListNumberStr = None
    lpf: OptionalNumberStr = None
    ir: OptionalNumberStr = None
    count: Optional[int] = None
    mixup: Optional[int] = 1


Augmentations = List[Augmentation]


@dataclass(frozen=True)
class TargetFile(DataClassSonusAIMixin):
    duration: float
    name: Location
    truth_settings: TruthSettings
    augmentations: Optional[Augmentations] = None
    class_balancing_augmentation: Optional[Augmentation] = None


TargetFiles = List[TargetFile]


@dataclass
class AugmentedTarget(DataClassSonusAIMixin):
    target_augmentation_index: int
    target_file_index: int


AugmentedTargets = List[AugmentedTarget]


@dataclass(frozen=True)
class NoiseFile(DataClassSonusAIMixin):
    name: Location
    duration: float
    augmentations: Optional[Augmentations] = None


NoiseFiles = List[NoiseFile]
ClassCount = List[int]

GeneralizedIDs = Union[str, int, List[int], range]


@dataclass(frozen=True)
class TruthFunctionConfig(DataClassSonusAIMixin):
    feature: str
    mutex: bool
    num_classes: int
    target_gain: float
    config: Optional[dict] = None
    function: Optional[str] = None
    index: Optional[List[int]] = None


@dataclass
class GenMixData:
    targets: AudiosT = None
    noise: AudioT = None
    mixture: AudioT = None
    truth_t: Optional[Truth] = None
    segsnr_t: Optional[Segsnr] = None


@dataclass
class GenFTData:
    feature: Optional[Feature] = None
    truth_f: Optional[Truth] = None
    segsnr: Optional[Segsnr] = None


@dataclass(frozen=True)
class ImpulseResponseData:
    sample_rate: int
    offset: int
    filter: List[np.float32]


ImpulseResponseFiles = List[Location]
