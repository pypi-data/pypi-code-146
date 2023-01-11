""" """

import re
from abc import ABC, abstractmethod
import socket
import pathlib

import numpy as np


def get_regex_result(regex_string: str, search_string: str, group_name: str = None):
    """ """
    m = re.compile(regex_string).search(search_string)
    if m is not None:
        return m.group(group_name) if group_name is not None else m.group()
    return None


def get_regex_result_all(regex_string: str, search_string: str, group_name: str = None):
    """ """
    m = re.compile(regex_string).findall(search_string)
    return m


class SolverLogParser(ABC):
    """ base class for solver log parsing"""

    def __init__(self, log: str, instance: pathlib.Path = None):
        self.log = log
        self.is_LP = False
        self.is_MIP = False
        self.is_QUBO = False

        self.machine_name = socket.gethostname()
        self.instance = instance.name

    @abstractmethod
    def get_primal(self) -> float:
        """ """

    @abstractmethod
    def get_term_condition(self) -> str:
        """ """

    def get_status(self) -> str:
        return self.get_term_condition()

    def get_sol_status(self) -> str:
        """ """

    def get_relative_gap(self) -> float:
        """ """

    def get_hostname(self) -> str:
        """ get hostname for solver run """
        return self.machine_name

    @abstractmethod
    def get_timing(self):
        pass

    @abstractmethod
    def get_all(self):
        pass


class HybridMIPSolverParser(SolverLogParser):
    """   """
    def __init__(self, log: str, instance: pathlib.Path = None):
        super().__init__(log, instance)
        self.is_HybridMIP = True

    def get_term_condition(self) -> str:
        regex = r"Status (?P<status>.*)\n"
        # this is rather the term condition in our terminology
        # the actual solution status is given as 'Solution status' in the solver output
        term_condition = str(get_regex_result(regex, self.log, "status")).strip()
        return term_condition

    def get_primal_value(self):
        """ returns int or np.nan """
        regex = r"Primal value\s+ (?P<primal>.*)\n"
        primal = str(get_regex_result(regex, self.log, "primal")).strip()
        if (primal is None) or (primal == "None"):
            return np.nan
        elif primal == "inf" or primal == "Inf":
            return np.inf
        return float(primal)

    def get_primal(self):
        return self.get_primal_value()

    def get_bound(self):
        """ returns float or np.nan """
        regex = r"Dual bound\s+ (?P<dual_bound>.*)\n"
        dual_bound = str(get_regex_result(regex, self.log, "dual_bound")).strip()
        if (dual_bound is None) or (dual_bound == "None"):
            return np.nan
        return float(dual_bound)

    def get_relative_gap(self):
        """ returns float or np.nan """
        regex = r"Rel.Gap\s+ (?P<relative_gap>.*)\n"
        relative_gap = str(get_regex_result(regex, self.log, "relative_gap")).strip()
        if (relative_gap is None or
            relative_gap == "None"):
            return np.nan
        elif relative_gap == "inf" or relative_gap == "Inf":
            return np.inf

        relative_gap = relative_gap.split("%")[0]
        return float(relative_gap)

    def get_sol_status(self) -> str:
        regex = r"Solution status (?P<sol_status>.*)\n"
        sol_status = str(get_regex_result(regex, self.log, "sol_status")).strip()
        return sol_status

    def get_timing(self):
        """ returns float or np.nan """
        regex = r"Timing (?P<timing>.*) \(total\)\n"
        timing = str(get_regex_result(regex, self.log, "timing")).strip()
        if (timing is None) or (timing == "None"):
            return np.nan
        return float(timing)

    def get_nodes(self) -> int:
        """ returns int """
        regex = r"Nodes(?!\s*\|\s*Tree)(?P<nodes>.*)"
        nodes = get_regex_result_all(regex, self.log, "nodes")
        nodes = nodes[0].strip()
        return int(nodes)

    def get_iterations(self) -> int:
        regex = r"LP iterations (?P<iterations>.*)\n"
        iterations = str(get_regex_result(regex, self.log, "iterations")).strip()
        iterations = iterations.split(" ")[0]
        return int(iterations)

    def get_all(self):
        rdata = {}
        rdata["machine_name"] = self.get_hostname()
        rdata["instance"] = self.instance

        rdata["sol_status"] = self.get_sol_status()
        rdata["term_condition"] = self.get_term_condition()
        rdata["objective"] = self.get_primal_value()
        rdata["bound"] = self.get_bound()
        rdata["relative_gap"] = self.get_relative_gap()
        rdata["nodes"] = self.get_nodes()
        rdata["timing"] = self.get_timing()
        rdata["iterations"] = self.get_iterations()


        return rdata

