import os
import json
from enum import Enum
from abc import ABC
from typing import Dict
import warnings

# set up warnings
def plain_warning(message, category, filename, lineno, line=None):
    return '%s: %s\n' % (category.__name__, message)

warnings.formatwarning = plain_warning


THIS_SCRIPT = os.path.dirname(os.path.abspath(__file__))

class ProblemType(Enum):
    MIP = 0
    QUBO = 1

class QuboSolverType(Enum):
  COOK = 0
  METROPOLIS_HASTINGS = 1
  FVSDP = 2
  THROW_DICE = 3
  THROW_DICE_SDP_ROOT = 4
  THROW_DICE_SDP_ALL = 5
  THROW_DICE_SDP_ALL_NEWTON = 6
  NO_SOLVER_SDP_ALL = 7

class SpecBuilder(ABC):
    def __init__(self):
        self.spec = {"solver_config" : {}}

    def gets(self) -> str:
        return json.dumps(self.spec)

    def getd(self) -> Dict:
        return self.spec

    def set_option(self, option: str, value) -> None:
        self.spec["solver_config"][option] = value

    def set_time_limit(self, time_limit: float):
        if not (isinstance(time_limit, float) or isinstance(time_limit, int)):
            raise ValueError(f"Time limit must be a float.")
        self.set_option("time_limit", time_limit)


class MIPSpecBuilder(SpecBuilder):
    def __init__(self):
        super().__init__()
        self.spec["problem_type"] = "MIP"

    def set_write_style(self, style: int) -> None:
        self.set_option("write_solution_style", style)

    def set_heuristics(self, heuristics: float):
        if heuristics < 0 or heuristics > 1:
            raise ValueError(f"Heuristics parameter must be in [0,1]")
        self.set_option("mip_heuristic_effort", heuristics)

class QUBOSpecBuilder(SpecBuilder):
    def __init__(self, type: QuboSolverType = QuboSolverType.THROW_DICE_SDP_ALL):
        super().__init__()
        self.spec["problem_type"] = "QUBO"

        # load the default spec for the selected solver type
        if type == QuboSolverType.COOK:
            spec = "cook_GPU.json"
        elif type == QuboSolverType.METROPOLIS_HASTINGS:
            spec = "metropolis_CPU.json"
        elif type == QuboSolverType.FVSDP:
            spec = "fvsdp.json"
        elif type == QuboSolverType.THROW_DICE:
            spec = "throw_dice.json"
        elif type == QuboSolverType.THROW_DICE_SDP_ROOT:
            spec = "throw_dice_sdp_root.json"
        elif type == QuboSolverType.THROW_DICE_SDP_ALL:
            spec = "throw_dice_sdp_all.json"
        elif type == QuboSolverType.THROW_DICE_SDP_ALL_NEWTON:
            spec = "throw_dice_sdp_all_newton.json"
        elif type == QuboSolverType.NO_SOLVER_SDP_ALL:
            spec = "no_solver_sdp_all.json"
        else:
            raise RuntimeError("Unknown qubo solver type with enum value: " + str(type))

        with open(os.path.join(THIS_SCRIPT, "default_specs", spec)) as jsonf:
            self.spec["solver_config"] = json.load(jsonf)

    def set_sense(self, sense: str):
        warnings.warn("Setting the sense via the spec is deprecated and ignored! " +\
                      "Set the sense in the .qubo file or via QuboModel.sense().")

    def set_presolve(self, presolve: bool):
        if not isinstance(presolve, bool):
            raise ValueError(f"Unknown value for presolve: {presolve}")
        self.spec["solver_config"]["presolve"]["enabled"] = presolve

    def set_coeff_strengthening(self, coeff_strengthening: str):
        if not isinstance(coeff_strengthening, bool):
            raise ValueError(f"Unknown value for coeff_strengthening: {coeff_strengthening}")
        self.spec["solver_config"]["presolve"]["coeff_strengthening"] = coeff_strengthening
        if coeff_strengthening and not self.spec["solver_config"]["presolve"]["enabled"]:
            warnings.warn(
                "Setting parameter coeff_strengthening to True has no effect, because presolve is disabled. " +\
                "Enable presolve by using set_presolve(True).")

    def set_max_num_nodes(self, max_num_nodes: int):
        """Limit number of branch-and-bound nodes."""
        if not max_num_nodes >= 1:
            raise ValueError(f"Parameter max_num_nodes must be >= 1")
        self.set_option("max_num_nodes", max_num_nodes)

    def root_node_only(self):
        """Only solve the root node"""
        self.set_max_num_nodes(1)
