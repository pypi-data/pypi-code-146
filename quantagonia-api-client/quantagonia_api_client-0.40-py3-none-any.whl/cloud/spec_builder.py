import os
import json
from enum import Enum
from abc import ABC
from typing import Dict

THIS_SCRIPT = os.path.dirname(os.path.abspath(__file__))

class ProblemType(Enum):
    MIP = 0
    QUBO = 1

class QuboSolverType(Enum):
  PRIMAL_COOK = 0
  PRIMAL_METROPOLIS_HASTINGS = 1
  PRIMAL_FVSDP = 2
  PRIMAL_THROW_DICE = 3

class SpecBuilder(ABC):
    def __init__(self):
        self.spec = {"solver_config" : {}}

    def gets(self) -> str:
        return json.dumps(self.spec)

    def getd(self) -> Dict:
        return self.spec

    def set_option(self, option: str, value) -> None:
        self.spec["solver_config"][option] = value

class MIPSpecBuilder(SpecBuilder):
    def __init__(self):
        super().__init__()
        self.spec["problem_type"] = "MIP"

    def set_write_style(self, style: int) -> None:
        self.set_option("write_solution_style", style)

class QUBOSpecBuilder(SpecBuilder):
    def __init__(self, type: QuboSolverType = QuboSolverType.PRIMAL_THROW_DICE):
        super().__init__()
        self.spec["problem_type"] = "QUBO"

        # load the default spec for the selected solver type
        if type == QuboSolverType.PRIMAL_COOK:
            spec = "cook_GPU.json"
        elif type == QuboSolverType.PRIMAL_METROPOLIS_HASTINGS:
            spec = "metropolis_CPU.json"
        elif type == QuboSolverType.PRIMAL_FVSDP:
            spec = "fvsdp.json"
        elif type == QuboSolverType.PRIMAL_THROW_DICE:
            spec = "throw_dice.json"
        else:
            raise RuntimeError("Unknown qubo solver type with enum value: " + str(type))

        with open(os.path.join(THIS_SCRIPT, "default_specs", spec)) as jsonf:
            self.spec["solver_config"] = json.load(jsonf)

    def set_time_limit(self, time_limit: float):
        self.set_option("time_limit", time_limit)

    def set_sense(self, sense: str):
        if sense != 'MINIMIZE' and sense != 'MAXIMIZE':
            raise ValueError('Unknown sense!')
        self.set_option("opt_sense", sense)
