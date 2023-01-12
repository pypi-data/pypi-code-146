from tomwer.core.process.reconstruction.utils.cor import (
    relative_pos_to_absolute,
    absolute_pos_to_relative,
)
import numpy


def test_cor_conversion():
    """
    test absolute_pos_to_relative and relative_pos_to_absolute functions
    """
    assert relative_pos_to_absolute(relative_pos=0.0, det_width=100) == 49.5
    assert relative_pos_to_absolute(relative_pos=0.0, det_width=101) == 50.0

    assert absolute_pos_to_relative(absolute_pos=20, det_width=500) == -229.5
    assert absolute_pos_to_relative(absolute_pos=300, det_width=500) == 50.5

    for det_width in (10, 20, 30, 50):
        for relative_cor_pos in (0, -2.3, -4.5):
            numpy.testing.assert_almost_equal(
                relative_cor_pos,
                absolute_pos_to_relative(
                    absolute_pos=relative_pos_to_absolute(
                        relative_pos=relative_cor_pos, det_width=det_width
                    ),
                    det_width=det_width,
                ),
            )
