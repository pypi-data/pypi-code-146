# Mypy; for the `|` operator purpose
# Remove this __future__ import once the oldest supported Python is 3.10
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .api import jobs
from .backend_connection import BackendConnection
from .estimate_result import EstimateResult
from .job_result import JobResult

if TYPE_CHECKING:
    import datetime
    from pathlib import Path

# TODO this requires imports of actual quantum libraries for proper type
# checking.
CircuitT = Any

logger = logging.getLogger("deqart-python-sdk")


class DeqartClient:
    def __init__(
        self, api_token: str | None = None, config_location: str | Path | None = None
    ):
        self._backend_connection = BackendConnection(api_token, config_location)

    def get(self, job_id: str) -> JobResult:
        """Get job current metadata and result

        :param job_id: job ID
        :type job_id: str

        :return: Result of job
        :rtype: JobResult
        """
        job_result = jobs.get(self._backend_connection, job_id)
        jr = JobResult(job_result)
        # logger.info(jr)
        return jr

    def search(
        self,
        run_status: str | None = None,
        created_later_than: str | datetime.datetime | None = None,
    ) -> list[JobResult]:
        """Search for jobs of the user

        :param run_status: if not None, run status of jobs to filter, can be one of "FAILED_VALIDATION" | "PENDING" | "QUEUED" | "RUNNING" | "TERMINATED" | "CANCELED" | "NOT_ENOUGH_FUNDS" | "COMPLETED"
        :type run_status: str

        :param created_later_than: if not None, filter by latest datetime. Please add timezone for clarity, otherwise UTC will be assumed
        :type created_later_than: str or datetime.datetime

        :return: Metadata of jobs
        :rtype: list of JobResult
        """
        job_results = jobs.search_jobs(
            self._backend_connection, run_status, created_later_than
        )
        return [JobResult(r) for r in job_results["data"]]

    def estimate(
        self,
        circuit: CircuitT,
    ) -> EstimateResult:
        """Estimate job runtime

        :param circuit: Quantum circuit
        :type circuit: Cirq, Qiskit, circuit
        :return: Estimate result class
        :rtype: EstimateResult
        """
        return EstimateResult(
            jobs.estimate_job_runtime(self._backend_connection, circuit)
        )

    def run(
        self,
        circuit: CircuitT,
        asynchronous: bool = False,
        job_name: str | None = None,
    ) -> JobResult:
        """Run job on Deqart Platform

        :param circuit: Quantum circuit
        :type circuit: Cirq, Qiskit, circuit
        :param asynchronous: if set to False, wait for job completion before returning. If set to True, return immediately
        :type asynchronous: bool
        :param job_name: customizable job name
        :type job_name: str
        :return: JobResult metadata
        :rtype: JobResult
        """
        submitted_job = JobResult(
            jobs.submit_job(self._backend_connection, circuit, job_name)
        )
        if submitted_job.run_status == "FAILED_VALIDATION":
            logger.error(submitted_job)
        else:
            logger.info(f"Submitted {submitted_job}")
            if not asynchronous:
                return self.wait(submitted_job.job_id)
        return submitted_job

    def wait(self, job_id: str) -> JobResult:
        """Wait for job completion

        :param job_id: job_id that can be found as property of JobResult metadata
        :type job_id: str
        :return: JobResult metadata
        :rtype: JobResult
        """
        return JobResult(jobs.wait_for_job(self._backend_connection, job_id))

    def cancel(
        self,
        job_id: str,
        asynchronous: bool = False,
    ) -> JobResult:
        """Cancel job

        :param job_id: job_id that can be found as property of JobResult metadata
        :type job_id: str
        :param asynchronous: if set to False, wait for job completion before returning. If set to True, return immediately
        :type asynchronous: bool
        :return: JobResult metadata
        :rtype: JobResult
        """
        jobs.cancel_job(self._backend_connection, job_id)
        if not asynchronous:
            return self.wait(job_id)
        else:
            return JobResult({"job_id": job_id})
