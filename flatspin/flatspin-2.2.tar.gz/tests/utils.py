from functools import partial
import pytest
import numpy.testing

# TODO: increase opencl precision?
approx = partial(pytest.approx, abs=1e-6)
assert_allclose = partial(numpy.testing.assert_allclose, atol=1e-6)
