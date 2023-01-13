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
    """This class is deprecated and to be removed soon."""
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
    def __init__(self, type = None):
        super().__init__()
        self.spec["problem_type"] = "QUBO"

        if type:
            warnings.warn("Setting a specific QuboSolverType is deprecated and ignored. Instead, a default spec is loaded. Please do all modifications via the dedicated methods of the SpecBuilder.")

        # always read default spec
        with open(os.path.join(THIS_SCRIPT, "default_spec.json")) as jsonf:
            self.spec["solver_config"] = json.load(jsonf)

    # general settings
    ###################################################################################
    def set_sense(self, sense: str):
        warnings.warn("Setting the sense via the spec is deprecated and ignored! " +\
                      "Set the sense in the .qubo file or via QuboModel.sense().")

    # termination settings
    ###################################################################################
    def set_max_num_nodes(self, max_num_nodes: int):
        """Limit number of branch-and-bound nodes."""
        if not max_num_nodes >= 1:
            raise ValueError(f"Parameter max_num_nodes must be >= 1")
        self.set_option("max_num_nodes", max_num_nodes)

    def root_node_only(self):
        """Only solve the root node"""
        self.set_max_num_nodes(1)

    def set_absolute_gap(self, abs_gap: float):
        """
        Set the absolute gap for termination.
        If the current absolute gap falls below this value, the solver terminates.
        """
        if not (isinstance(abs_gap, float) or isinstance(abs_gap, int)):
            raise ValueError("Value for absolute gap needs to be numeric.")
        self.set_option("absolute_gap", abs_gap)

    def set_relative_gap(self, rel_gap: float):
        """
        Set the relative gap for termination.
        If the current relative gap falls below this value, the solver terminates.
        """
        if not (isinstance(rel_gap, float) or isinstance(rel_gap, int)):
            raise ValueError("Value for relative gap needs to be numeric.")
        self.set_option("relative_gap", rel_gap)

    # presolve settings
    ###################################################################################
    def set_presolve(self, presolve: bool):
        if not isinstance(presolve, bool):
            raise ValueError(f"Value for presolve must be a bool.")
        self.spec["solver_config"]["presolve"]["enabled"] = presolve

    def set_coeff_strengthening(self, coeff_strengthening: str):
        if not isinstance(coeff_strengthening, bool):
            raise ValueError(f"Value for coeff strengthening must be a bool.")
        self.spec["solver_config"]["presolve"]["coeff_strengthening"] = coeff_strengthening
        if coeff_strengthening and not self.spec["solver_config"]["presolve"]["enabled"]:
            warnings.warn(
                "Setting parameter coeff_strengthening to True has no effect, because presolve is disabled. " +\
                "Enable presolve by using set_presolve(True).")

    def set_node_presolve(self, node_presolve: bool):
        if not isinstance(node_presolve, bool):
            raise ValueError(f"Value for node presolve must be a bool.")
        self.set_option("node_presolve", node_presolve)

    # search strategy settings
    ###################################################################################
    def set_enumeration(self, enumeration: bool):
        if not isinstance(enumeration, bool):
            raise ValueError(f"Value for enumeration must be a bool.")
        self.spec["solver_config"]["enumerate"]["enabled"] = enumeration
