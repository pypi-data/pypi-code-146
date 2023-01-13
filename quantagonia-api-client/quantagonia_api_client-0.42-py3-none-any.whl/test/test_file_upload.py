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
import numpy as np

input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example.qubo")
input_defective_qubo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "G10-defective.qubo")
input_defective_mips = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "garbage.mps")

BASE = os.path.abspath(os.path.dirname(__file__))


class TestFileUpload(unittest.TestCase):

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
        self.runner = RunnerFactory.getRunner(HybridSolverConnectionType.CLOUD, API_KEY,
                                HybridSolverServers[SERVER], False)

    def test_sos_instances(self):
        instances = [
            # mps files
            [os.path.join(BASE, "correctness_data"), 'sos/ftp_ns1943024.mps', 'optimal', 420.525917559, 'min'], # 64kb
            [os.path.join(BASE, "correctness_data"), 'sos/ftp_u30t24ramp.mps', 'optimal', 1693399.78213, 'min'],  #5.1mb
            [os.path.join(BASE, "correctness_data"), 'sos/ftp_u50t24wrongcost.mps', 'optimal', 2792696.47315, 'min'],#4.3mb
            [os.path.join(BASE, "correctness_data"), 'sos/miplib_30n20b8.mps', 'optimal', 1.56640764559, 'min'],  #2mb
            [os.path.join(BASE, "correctness_data"), 'sos/miplib_50v_10.mps', 'optimal', 2881.89485382, 'min'],  #303kb
            # [sos/'miplib_air05.lp', "optimal", 2.59070849954e+04],## takes too much time
            # [sos/'miplib_blp-ar98.mps', "optimal", 6.205835712e+03], ## takes too much time
            [os.path.join(BASE, "correctness_data"), 'sos/miplib_momentum1.mps', 'optimal', 73882.08581414, 'min'],#1.9mb
            [os.path.join(BASE, "correctness_data"), 'sos/miplib_wachplan.mps', 'optimal', -9.0, 'min'],#1.6mb
            # lp files
            [os.path.join(BASE, "correctness_data"), 'sos/ftp_bc.lp', 'optimal', 0.782836823575, 'min'],
            [os.path.join(BASE, "correctness_data"), 'sos/ftp_ns1943024.lp', 'optimal', 420.525917559, 'min'],#196kb
            [os.path.join(BASE, "correctness_data"), 'sos/ftp_u30t24ramp.lp', 'optimal', 1693399.78213, 'min'],#2.7mb
            [os.path.join(BASE, "correctness_data"), 'sos/ftp_u50t24wrongcost.lp', 'optimal', 2792696.47315, 'min'],  #4.3mb
            [os.path.join(BASE, "correctness_data"), 'sos/miplib_30n20b8.lp', 'optimal', 1.56640764559, 'min'],  # 2mb
            [os.path.join(BASE, "correctness_data"), 'sos/miplib_50v_10.lp', 'optimal', 2881.89485382, 'min'],  # 303kb
            # ['sos/miplib_air05.lp', "optimal", 2.59070849954e+04],## takes too much time
            # ['sos/miplib_blp-ar98.mps', "optimal", 6.205835712e+03], ## takes too much time
            [os.path.join(BASE, "correctness_data"), 'sos/miplib_momentum1.lp', 'optimal', 73882.08581414, 'min'],  # 1.9mb
            # [os.path.join(BASE, "correctness_data"), 'sos/miplib_wachplan.lp', 'optimal', -9.0, 'min'],#6mb
        ]
        instances_df = pd.DataFrame(
            instances, columns=["path", "instance", "expected_status", "known_optimal", "sense"])

        base_specs = [MIPSpecBuilder()]

        jobid = None
        def record_jobid_callback(_jobid):
            nonlocal jobid
            jobid = _jobid
        res = self._submit_mip_batch(instances_df, base_specs, submit_callback=record_jobid_callback)

        self._eval_batch(instances_df, len(base_specs), res, 1e-4, jobid=jobid)

    def _submit_mip_batch(self, instances_df, base_specs, time_limit=3600, new_incumbent_callback=None, submit_callback=None):
        """
        Submit mip batch to return files and specs lists.
        Handling of specs is different, such that a dedicated MIP method is required. To be changed in the future.
        """

        instance_files = []
        specs = []
        for spec in base_specs:
            for _, row in instances_df.iterrows():
                instance_files.append(Path(os.path.join(row.path, row.instance)))
                spec.set_option("time_limit", time_limit)
                specs.append(spec.getd())

        # submit batch and wait for results
        res = self.runner.solveBatched(problem_files=instance_files, \
            specs=specs, new_incumbent_callback=new_incumbent_callback, submit_callback=submit_callback)
        return res

    def _eval_batch(self, instances_df, num_base_specs, res, rel_tol=1e-6, jobid = None):
        """Evaluate qubo or mip batch and assert that no instances failed."""

        # evaluation per instance
        failed_instances = []
        log_msgs = {}
        for specs_count in range(num_base_specs):
            for instance_count, row in instances_df.iterrows():
                ix = instance_count + specs_count * instances_df.shape[0]
                solver_log = res[ix]["solver_log"]
                instance_path = Path(os.path.join(row.path, row.instance))
                log_analyzer = Factory(solver_log, instance_path)

                # check instance
                instance_failed = False
                msg = [str(instance_path), solver_log]

                # check status/term_condition
                # TODO: use enums for the status?
                status = log_analyzer.get_status().lower()
                if (row.expected_status in ["optimal", "unbounded", "infeasible"] and row.expected_status != status) or \
                        (row.expected_status == "feasible" and status not in ["time_limit", "optimal"]):
                    msg.append(f"TEST FAILED: Status does not match: {row.expected_status} vs. {status}")
                    instance_failed = True

                # if tested instance is optimal, check objective
                if status == "optimal":
                    primal = log_analyzer.get_primal()
                    if not np.isclose(row.known_optimal, primal, rtol=rel_tol):
                        msg.append(f"TEST FAILED: Optimal objectives do not match: {row.known_optimal}, {primal}")
                        instance_failed = True

                # if tested instance is feasible but not optimal, check bounds
                elif status == "feasible" or status == "timelimit (wall clock time)":
                    primal = log_analyzer.get_primal()
                    bound = log_analyzer.get_bound()

                    # get gaps according to sense
                    if row.sense == "max":
                        primal_gap = (row.known_optimal - primal) / abs(primal)
                        dual_gap = (bound - row.known_optimal) / abs(row.known_optimal)
                    else:
                        primal_gap = (primal - row.known_optimal) / abs(primal)
                        dual_gap = (row.known_optimal - bound) / abs(row.known_optimal)

                    if primal_gap < - rel_tol:
                        msg.append(f"TEST FAILED: Primal gap check failed: {primal_gap}")
                        instance_failed = True
                    if dual_gap < - rel_tol:
                        msg.append(f"TEST FAILED: Dual gap check failed: {dual_gap}")
                        instance_failed = True

                if instance_failed:
                    failed_instances.append(str(instance_path))
                log_msgs[str(instance_path)] = msg

        # finally assert against 0
        self.assertEqual(len(failed_instances), 0, msg = "job id " + str(jobid))

    def test_baseline_problem(self, primal_analytical=337):
        import tempfile
        import shutil

        from .qubo_utils.modeling import hamiltonian as hamiltonian
        from .qubo_utils.modeling import constraints as constraints
        from .qubo_utils.modeling import problem as problem
        # TODO: could be integrated in a batch
        # testing a simple problem

        e = np.array([1, 0, 1, 0, 1, 0])
        ham1 = constraints.constraint_partition(1, e)

        e = np.array([1, 1, 1, 1, 0, 0])
        ham2 = constraints.constraint_partition(1, e)

        e = np.array([1, 1, 1, 1, 0, 1])
        ham3 = constraints.constraint_partition(1, e)

        objVec = np.array([1, 1, 1, 1, 1, 1])
        obj = hamiltonian.Hamiltonian(0.0, np.diag(objVec))

        prob = problem.Problem()

        prob.addConstraint(10.0, ham1)
        prob.addConstraint(11.0, ham2)
        prob.addConstraint(12.0, ham3)
        prob.objective = (1.0, obj)

        tmpdir = tempfile.mkdtemp(prefix="qqvm-")

        instance_path = os.path.join(tmpdir, 'ham.qubo')
        prob.writeToFileFlat(instance_path)

        spec = QUBOSpecBuilder()
        spec.set_time_limit(5)
        jobid = None
        def record_jobid_callback(_jobid):
            nonlocal jobid
            jobid = _jobid
        res_dict = self.runner.solve(problem_file=instance_path, spec=spec.getd(),
            submit_callback=record_jobid_callback)

        shutil.rmtree(Path(tmpdir))
