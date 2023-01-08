import numpy as np

from pararealml import *


def ic_function(x: np.ndarray) -> np.ndarray:
    return np.cos((x[:, 0] - 2.) * np.pi / 4.).reshape((len(x), 1))


diff_eq = DiffusionEquation(2, 20.)
mesh = Mesh(
    [(2., 6.), (0., 2 * np.pi)],
    [.2, np.pi / 10.],
    CoordinateSystem.POLAR
)
bcs = [
    (
        ConstantValueBoundaryCondition([1.]),
        ConstantFluxBoundaryCondition([0.])
    ),
    (
        ConstantFluxBoundaryCondition([0.]),
        ConstantFluxBoundaryCondition([0.])
    )
]
cp = ConstrainedProblem(diff_eq, mesh, bcs)
t_interval = (0., 2.)
ic = ContinuousInitialCondition(cp, ic_function)
ivp = InitialValueProblem(cp, t_interval, ic)
