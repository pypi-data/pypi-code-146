import unittest
import logging
from quantagonia.cloud.specs_https_client import SpecsHTTPSClient
from quantagonia.cloud.specs_enums import *
from quantagonia.enums import HybridSolverServers, HybridSolverConnectionType
from quantagonia.runner_factory import RunnerFactory
from quantagonia.spec_builder import QUBOSpecBuilder, MIPSpecBuilder
import json
from copy import deepcopy
from quantagonia.errors import SolverError
import ast
import os
import pandas as pd
from pathlib import Path
from .log_parser_factory import Factory
import asyncio
import time

input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example.qubo")
input_defective_qubo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "G10-defective.qubo")
input_defective_mips = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "garbage.mps")

BASE = os.path.abspath(os.path.dirname(__file__))


class TestErrorHandling(unittest.TestCase):

    def setUp(self):
        """
            These tests are created for local use and development of the API client.
            the API_KEY / API_KEY_2 and SERVER variables are passed as as env variables for security reasons.
            If hardcoded please alter before push.
            The tests are not being executed in Jenkins right now.
            Adding the variables and on a local pc they can be executed one by one for development and debugging of the
            quantagonia-api-client
        """
        API_KEY = os.getenv("QUANTAGONIA_API_KEY")
        API_KEY_2 = os.getenv("QUANTAGONIA_API_KEY_2")
        SERVER = os.getenv("SERVER")

        server = HybridSolverServers[SERVER]
        self.client = SpecsHTTPSClient(API_KEY, server)
        self.client_2 = SpecsHTTPSClient(API_KEY_2, server)
        self.runner = RunnerFactory.getRunner(HybridSolverConnectionType.CLOUD, API_KEY,
                                HybridSolverServers[SERVER], False)

    def test_submit_job(self):
        spec = QUBOSpecBuilder()
        job_id = self.client.submitJob([input_file_path], [spec.getd()])
        try:
            resp = self.client_2.checkJob(job_id)
        except RuntimeError as e:
            dict_error = ast.literal_eval(str(e))
            self.assertEqual(dict_error['httpStatus'], 403)
            self.assertEqual(dict_error['message'], 'Forbidden resource')

    def test_solver_error_des(self):
        """
            Checking the error parsing and passing as a SolverError error.
            The error is a Quantagonia specific error. The error has a message where we the json
            error response from the server is passed and can be retrieved with the "message" property of the error .
        """
        try:
            error = {'httpStatus': 500, 'message': 'Job finished with error', 'errorCode': 500, 'stactrace': None, 'contact': 'Contact quantagonia at <support@quantagonia.com>', 'details': 'Quantagonia HybridSolver.\nCopyright (c) 2022 Quantagonia GmbH.\nHybridSolver integrates various open-source packages; see release notes.\n\nSetting primal solver: FixingSupport<ThrowDiceSolver<0.9 NoSolver, 0.02 QUBO-Ising-Adapter<Metropolis-Hastings>, 0.08 FVSDP (primal)>>.\n\n*** ERROR ***\nUnable to read .qubo file  at line 11\nEXCEPTION: Unable to parse QUBO line: ix\n*** ERROR ***\n'}
            raise SolverError(error)
        except SolverError as e:
            self.assertEqual(e.message['httpStatus'], 500)

    def test_runtime_error(self):
        """
            Checking the error parsing and passing as a runtime error.
            The error is parsed into dick with ast library.
            The specific error is a python error and the message is passed in the python error.
        """
        try:
            error = {'httpStatus': 403, 'message': 'Forbiden resourse', 'errorCode': 0
                , 'stactrace': None, 'contact': 'Contact quantagonia at <support@quantagonia.com>', 'details': 'Your account cannot access the specific job'}
            raise RuntimeError(error)
        except RuntimeError as e:
            dict_error = ast.literal_eval(str(e))
            self.assertEqual(dict_error['httpStatus'], 403)

    def test_garbage_mips_file(self):
        """
            Test the cloud instalation with a garbage file for MIPS solver.
            It Should return a Quantagonia Solver error with http status 500. Since the solver cannot read the
            file. Probable change that into 400 since it is a bad request from the user.
            500 is due to unified error handling.

            The specific Job and MIPS does not return the correct log file and does not append the error.
        """
        spec = MIPSpecBuilder()
        try:
            self.runner.solve(problem_file=input_defective_mips, spec=spec.getd())
        except SolverError as e:
            self.assertEqual(e.message['httpStatus'], 500)

    def test_garbage_qubo_file(self):
        """
            Test the cloud instalation with a garbage file for QUBO solver.
            It Should return a Quantagonia Solver error with http status 500. Since the solver cannot read the
            file. Probable change that into 400 since it is a bad request from the user.
            500 is due to unified error handling.

            Parse the details and the log is present
        """
        spec = QUBOSpecBuilder()
        details = 'Quantagonia HybridSolver' \
                  '.\nCopyright (c) 2022 Quantagonia GmbH.' \
                  '\nHybridSolver integrates various open-source packages; see release notes.' \
                  '\n\nSetting primal solver: FixingSupport<ThrowDiceSolver<0.9 NoSolver' \
                  ', 0.02 QUBO-Ising-Adapter<Metropolis-Hastings>, 0.08 FVSDP (primal)>>.\n\n*** ERROR ***' \
                  '\nUnable to read .qubo file  at line 11\nEXCEPTION: Unable to parse QUBO line: ix\n*** ERROR ***\n'
        try:
            self.runner.solve(problem_file=input_defective_qubo, spec=spec.getd())
        except SolverError as e:
            self.assertIn("Unable to read .qubo file  at line 11", e.message['details'])
            self.assertEqual(e.message['httpStatus'], 500)

    def test_mip_solution_streaming(self):
        instances = [
            ["correctness_data", "iis-glass-cov.mps", "min"]
        ]

        instances_df = pd.DataFrame(
            instances, columns=["set", "instance", "sense"]
        )

        path_to_instances = BASE

        mip_spec = MIPSpecBuilder()
        mip_spec.set_option("mip_rel_gap", 0.4)

        base_specs = [
            mip_spec
        ]

        # callback function for recording results
        results = {}
        for tpl in instances:
            results[tpl[1]] = []

        def record_callback(batch_ix, objective, solution):
            results[instances[batch_ix][1]].append(float(objective))

        # submit batch, callback records all values
        res = self._submit_mip_batch(path_to_instances, instances_df,
            base_specs, 30, new_incumbent_callback=record_callback)

        for batch_ix in range(len(instances)):
            sense = instances[batch_ix][2]
            objs = results[instances[batch_ix][1]]

            # make sure that we get at least one solution
            self.assertGreater(len(objs), 0)

            # parse optimal value
            solver_log = res[batch_ix]["solver_log"]
            instance_path = Path(os.path.join(path_to_instances,
                instances[batch_ix][0], instances[batch_ix][1]))
            log_analyzer = Factory(solver_log, instance_path)
            opt = log_analyzer.get_primal()

            # solution values must be recorded in order, hence increase
            # in objective
            for ix in range(1, len(objs)):
                if sense == "max":
                    self.assertGreater(objs[ix], objs[ix - 1])
                if sense == "min":
                    self.assertLess(objs[ix], objs[ix - 1])

    def _submit_mip_batch(self, path, instances_df, base_specs, time_limit=3600, new_incumbent_callback=None):
        """
        Submit mip batch to return files and specs lists.
        Handling of specs is different, such that a dedicated MIP method is required. To be changed in the future.
        """

        instance_files = []
        specs = []
        for spec in base_specs:
            for _, row in instances_df.iterrows():
                instance_files.append(Path(os.path.join(path, row.set, row.instance)))
                spec.set_option("time_limit", time_limit)
                specs.append(spec.getd())

        # submit batch and wait for results
        res = self.runner.solveBatched(problem_files=instance_files, specs=specs, new_incumbent_callback=new_incumbent_callback)
        return res

    def async_test(coro):
        def wrapper(*args, **kwargs):
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(coro(*args, **kwargs))
            finally:
                loop.close()

        return wrapper

    def test_job_interruption(self):
        instances = [
            ['bqp', 'bqp100_0.qubo.gz', "feasible", 7970.0, 'max']
        ]
        instances_df = pd.DataFrame(
            instances, columns=["set", "instance", "expected_status", "known_optimal", "sense"])

        path_to_instances = os.path.join(BASE, "./data")

        base_specs = [
            QUBOSpecBuilder()
        ]

        instance_files = []
        specs = []
        sp = None
        time_limit = 1000
        for spec in base_specs:
            for _, row in instances_df.iterrows():
                instance_files.append(Path(os.path.join(path_to_instances, row.set, row.instance)))
                spec.set_time_limit(time_limit)
                spec_file = deepcopy(spec.getd())
                sp = spec
                specs.append(spec_file)

        job_id = self.client.submitJob(problem_files=instance_files, specs=[sp.getd()])
        for i in range(16):
            job = self.client.checkJob(job_id)
            results = self.client.getResults(job_id)
            solution = self.client.getCurrentSolution(job_id)
            objective_val = solution[0]['objective']
            task_status = solution[0]['status']

            if objective_val != 0.0 and task_status == 'Running':
                time.sleep(10)
                resp = self.client.interruptJob(job_id)
                solution = self.client.getCurrentSolution(job_id)
                job_status = solution[0]['status']
                self.assertEqual(JobStatus.terminated, job_status, msg="job id " + str(job_id))
                return
            time.sleep(10)