class HybridQUBOSolverParser(SolverLogParser):
    """ class for QUBO solver parsing """

    def __init__(self, log: str, instance: pathlib.Path = None):
        super().__init__(log, instance)
        self.is_QUBO = True

    def get_sol_status(self) -> str:
        """ """
        regex = r"(?<=(solver\sresults))[\s\S]*\s-\ssolution_status:(?P<solution_status>.*)"
        sol_status = str(get_regex_result(regex, self.log, "solution_status")).strip()
        return sol_status

    def get_objective(self) -> float:
        """ """
        regex = r"(?<=(solver\sresults))[\s\S]*\s-\sobjective:(?P<objective>.*)"
        objective = str(get_regex_result(regex, self.log, "objective")).strip()
        return float(objective)

    def get_bound(self) -> float:
        """ """
        regex = r"(?<=(solver\sresults))[\s\S]*\s-\sbound:(?P<bound>.*)"
        bound = str(get_regex_result(regex, self.log, "bound")).strip()
        if (bound is None) or (bound == "None"):
            return np.nan
        return float(bound)

    def get_term_condition(self) -> str:
        """ """
        regex = r"(?<=(solver\sresults))[\s\S]*\s-\stermination_condition:(?P<termination_condition>.*)"
        term_condition = str(get_regex_result(regex, self.log, "termination_condition")).strip()
        # streamline with mip output
        term_condition = "optimal" if term_condition.lower() == "optimality" else term_condition
        return term_condition

    def get_best_node(self) -> str:
        """ """
        regex = r"(?<=(solver\sresults))[\s\S]*\s-\sbest_node:(?P<best_node>.*)"
        best_node = str(get_regex_result(regex, self.log, "best_node")).strip()
        return best_node

    def get_absolute_gap(self):
        regex = r"(?<=(solver\sresults))[\s\S]*\s-\sabsolute_gap:(?P<absolute_gap>.*)"
        absolute_gap = str(get_regex_result(regex, self.log, "absolute_gap")).strip()
        absolute_gap = absolute_gap.split()[0]
        if (absolute_gap is None) or (absolute_gap == "None"):
            return np.nan
        return float(absolute_gap)*100 # to have value in percent as it is for the MIP log

    def get_relative_gap(self):
        regex = r"(?<=(solver\sresults))[\s\S]*\s-\srelative_gap:(?P<relative_gap>.*)"

        relative_gap = str(get_regex_result(regex, self.log, "relative_gap")).strip()
        if (relative_gap is None) or (relative_gap == "None"):
            return np.nan
        return float(relative_gap)*100 # to have value in percent as it is for the MIP log

    def get_nodes(self) -> int:
        regex = r"(?<=(solver\sresults))[\s\S]*\s-\snodes:(?P<nodes>.*)"
        nodes = str(get_regex_result(regex, self.log, "nodes")).strip()
        if (nodes is None) or (nodes == "None"):
            return np.nan
        return int(nodes)

    def get_timing(self) -> str:
        regex = r"(?<=(solver\sresults))[\s\S]*\s-\swall_time:(?P<wall_time>.*)"
        timing = str(get_regex_result(regex, self.log, "wall_time")).strip()
        if (timing is None) or (timing == "None"):
            return np.nan
        return timing

    def get_primal(self):
        return self.get_objective()

    def get_all(self) -> dict:
        rdata = {}
        rdata["machine_name"] = self.get_hostname()
        rdata["instance"] = self.instance

        rdata["sol_status"] = self.get_sol_status()
        rdata["term_condition"] = self.get_term_condition()
        rdata["objective"] = self.get_objective()
        rdata["bound"] = self.get_bound()
        rdata["absolute_gap"] = self.get_absolute_gap()
        rdata["relative_gap"] = self.get_relative_gap()
        rdata["nodes"] = self.get_nodes()
        rdata["timing"] = self.get_timing()
        rdata["best_node"] = self.get_best_node()

        return rdata


class HybridParser(SolverLogParser):
    """ class for parsing output for infeasible solutions """

    def __init__(self, log: str, instance: pathlib.Path = None):
        super().__init__(log, instance)
        self.is_Hybrid = True

    def get_term_condition(self) -> str:
        """ """
        regex = r"Model   status\s*:(?P<status>.*)\n"
        term_condition = str(get_regex_result(regex, self.log, "status")).strip()
        return term_condition

    def get_objective(self) -> float:
        """ """
        regex = r"Objective value\s*:(?P<objective>.*)\n"
        objective = str(get_regex_result(regex, self.log, "objective")).strip()
        return float(objective)

    def get_iterations(self) -> float:
        """ """
        regex = r"Simplex\s*iterations\s*:(?P<iterations>.*)"
        iterations = str(get_regex_result(regex, self.log, "iterations")).strip()
        return float(iterations)

    def get_timing(self) -> str:
        regex = r"HybridSolver run time\s*:(?P<timing>.*)"
        timing = str(get_regex_result(regex, self.log, "timing")).strip()
        if (timing is None) or (timing == "None"):
            return np.nan
        return timing

    def get_primal(self):
        return self.get_objective()

    def get_all(self) -> dict:
        rdata = {}
        rdata["machine_name"] = self.get_hostname()
        rdata["instance"] = self.instance

        rdata["iterations"] = self.get_iterations()
        rdata["term_condition"] = self.get_term_condition()
        rdata["objective"] = self.get_objective()
        rdata["timing"] = self.get_timing()

        return rdata


class FailHandler(SolverLogParser):
    """  """

    def get_sol_status(self) -> str:
        """ """
        return "FAILED"

    def get_term_condition(self) -> str:
        """ """
        return "ERROR"

    def get_timing(self) -> str:
        return np.nan

    def get_primal(self):
        return self.get_objective()

    def get_all(self) -> dict:
        rdata = {}
        rdata["machine_name"] = self.get_hostname()
        rdata["instance"] = self.instance

        rdata["sol_status"] = self.get_sol_status()
        rdata["term_condition"] = self.get_term_condition()
        rdata["objective"] = np.nan
        rdata["bound"] = np.nan
        rdata["absolute_gap"] = np.nan
        rdata["relative_gap"] = np.nan
        rdata["nodes"] = np.nan
        rdata["timing"] = self.get_timing()
        rdata["best_node"] = np.nan
        return rdata
