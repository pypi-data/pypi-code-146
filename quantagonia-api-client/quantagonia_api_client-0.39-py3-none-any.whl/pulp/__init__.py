import pulp

from quantagonia.pulp.hybrid_solver_api import QQVM_CMD
from quantagonia.pulp.qpulp_adapter import QPuLPAdapter
from quantagonia.enums import HybridSolverConnectionType

# inject Quantagonia's solver into PuLP's list
if QQVM_CMD not in pulp.apis._all_solvers:
  pulp.apis._all_solvers.append(QQVM_CMD)