import pytest

from pyxel.detectors import CCD
from pyxel.models.charge_transfer.EMCCD_poisson import multiplication_register


def test_multiplication_register(ccd_10x10: CCD):
    detector = ccd_10x10

    multiplication_register(detector=detector, total_gain=0.0, gain_elements=1)


@pytest.mark.parametrize(
    "total_gain,gain_elements",
    [
        (-1, 10),
        (1, -1),
        (-1, -1),
    ],
)
def test_multiplication_register_bad_inputs(ccd_10x10: CCD, total_gain, gain_elements):
    detector = ccd_10x10

    with pytest.raises(ValueError, match="Wrong input parameter"):
        multiplication_register(
            detector=detector, total_gain=total_gain, gain_elements=gain_elements
        )
