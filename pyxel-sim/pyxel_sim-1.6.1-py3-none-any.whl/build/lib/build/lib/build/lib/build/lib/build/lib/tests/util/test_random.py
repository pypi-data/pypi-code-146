#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import numpy as np

from pyxel.util import set_random_seed


def test_set_random_seed_no_seed():
    """Test function 'set_random_seed' without a seed."""
    np.random.seed(123)
    exp_value1_seed123 = np.random.random()
    exp_value2_seed123 = np.random.random()
    exp_value3_seed123 = np.random.random()

    # Test before 'set_random_seed'
    np.random.seed(123)
    value = np.random.random()
    assert value == exp_value1_seed123

    # Test with 'set_random_seed'
    with set_random_seed(seed=None):
        value = np.random.random()
        assert value == exp_value2_seed123

    # Test after 'set_random_seed'
    value = np.random.random()
    assert value == exp_value3_seed123


def test_set_random_seed_with_seed456():
    """Test function 'set_random_seed' without a seed."""
    np.random.seed(123)
    exp_value1_seed123 = np.random.random()
    exp_value2_seed123 = np.random.random()

    # Test before 'set_random_seed'
    np.random.seed(456)
    exp_value1_seed456 = np.random.random()

    # Set first seed
    np.random.seed(123)
    value = np.random.random()
    assert value == exp_value1_seed123

    # Test with 'set_random_seed'
    with set_random_seed(seed=456):
        value = np.random.random()
        assert value == exp_value1_seed456

    # Test after 'set_random_seed'
    value = np.random.random()
    assert value == exp_value2_seed123


def test_set_random_seed_with_seed123():
    """Test function 'set_random_seed' without a seed."""
    np.random.seed(123)
    exp_value1_seed123 = np.random.random()
    exp_value2_seed123 = np.random.random()

    # Test before 'set_random_seed'
    np.random.seed(123)
    value = np.random.random()
    assert value == exp_value1_seed123

    # Test with 'set_random_seed'
    with set_random_seed(seed=123):
        value = np.random.random()
        assert value == exp_value1_seed123

    # Test after 'set_random_seed'
    value = np.random.random()
    assert value == exp_value2_seed123
