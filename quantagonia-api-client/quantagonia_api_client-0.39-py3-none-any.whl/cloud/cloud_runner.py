from io import UnsupportedOperation
import sys, os
import asyncio
from time import sleep
from enum import Enum
from yaspin import yaspin
import uuid
from quantagonia.cloud.solver_log import SolverLog
from quantagonia.cloud.specs_https_client import SpecsHTTPSClient, JobStatus
from quantagonia.cloud.specs_enums import *
from quantagonia.runner import Runner
from quantagonia.enums import HybridSolverServers



class CloudRunner(Runner):
    def __init__(self, api_key: str, server: HybridSolverServers = HybridSolverServers.PROD, suppress_log : bool = False):
        self.https_client = SpecsHTTPSClient(api_key=api_key, target_server=server)
        self.suppress_log = suppress_log
        self._error_symbol = "❌"

    def _solveParseArgs(self, batch_size : int, **kwargs):

        # default values
        poll_frequency: float = 1
        timeout: float = 14400
        new_incumbent_callback = None
        submit_callback = None

        # parse args
        if "poll_frequency" in kwargs:
            poll_frequency = kwargs["poll_frequency"]
        if "poll_frequency" in kwargs:
            timeout = kwargs["timeout"]
        if "new_incumbent_callback" in kwargs:
            new_incumbent_callback = kwargs["new_incumbent_callback"]
        if "submit_callback" in kwargs:
            submit_callback = kwargs["submit_callback"]

        solver_logs = [SolverLog() for ix in range(0, batch_size)]

        return poll_frequency, timeout, solver_logs, new_incumbent_callback, submit_callback

    def waitForJob(self, jobid: uuid, poll_frequency: float, timeout: float, solver_logs: list, batch_size : int, new_incumbent_callback = None) -> JobStatus:

        printed_created = False
        printed_running = False
        spinner = yaspin()

        batch_num_incumbents = [0] * batch_size

        for t in range(0,int(timeout/poll_frequency)):

            sleep(poll_frequency)

            try:
                status = self.https_client.checkJob(jobid=jobid)
            except RuntimeError as runtime_e:
                sys.exit(f"{self._error_symbol} Unable to check job:\n\n{runtime_e}")

            if not self.suppress_log:
                try:
                    logs = self.https_client.getCurrentLog(jobid=jobid)
                except RuntimeError as runtime_e:
                    sys.exit(f"{self._error_symbol} Unable to get log:\n\n{runtime_e}")

                for ix in range(0, batch_size):
                    solver_logs[ix].updateLog(logs[ix])

            # note: we do not give an error status to the job, but rather do
            # this on the batch item level (as part of getResults)
            if status == JobStatus.finished:
                spinner.stop()
                return JobStatus.finished
            elif status == JobStatus.terminated:
                spinner.stop()
                return JobStatus.terminated
            elif status == JobStatus.error:
                spinner.stop()
                return JobStatus.error
            elif status == JobStatus.created:
                if not self.suppress_log:
                    if not printed_created:
                        printed_created = True
                        spinner.text = "Waiting for a free slot in the queue..."
                        spinner.start()
                        solver_logs[0].nextTimeAddNewLine()

            elif status == JobStatus.running:
                if not printed_running and not self.suppress_log:
                    printed_running = True
                    spinner.text = f"Job {jobid} unqueued, processing..."
                    spinner.ok("✔")

                    solver_logs[0].nextTimeAddNewLine()

                # check whether we got a new solution in any of the batch items
                if new_incumbent_callback is not None:
                    try:
                        batch_solutions = self.https_client.getCurrentSolution(jobid=jobid)
                    except RuntimeError as runtime_e:
                        sys.exit(f"{self._error_symbol}: " + str(runtime_e))

                    for ix in range(0, batch_size):
                        if int(batch_solutions[ix]["incumbents"]) > batch_num_incumbents[ix]:
                            new_incumbent_callback(ix, batch_solutions[ix]["objective"], batch_solutions[ix]["solution"])
                            batch_num_incumbents[ix] = int(batch_solutions[ix]["incumbents"])

        return JobStatus.timeout

    async def waitForJobAsync(self, jobid: uuid, poll_frequency: float, timeout: float, solver_logs: list, batch_size : int, new_incumbent_callback = None) -> JobStatus:

        printed_created = False
        printed_running = False
        spinner = yaspin(color="green")

        batch_num_incumbents = [0] * batch_size

        for t in range(0,int(timeout/poll_frequency)):

            await asyncio.sleep(poll_frequency)

            try:
                status = await self.https_client.checkJobAsync(jobid=jobid)
            except RuntimeError as runtime_e:
                sys.exit(f"{self._error_symbol}: " + str(runtime_e))
            if not self.suppress_log:
                try:
                    logs = await self.https_client.getCurrentLogAsync(jobid=jobid)
                except RuntimeError as runtime_e:
                    sys.exit(f"{self._error_symbol}: " + str(runtime_e))
                for ix in range(0, batch_size):
                    solver_logs[ix].updateLog(logs[ix])

            if status == JobStatus.finished:
                return JobStatus.finished
            elif status == JobStatus.terminated:
                return JobStatus.terminated
            elif status == JobStatus.error:
                return JobStatus.error
            elif status == JobStatus.created:
                if not self.suppress_log:
                    if not printed_created:
                        printed_created = True
                        spinner.text = "Waiting for a free slot in the queue..."
                        spinner.start()
                        solver_logs[0].nextTimeAddNewLine()

            elif status == JobStatus.running:
                if not printed_running and not self.suppress_log:
                    printed_running = True
                    spinner.text = f"Job {jobid} unqueued, processing..."
                    spinner.ok("✔")
                    solver_logs[0].nextTimeAddNewLine()

                # check whether we got a new solution in any of the batch items
                if new_incumbent_callback is not None:
                    try:
                        batch_solutions = await self.https_client.getCurrentSolutionAsync(jobid=jobid)
                    except RuntimeError as runtime_e:
                        sys.exit(f"{self._error_symbol}: " + str(runtime_e))

                    for ix in range(0, batch_size):
                        if int(batch_solutions[ix]["incumbents"]) > batch_num_incumbents[ix]:
                            new_incumbent_callback(ix, batch_solutions[ix]["objective"], batch_solutions[ix]["solution"])
                            batch_num_incumbents[ix] = int(batch_solutions[ix]["incumbents"])

        return JobStatus.timeout

    def solve(self, problem_file: str, spec: dict, **kwargs):

        res = self.solveBatched([problem_file], [spec], **kwargs)

        return res[0]

    ###
    # kwargs:
    # - submit_callback(jobid): called when job is submitted, receives jobid as parameter
    ###
    def solveBatched(self, problem_files: list, specs: list, **kwargs):

        batch_size = len(problem_files)
        poll_frequency, timeout, solver_logs, new_incumbent_callback, submit_callback = \
            self._solveParseArgs(batch_size, **kwargs)

        try:
            jobid = self.https_client.submitJob(problem_files=problem_files, specs=specs)
            if("submit_callback" in kwargs):
                kwargs["submit_callback"](jobid)
        except RuntimeError as runtime_e:
            sys.exit(f"{self._error_symbol}: " + str(runtime_e))

        if not self.suppress_log:
            print(f"Queued job with jobid: {jobid} for execution in the Quantagonia cloud...\n")

        status: JobStatus = self.waitForJob(jobid=jobid, poll_frequency=poll_frequency, timeout=timeout,
            solver_logs=solver_logs, batch_size=batch_size, new_incumbent_callback=new_incumbent_callback)

        if status is not JobStatus.finished:
            raise Exception(f"Job with jobid {jobid} error. Status of the job: {status}")
        else:
            if not self.suppress_log:
                print(f"Finished processing job {jobid}...")

        try:
            res = self.https_client.getResults(jobid=jobid)
        except RuntimeError as runtime_e:
            sys.exit(f"{self._error_symbol}: " + str(runtime_e))

        if not self.suppress_log:
            for ix in range(0, batch_size):
                solver_logs[ix].updateLog(res[ix]['solver_log'])

        return [{
            'solver_log': res[ix]['solver_log'],
            'solution_file': res[ix]['solution_file'],
            'status': res[ix]['status']
        } for ix in range(0, batch_size)]

    async def solveAsync(self, problem_file: str, spec: dict, **kwargs):

        res = await self.solveBatchedAsync([problem_file], [spec], **kwargs)

        return res[0]

    async def solveBatchedAsync(self, problem_files: list, specs: list, **kwargs):

        batch_size = len(problem_files)
        poll_frequency, timeout, solver_logs, new_incumbent_callback, submit_callback = \
            self._solveParseArgs(batch_size, **kwargs)

        try:
            jobid = await self.https_client.submitJobAsync(problem_files=problem_files, specs=specs)
        except RuntimeError as runtime_e:
            sys.exit(f"{self._error_symbol}: " + str(runtime_e))
        if not self.suppress_log:
            print(f"Queued job with jobid: {jobid} for execution in the Quantagonia cloud...\n")

        status: JobStatus = await self.waitForJobAsync(jobid=jobid, poll_frequency=poll_frequency, timeout=timeout,
            solver_logs=solver_logs, batch_size=batch_size, new_incumbent_callback=new_incumbent_callback)

        if status is not JobStatus.finished:
            raise Exception(f"Job with jobid {jobid} error. Status of the job: {status}")
        else:
            if not self.suppress_log:
                print(f"Finished processing job {jobid}...")

        try:
            res = self.https_client.getResults(jobid=jobid)
        except RuntimeError as runtime_e:
            sys.exit(f"{self._error_symbol}: " + str(runtime_e))
        if not self.suppress_log:
            for ix in range(0, batch_size):
                solver_logs[ix].updateLog(res[ix]['solver_log'])

        return [{
            'solver_log' : res[ix]['solver_log'],
            'solution_file' : res[ix]['solution_file'],
            'status: ': res[ix]['status']
        } for ix in range(0, batch_size)]

    def interrupt_job(self, jobid: uuid):
        resp = self.https_client.interrupt_job(jobid)
        return resp

    async def interrupt_job_async(self, jobid:uuid):
        resp = await self.https_client.interruptJobAsync(jobid)
        return resp
