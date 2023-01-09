#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

""":term:`MKID`-array detector modeling class."""

from typing import TYPE_CHECKING, Mapping, Optional

from pyxel.data_structure import Phase
from pyxel.detectors import Detector
from pyxel.util.memory import memory_usage_details

if TYPE_CHECKING:
    import pandas as pd

    from pyxel.detectors import Environment, MKIDCharacteristics, MKIDGeometry


class MKID(Detector):
    """:term:`MKID`-based detector class containing all detector attributes and data."""

    def __init__(
        self,
        geometry: "MKIDGeometry",
        environment: "Environment",
        characteristics: "MKIDCharacteristics",
    ):
        self._geometry: MKIDGeometry = geometry
        self._characteristics: MKIDCharacteristics = characteristics

        super().__init__(environment=environment)
        self.reset()

    def __eq__(self, other) -> bool:
        return (
            type(self) == type(other)
            and self.geometry == other.geometry
            and self.environment == other.environment
            and self.characteristics == other.characteristics
            and self._phase == other._phase
            and super().__eq__(other)
        )

    def reset(self) -> None:
        """TBW."""
        super().reset()
        self._phase = Phase(geo=self.geometry)

    def empty(self, empty_all: bool = True) -> None:
        """Empty the data in the detector.

        Returns
        -------
        None
        """
        super().empty(empty_all)

        if empty_all and self._phase:
            self.phase.array *= 0

    @property
    def geometry(self) -> "MKIDGeometry":
        """TBW."""
        return self._geometry

    @property
    def characteristics(self) -> "MKIDCharacteristics":
        """TBW."""
        return self._characteristics

    @property
    def phase(self) -> Phase:
        """TBW."""
        if not self._phase:
            raise RuntimeError("'phase' not initialized.")

        return self._phase

    def memory_usage(
        self, print_result: bool = True, human_readable: bool = True
    ) -> dict:
        """TBW.

        Returns
        -------
        dict
            Dictionary of attribute memory usage
        """
        attributes = [
            "_photon",
            "_charge",
            "_pixel",
            "_signal",
            "_image",
            "_phase",
            "material",
            "environment",
            "_geometry",
            "_characteristics",
        ]

        return memory_usage_details(
            self, attributes, print_result=print_result, human_readable=human_readable
        )

    # TODO: Refactor this
    def to_dict(self) -> Mapping:
        """Convert an instance of `MKID` to a `dict`."""
        dct = {
            "version": 1,
            "type": "MKID",
            "properties": {
                "geometry": self.geometry.to_dict(),
                "environment": self.environment.to_dict(),
                "characteristics": self.characteristics.to_dict(),
            },
            "data": {
                "photon": None if self._photon is None else self._photon.array.copy(),
                "scene": None if self._scene is None else self._scene.to_dict(),
                "pixel": None if self._pixel is None else self._pixel.array.copy(),
                "signal": None if self._signal is None else self._signal.array.copy(),
                "image": None if self._image is None else self._image.array.copy(),
                "phase": None if self._phase is None else self._phase.array.copy(),
                "processed_data": (
                    None
                    if self._processed_data is None
                    else self._processed_data.data.to_dict()
                ),
                "charge": (
                    None
                    if self._charge is None
                    else {
                        "array": self._charge.array.copy(),
                        "frame": self._charge.frame.copy(),
                    }
                ),
            },
        }

        return dct

    # TODO: Refactor this
    @classmethod
    def from_dict(cls, dct: Mapping) -> "MKID":
        """Create a new instance of `MKID` from a `dict`."""
        # TODO: This is a simplistic implementation. Improve this.
        import numpy as np
        import xarray as xr

        from pyxel.data_structure import Scene
        from pyxel.detectors import Environment, MKIDCharacteristics, MKIDGeometry

        if dct["type"] != "MKID":
            raise ValueError

        if dct["version"] != 1:
            raise ValueError

        properties = dct["properties"]
        geometry = MKIDGeometry.from_dict(properties["geometry"])
        environment = Environment.from_dict(properties["environment"])
        characteristics = MKIDCharacteristics.from_dict(properties["characteristics"])

        detector = cls(
            geometry=geometry,
            environment=environment,
            characteristics=characteristics,
        )

        data = dct["data"]

        if "photon" in data:
            detector.photon.array = np.asarray(data["photon"])

        scene: Optional[Mapping] = data.get("scene")
        if scene is not None:
            detector.scene = Scene.from_dict(scene)

        if "pixel" in data:
            detector.pixel.array = np.asarray(data["pixel"])
        if "signal" in data:
            detector.signal.array = np.asarray(data["signal"])
        if "image" in data:
            detector.image.array = np.asarray(data["image"])
        if "processed_data" in data:
            detector.processed_data._data = xr.Dataset.from_dict(data["processed_data"])
        if "charge" in data and data["charge"] is not None:
            charge_dct = data["charge"]
            detector.charge._array = np.asarray(charge_dct["array"])

            new_frame: pd.DataFrame = charge_dct["frame"]
            previous_frame: pd.DataFrame = detector.charge._frame
            detector.charge._frame = new_frame[previous_frame.columns]

        return detector
