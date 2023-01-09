#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
"""Util functions to handle random seeds."""

from contextlib import contextmanager
from typing import Optional

import numpy as np


@contextmanager
def set_random_seed(seed: Optional[int] = None):
    """Set temporary seed the random generator.

    Examples
    --------
    import numpy as np

    with set_random_seed(seed=...):
        value = np.random.random()
    """
    if seed is not None:
        previous_state = np.random.get_state()
        try:
            np.random.seed(seed)
            yield
        finally:
            np.random.set_state(previous_state)
    else:
        # Do nothing
        yield
