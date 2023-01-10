import numpy as np
import os, sys
from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import yaml
from glob import glob
from importlib import import_module

class SimOptimizer(Problem):
    def __init__(self, config_file: str="config.yaml"):

        self.config_file = config_file
        self._read_config()
        self._init_from_config()
        self._init_paths()
        self._init_optimization_algorithm()

        sys.path.append(os.getcwd())

        # get model to optimization dir :
        self.get_model()

        sim = import_module("sim_setup")

        self.setup = sim.get_setup()

        # Define objective function as only function of x
        self.objective_fun = lambda x: sim.objective(self.setup["simulation"], x)

        super().__init__(
            n_var=self.setup["n_vars"],
            n_obj=self.setup["n_obj"],
            n_constr=0,
            xl=self.setup["ranges"][:, 0],
            xu=self.setup["ranges"][:, 1],
        )

    def _read_config(self):
        with open(self.config_file) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def _init_from_config(self):

        # Model setup :
        self.model_name = self.config["model_name"]

        # Optimization setup :
        self.opti_config = self.config["opti_config"]
        self.verbose = self.config["opti_config"]["verbose"]
        self.save_history = self.config["opti_config"]["save_history"]
        self.optimizer_id = self.config["optimizer"]
        self.seed = self.config["opti_config"]["seed"]
        self.experiment_name = self.config["experiment"]

        # General housekeeping :
        self.kept_files = self.config["kept_files"]

    def _init_paths(self):
        self.data_dump_root = "../data-dump/opti-runs/"
        self.experiment_dump = self.data_dump_root + self.experiment_name + ".npy"

    def _init_optimization_algorithm(self):
        if self.optimizer_id == "PSO":
            self.algorithm = PSO(pop_size=self.opti_config["pop_size"], adaptive=True)
        elif self.optimizer_id == "NSGAII":
            self.algorithm = NSGA2(pop_size=self.opti_config["pop_size"])

    def optimize(self):

        self.res = minimize(
            self,
            self.algorithm,
            ("n_gen", self.opti_config["n_gen"]),
            seed=self.seed,
            save_history=self.save_history,
            verbose=self.verbose,
        )

    def dump_result(self):

        if not os.path.exists(self.data_dump_root):
            os.mkdir(self.data_dump_root)

        F, X = self.res.opt.get("F", "X")

        n_evals = []  # corresponding number of function evaluations\
        hist_F = []  # the objective space values in each generation
        hist_cv = []  # constraint violation in each generation
        hist_cv_avg = []  # average constraint violation in the whole population

        for algo in self.res.history:

            # store the number of function evaluations
            n_evals.append(algo.evaluator.n_eval)

            # retrieve the optimum from the algorithm
            opt = algo.opt

            # store the least contraint violation and the average in each population
            hist_cv.append(opt.get("CV").min())
            hist_cv_avg.append(algo.pop.get("CV").mean())

            # filter out only the feasible and append and objective space values
            feas = np.where(opt.get("feasible"))[0]
            hist_F.append(opt.get("F")[feas])

        data = {
            "F": F,
            "X": X,
            "n_evals": n_evals,
            "hist_F": hist_F,
            "hist_cv": hist_cv,
            "hist_cv_avg": hist_cv_avg,
            "config": self.config,
        }

        np.save(self.experiment_dump, data, allow_pickle=True)

    def _evaluate(self, x: np.ndarray, out, *args, **kwargs):
        out["F"] = self.objective_fun(x)

    def get_model(self):
        command = f"cp -r ../models/{self.model_name}/* ./"
        self.run_command(command)

    def clean_setup(self):

        files = glob("./*")
        files = list(filter(lambda x: x not in self.kept_files, files))
        command = "rm -rf " + " ".join(files)

        self.run_command(command)

    @staticmethod
    def run_command(command: str):
        out = os.system(command)
        if out != 0:
            raise Exception("Problem running setup command")

def optimize(args: object) -> None:
    
    config_file = args.config_file

    print(f"\n  PyCFS : Running optimization with config : {config_file}. \n")

    optimizer = SimOptimizer(config_file)
    optimizer.optimize()
    optimizer.dump_result()
    optimizer.clean_setup()