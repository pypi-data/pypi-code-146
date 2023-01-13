from .hybrid_solver_api import QQVM_CMD

from quantagonia.runner import Runner
from quantagonia.runner_factory import HybridSolverConnectionType, RunnerFactory
from quantagonia.enums import HybridSolverServers

class QPuLPAdapter:

  @classmethod
  def getSolver(cls,
                connection : HybridSolverConnectionType,
                api_key : str = None,
                server : HybridSolverServers = HybridSolverServers.PROD,
                spec_dict : dict = None,
                keep_files : bool = False):
    runner : Runner = RunnerFactory.getRunner(connection, api_key, server)
    solver = QQVM_CMD(runner=runner, spec_dict=spec_dict, keepFiles=keep_files)

    return solver
