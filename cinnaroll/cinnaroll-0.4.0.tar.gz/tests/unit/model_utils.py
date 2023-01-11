import numpy as np
import numpy.typing as npt
from typing import Tuple


def generate_random_data(
    num_samples: int, num_features: int
) -> Tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Generate random data of specified dimension. Returns numpy.arrays."""
    X = np.random.rand(num_samples, num_features)
    Y = np.random.rand(num_samples)

    return X, Y
