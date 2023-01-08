from pararealml.boundary_condition import ConstantFluxBoundaryCondition
from pararealml.constrained_problem import ConstrainedProblem
from pararealml.differential_equation import BurgerEquation
from pararealml.initial_condition import MarginalBetaProductInitialCondition
from pararealml.initial_value_problem import InitialValueProblem
from pararealml.mesh import Mesh

diff_eq = BurgerEquation(2, re=10)
mesh = Mesh([(0.0, 1.0), (0.0, 1.0)], [0.05, 0.05])
bcs = [
    (
        ConstantFluxBoundaryCondition([0.0, 0.0]),
        ConstantFluxBoundaryCondition([0.0, 0.0]),
    ),
    (
        ConstantFluxBoundaryCondition([0.0, 0.0]),
        ConstantFluxBoundaryCondition([0.0, 0.0]),
    ),
]
cp = ConstrainedProblem(diff_eq, mesh, bcs)
t_interval = (0.0, 0.5)
ic = MarginalBetaProductInitialCondition(cp, [[(4, 8)] * 2, [(2, 6)] * 2])
ivp = InitialValueProblem(cp, t_interval, ic)
