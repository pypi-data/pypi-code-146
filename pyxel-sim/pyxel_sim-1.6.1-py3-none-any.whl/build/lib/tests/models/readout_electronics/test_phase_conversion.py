#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
import pytest

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Environment
from pyxel.models.readout_electronics import simple_phase_conversion


def test_simple_phase_conversion_with_ccd():
    """Test model 'dead_time_filter' with a `CCD` detector."""
    detector = CCD(
        geometry=CCDGeometry(
            row=5,
            col=4,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(),
    )

    with pytest.raises(TypeError, match="Expecting a MKID object for the detector."):
        simple_phase_conversion(detector=detector)
