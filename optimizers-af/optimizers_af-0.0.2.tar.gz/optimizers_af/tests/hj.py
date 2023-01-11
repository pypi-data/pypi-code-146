import numpy as np

from optimizers_af.optimizers import HookeJeeves
from optimizers_af.test_functions import test_func_1, de_jong_1, rastrigin


FUNCTIONS = (test_func_1, de_jong_1, rastrigin)
INITIAL_POINTS = (
    np.array([3.10, 2.70, 4.20, 3.1, 4.1, .59]),
    np.array([3.10, 2.70, 4.20, 3.1, 4.1, .59]),
    np.array([3.10, 2.70, 4.20, 3.1, 4.1, .59]),
)

test_points_hj = []
for func, point in zip(FUNCTIONS, INITIAL_POINTS):
    HJ = HookeJeeves(
        func=func,
        accuracy=1e-7,
        initial_step_size=1.0,
        step_reduction_factor=0.5,
    )
    test_points_hj.append(HJ.run(point=point)[0])

for func, point in zip(FUNCTIONS, test_points_hj):
    print(f'HJ: Minimum of `{func.__name__}`: {str(point.round(2))}')
