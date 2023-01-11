import sys, os, os.path
from pulp.apis import LpSolver_CMD, subprocess, PulpSolverError, constants
from enum import Enum
import warnings

from quantagonia.runner import Runner
from quantagonia.spec_builder import MIPSpecBuilder

class QQVM_CMD(LpSolver_CMD):
    """The QQVM_CMD solver"""

    name = "QQVM_CMD"

    def __init__(
            self,
            runner : Runner,
            spec_dict : dict,
            keepFiles=False,
            obfuscate: bool = True
    ):
        """
        :param dict spec_dict: sets parameters and options for Bolt
        :param bool keepFiles: if True, files are saved in the current directory and not deleted after solving
        :param bool obfuscate: if True, constraints and variable names are obfuscated
        """
        self.runner = runner
        self.spec_dict = spec_dict
        if self.spec_dict is None:
            self.spec_dict = MIPSpecBuilder().getd()
        self.obfuscate = obfuscate
        LpSolver_CMD.__init__(
            self,
            mip=True,
            path="",
            keepFiles=keepFiles,
        )

    def defaultPath(self):
        return self.executableExtension("qqvm")

    def available(self):
        """True if the solver is available"""
        return self.executable(self.path)

    def actualSolve(self, lp):
        """Solve a well formulated lp problem"""
        varLP = False # When lp files are written, qqvm-bolt loses the ordering of variables. This results in wrong
        # reading of solutions as the assumed ordering is not present. In order to support varLP=True, one would have to
        # reimplement the readsol method.

        if varLP:
            tmpMps, tmpSol, tmpOptions, tmpLog = self.create_tmp_files(
                lp.name, "lp", "sol", "QQVM", "QQVM_log"
            )
        else:
            tmpMps, tmpSol, tmpOptions, tmpLog = self.create_tmp_files(
                lp.name, "mps", "sol", "QQVM", "QQVM_log"
            )

        if not varLP:
            if lp.sense == constants.LpMaximize:
                # we swap the objectives
                # because it does not handle maximization.

                warnings.warn(
                    "QQVM_CMD solving equivalent minimization form."
                )

                lp += -lp.objective

        lp.checkDuplicateVars()
        lp.checkLengthVars(52)

        # flag for renaming in writeMPS() should be {0,1}
        rename = 1
        if not self.obfuscate:
            rename = 0

        rename_map = {}

        if varLP:
            lp.writeLP(filename=tmpMps)  # , mpsSense=constants.LpMinimize)
        else:
            ret_tpl = lp.writeMPS(filename=tmpMps, rename = rename)  # , mpsSense=constants.LpMinimize)
            rename_map = ret_tpl[1]

        if lp.isMIP():
            if not self.mip:
                warnings.warn("QQVM_CMD cannot solve the relaxation of a problem")

        ########################################################################
        # actual solve operation (local or cloud)
        result = self.runner.solve(tmpMps, self.spec_dict)
        ########################################################################

        if not varLP:
            if lp.sense == constants.LpMaximize:
                lp += -lp.objective

        # parse solution
        content = result['solver_log'].splitlines()

        # LP
        model_line = [l for l in content if len(l.split()) > 2 and l.split()[:2] == ["Model", "status"]]
        if len(model_line) > 0:
            model_status = model_line[0].split()[3]  # Model status: ...
        else:
            # ILP
            model_line = [l for l in content if "Status" in l][0]
            model_status = model_line.split()[1]

        sol_line = [l for l in content if l[:2] == ["Solution", "status"]]
        sol_line = sol_line[0] if len(sol_line) > 0 else ["Not solved"]
        sol_status = sol_line[-1]
        if model_status.lower() == "optimal":  # optimal
            status, status_sol = (
                constants.LpStatusOptimal,
                constants.LpSolutionOptimal,
            )
        elif sol_status.lower() == "feasible":  # feasible
            # Following the PuLP convention
            status, status_sol = (
                constants.LpStatusOptimal,
                constants.LpSolutionIntegerFeasible,
            )
        elif model_status.lower() == "infeasible":  # infeasible
            status, status_sol = (
                constants.LpStatusInfeasible,
                constants.LpSolutionNoSolutionFound,
            )
        elif model_status.lower() == "unbounded":  # unbounded
            status, status_sol = (
                constants.LpStatusUnbounded,
                constants.LpSolutionNoSolutionFound,
            )

        if status == constants.LpStatusUndefined:
            raise PulpSolverError("Pulp: Error while executing", self.path)

        values = self.readsol(lp.variables(), result['solution_file'], rename_map)

        self.delete_tmp_files(tmpMps, tmpSol, tmpOptions, tmpLog)
        lp.assignStatus(status, status_sol)

        if status == constants.LpStatusOptimal:
            lp.assignVarsVals(values)

        return status

    @staticmethod
    def readsol(variables, solution_file, rename_keys = {}):
        """Read a QQVM solution file"""

        content = solution_file.splitlines()

        values = {}
        if not len(content):  # if file is empty, update the status_sol
            return None
        # extract everything between the line Columns and Rows
        col_id = [ix for ix in range(0, len(content)) if "Columns" in content[ix]][0]
        row_id = [ix for ix in range(0, len(content)) if "Row" in content[ix]][0]
        solution = content[col_id + 1 : row_id]

        for l in solution:
            var_name, var_val = l.split()
            values[var_name] = float(var_val)

        # adapt variabel names to obfuscated names
        if len(rename_keys) > 0:
            new_values = {}

            for k in rename_keys:
                new_values[k] = values[rename_keys[k]]

            return new_values

        return values
