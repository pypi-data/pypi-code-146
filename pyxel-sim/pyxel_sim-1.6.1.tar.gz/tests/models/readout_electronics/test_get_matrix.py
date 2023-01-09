#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import numpy as np

from pyxel.models.readout_electronics.amplifier_crosstalk import get_matrix


def test_get_matrix_with_list():
    """Test function 'get_matrix'."""
    matrix = [[1, 0.5], [0.5, 1], [0, 0]]
    data = get_matrix(matrix)

    exp_matrix = np.array([[1, 0.5], [0.5, 1], [0, 0]])
    np.testing.assert_equal(data, exp_matrix)
