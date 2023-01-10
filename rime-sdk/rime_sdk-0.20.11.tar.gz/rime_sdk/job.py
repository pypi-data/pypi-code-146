"""Library defining the interfaces for monitoring jobs in the RIME backend."""

import re
import time
from abc import ABC, abstractmethod
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional

import pandas as pd
from deprecated import deprecated

from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.swagger import swagger_client
from rime_sdk.swagger.swagger_client import ApiClient
from rime_sdk.swagger.swagger_client.models import (
    RimeJobMetadata,
    RimeJobStatus,
    RimeJobType,
    RimeJobView,
    RimeTestRunProgress,
    RimeTestTaskStatus,
)
from rime_sdk.swagger.swagger_client.rest import ApiException
from rime_sdk.test_run import TestRun

default_csv_header = ["test_name", "feature(s)", "status"]
cancellable_job_types = [
    RimeJobType.FIREWALL_BATCH_TEST,
    RimeJobType.MODEL_STRESS_TEST,
]
# Format datetimes in user-readable format
datetime_fields = ["creation_time", "start_time"]
# Removed if empty or overly verbose
fields_to_be_removed = ["job_data", "archived_job_logs"]


class BaseJob(ABC):
    """Abstract class for RIME Jobs.

    This object provides an interface for monitoring the status of a
    job in the RIME backend.
    """

    _job_type: str

    def __init__(self, api_client: ApiClient, job_id: str) -> None:
        """Create a new RIME Job.

        Args:
            api_client: ApiClient
                The client used to query about the status of the job.
            job_id: str
                The identifier for the RIME job that this object monitors.
        """
        self._api_client = api_client
        self._job_id = job_id

    def __repr__(self) -> str:
        """Return a string representation of this object."""
        return str(self)

    @property
    def job_id(self) -> str:
        """Return the id of the job."""
        return self._job_id

    @property
    def job_type(self) -> str:
        """Return the type of the job."""
        return self._job_type

    def __str__(self) -> str:
        """Pretty-print the object."""
        # Ping the backend for the status of the job and detailed info only for
        # succeeded jobs.
        status = self.get_status()
        ret = {
            "job_id": self._job_id,
            "job_type": self._job_type,
            "status": status.get("status"),
            "termination_reason": status.get("terminationReason"),
        }
        if status.get("status") == RimeJobStatus.SUCCEEDED:
            ret.update(self._get_test_run_dict())
        job_class = self.__class__.__name__
        return f"{job_class} {ret}"

    def __eq__(self, obj: Any) -> bool:
        """Check if this job is equivalent to 'obj'."""
        return isinstance(obj, BaseJob) and self._job_id == obj._job_id

    @staticmethod
    def _get_test_run_progress(test_run: RimeTestRunProgress) -> Optional[str]:
        test_batches = test_run.test_batches
        if len(test_batches) == 0:
            return None
        n = sum(batch.status == RimeTestTaskStatus.COMPLETED for batch in test_batches)
        return "{:<2} / {:>2} tests completed".format(n, len(test_batches))

    @abstractmethod
    def _get_progress(self, job: RimeJobMetadata) -> Optional[str]:
        """Pretty print the progress of the test run."""

    def get_status(
        self,
        verbose: bool = False,
        wait_until_finish: bool = False,
        poll_rate_sec: float = 5.0,
    ) -> Dict:
        """Query the ModelTest service for the job's status.

        This includes flags for blocking until the job is complete and printing
        information to ``stdout``. This method can help with monitoring the
        progress of stress test jobs, because it prints out helpful information
        such as running time and the progress of the test run.

        If the job has failed, the logs of the testing engine will be dumped
        to ``stdout`` to help with debuggability.

        Arguments:
            verbose: bool
                whether or not to print diagnostic information such as progress.
                Note that these logs have no strict form and will be subject to
                significant change in future versions.
            wait_until_finish: bool
                whether or not to block until the job has succeeded or failed.
                If `verbose` is enabled too, information about the job including
                running time and progress will be printed to ``stdout`` every
                ``poll_rate_sec``.
            poll_rate_sec: float
               the frequency with which to poll the job's status. Units are in seconds.

        Returns:
            A dictionary representing the job's state.

            .. code-block:: python

                {
                "id": str
                "type": str
                "status": str
                "start_time_secs": int64
                "running_time_secs": double
                }

        Example:

        .. code-block:: python

            # Block until this job is finished and dump monitoring info to stdout.
            job_status = job.get_status(verbose=True, wait_until_finish=True)
        """
        printed_cancellation_req = False
        # Create backend client stubs to use for the remainder of this session.
        api = swagger_client.JobReaderApi(self._api_client)
        with RESTErrorHandler():
            job: RimeJobMetadata = api.job_reader_get_job(
                job_id=self._job_id, view=RimeJobView.FULL
            ).job
        if verbose:
            print(
                "Job '{}' started at {}".format(
                    job.job_id, datetime.fromtimestamp(job.creation_time.timestamp()),
                )
            )

        # Do not repeat if the job is finished or blocking is disabled.
        while wait_until_finish and job.status not in (
            RimeJobStatus.SUCCEEDED,
            RimeJobStatus.FAILED,
            RimeJobStatus.CANCELLED,
        ):
            time.sleep(poll_rate_sec)
            with RESTErrorHandler():
                job = api.job_reader_get_job(
                    job_id=self._job_id, view=RimeJobView.FULL
                ).job
                progress = self._get_progress(job)
            if verbose:
                if (
                    not printed_cancellation_req
                    and verbose
                    and job.cancellation_requested
                ):
                    print("Cancellation Requested")
                    # Only print "Cancellation Requested" once.
                    printed_cancellation_req = True

                minute, second = divmod(job.running_time_secs, 60)
                hour, minute = divmod(minute, 60)
                progress_str = " ({})".format(progress) if progress else ""
                print(
                    "\rStatus: {}, Running Time: {:02}:{:02}:{:05.2f}{}".format(
                        job.status, int(hour), int(minute), second, progress_str
                    ),
                    end="",
                )

        # Only get the logs if the job has failed, as the
        # primary purpose is debuggability during development.
        model_testing_api = swagger_client.ModelTestingApi(self._api_client)
        if job.status == RimeJobStatus.FAILED:
            try:
                response = model_testing_api.model_testing_get_latest_logs(
                    job_id=self._job_id
                )
                if response.result.chunk:
                    print(
                        "\nLogs from failed job:\n"
                        + self._format_logs(response.result.chunk)
                    )
                else:
                    print("No logs found.")
            except ApiException as e:
                if e.status == HTTPStatus.NOT_FOUND:
                    print("Unable to retrieve logs for failed job.")
                else:
                    raise ValueError(e.reason) from None

        job_dict = job.to_dict()
        # Hide job data and archived logs in the return value because it can get ugly.
        for field in fields_to_be_removed:
            if field in job_dict:
                del job_dict[field]

        for field in datetime_fields:
            if field in job_dict and job_dict[field]:
                job_dict[field] = job_dict[field].strftime("%H:%M %B %d, %Y")

        return job_dict

    @staticmethod
    def _format_logs(logs_string: str) -> str:
        # Required to remove any warnings which contain endpoint information from logs.
        logs_without_warning = re.sub(r"^WARNING(.*?)recommended!\n$", "", logs_string)
        return logs_without_warning

    def _get_test_run_dict(self) -> dict:
        """Return a dictionary that is used to help pretty-print this object."""
        return {}

    def cancel(self) -> None:
        """Request that the job be cancelled in the backend.

        The backend will mark the job with "Cancellation Requested" and then clean
        up the job in the background.
        """
        if self.job_type not in cancellable_job_types:
            raise ValueError(
                (
                    f"Cancelling jobs is only supported for "
                    f"job types {cancellable_job_types}"
                )
            )
        api = swagger_client.JobReaderApi(self._api_client)
        with RESTErrorHandler():
            api.job_reader_cancel_job(job_id=self.job_id)

    def get_agent_id(self) -> str:
        """Get the agent ID which is running a successful job."""
        api = swagger_client.JobReaderApi(self._api_client)
        with RESTErrorHandler():
            job = api.job_reader_get_job(job_id=self._job_id).job
        return job.agent_id

    def get_job_debug_logs_link(self) -> str:
        """Get the archived logs (as a link) for failed job."""
        api = swagger_client.JobReaderApi(self._api_client)
        with RESTErrorHandler():
            job: RimeJobMetadata = api.job_reader_get_job(
                job_id=self._job_id, view=RimeJobView.FULL
            ).job
            if job.status != RimeJobStatus.FAILED:
                raise ValueError(
                    "debug logs are only available for "
                    "failed jobs, this job has status {}".format(job.status)
                )
            else:
                expiration_time = datetime.fromtimestamp(
                    job.archived_job_logs.expiration_time.timestamp()
                )
                if (
                    job.archived_job_logs.url.url != ""
                    and datetime.now() < expiration_time
                ):
                    return job.archived_job_logs.url.url
                else:
                    raise ValueError("debug logs are not available for this job")


class Job(BaseJob):
    """This object provides an interface for monitoring a Stress Test Job in the RIME backend."""

    _job_type = RimeJobType.MODEL_STRESS_TEST

    def _get_progress(self, job: RimeJobMetadata) -> Optional[str]:
        """Pretty print the progress of the test run."""
        if job.job_data.stress.progress is None:
            return None
        else:
            return self._get_test_run_progress(job.job_data.stress.progress.test_run)

    def get_test_run_id(self) -> str:
        """Get the test run ID for a successful job."""
        # This first step only prevents a rare case where the RIME engine has
        # signaled the test suite has completed but before the upload has completed.
        api = swagger_client.JobReaderApi(self._api_client)
        with RESTErrorHandler():
            job: RimeJobMetadata = api.job_reader_get_job(job_id=self._job_id).job
        if job.status != RimeJobStatus.SUCCEEDED:
            raise ValueError(
                "Job has status {}; it must have status {} to get results".format(
                    job.status, RimeJobStatus.SUCCEEDED
                )
            )
        return job.job_data.stress.test_run_id

    def get_test_run(self) -> TestRun:
        """Get the test run object.

        Raises:
            ValueError if the job does not have state 'SUCCEEDED.'
        """
        test_run_id = self.get_test_run_id()
        return TestRun(self._api_client, test_run_id)

    def _get_test_run_dict(self) -> dict:
        """Return a dictionary that is used to help pretty-print this object."""
        ret = {}
        test_run_obj = self.get_test_run()
        test_run_res = test_run_obj.get_result_df()
        for k, v in test_run_res.iloc[0].to_dict().items():
            # Omit metrics from the output dictionary.
            if not str(k).startswith("metrics"):
                ret[k] = v
        return ret

    @deprecated("Use TestRun.get_link()")
    def get_link(self) -> str:  # noqa: D401
        """Deprecated.

        Get the web app URL for a successful stress test job.

        This link directs to your organization's deployment of RIME.
        You can view more detailed information about the results of your stress test\
        in the web app, including helpful visualiziations, key insights, and\
        explanations of test results.

        Note: this is a string that should be copy-pasted into a browser.

        :meta private:
        """
        test_run = self.get_test_run()
        return test_run.get_link()

    @deprecated("Use TestRun.get_test_run_result()")
    def get_test_run_result(self) -> pd.DataFrame:  # noqa: D401
        """Deprecated.

        Retrieve high level summary information.
        This dataframe includes information such as model metrics on the reference and\
        evaluation datasets, overall RIME results such as severity across tests,\
        and high level metadata such as the project ID and model task.
        By concatenating these rows together, this allows you to build a table of test
        run results for sake of comparison. This only works on stress test jobs that
        have succeeded.
        Note: this does not work on <0.14.0 RIME test runs.

        Returns:
            A `pandas.DataFrame` object containing the test run result.
            There are a lot of columns, so it is worth viewing them with the `.columns`
            method to see what they are. Generally, these columns have information
            about the model and datasets as well as summary statistics like the number
            of failing test cases or number of high severity test cases.

        Example:
        .. code-block:: python
            # Wait until the job has finished, since this method only works on
            # succeeded jobs.
            job.get_status(verbose=True, wait_until_finish=True)
            # Dump the test cases in dataframe ``df``.
            # Print out the column names and types.
            print(df.columns)

        :meta private:
        """
        test_run_obj = self.get_test_run()
        return test_run_obj.get_result_df()

    @deprecated("Use TestRun.get_test_cases_result()")
    def get_test_cases_result(self) -> pd.DataFrame:  # noqa: D401
        """Deprecated.

        Retrieve all the test cases in a dataframe.
        This gives you the ability to perform granular queries on
        test cases. For example, if you only care about subset performance tests and
        want to see the results on each feature, you can fetch all the test cases in
        a dataframe, then query on that dataframe by test type. This only works on
        stress test jobs that have succeeded.
        Note: this will not work for test runs run on RIME versions <0.14.0.

        Returns:
            A ``pandas.DataFrame`` object containing the test case results.
            Here is a selected list of columns in the output:
            1. ``test_run_id``: ID of the parent test run.
            2. ``features``: List of features that the test case ran on.
            3. ``test_batch_type``: Type of test that was run (e.g. Subset AUC,\
                Must be Int, etc.).
            4. ``status``: Status of the test case (e.g. Pass, Fail, Skip, etc.).
            5. ``severity``: Metric that denotes the severity of the failure of\
                the test.

        Example:
        .. code-block:: python
            # Wait until the job has finished, since this method only works on
            # SUCCEEDED jobs.
            job.get_status(verbose=True, wait_until_finish=True)
            # Dump the test cases in dataframe ``df``.
            # Print out the column names and types.
            print(df.columns)

        :meta private:
        """
        test_run_obj = self.get_test_run()
        return test_run_obj.get_test_cases_df()


class ContinuousTestJob(BaseJob):
    """This object provides an interface for monitoring a Continuous Test Job in the RIME backend."""

    _job_type = RimeJobType.FIREWALL_BATCH_TEST

    def _get_progress(self, job: RimeJobMetadata) -> Optional[str]:
        """Pretty print the progress of the test run."""
        if job.job_data.continuous_inc.progress is None:
            return None
        test_runs = job.job_data.continuous_inc.progress.test_runs
        total_ct_runs = len(job.job_data.continuous_inc.ct_test_run_ids)
        if total_ct_runs == 0:
            return None
        finished_test_runs = len(
            [
                test_run
                for test_run in test_runs
                if test_run.test_run.status == RimeTestTaskStatus.COMPLETED
            ]
        )
        run_progress = "{:<2} / {:>2} time bins completed".format(
            finished_test_runs, total_ct_runs
        )
        for test_run in test_runs:
            if test_run.test_run.status != RimeTestTaskStatus.COMPLETED:
                batch_progress = self._get_test_run_progress(test_run.test_run)
                if batch_progress is not None:
                    return f"{run_progress}, {batch_progress}"
        return run_progress

    def _get_test_run_dict(self) -> dict:
        """Return a dictionary that is used to help pretty-print this object."""
        return {}


class ImageBuilderJob(BaseJob):
    """This object provides an interface for monitoring a Image Builder Job in the RIME backend."""

    _job_type = RimeJobType.IMAGE_BUILDER

    def _get_progress(self, job: RimeJobMetadata) -> Optional[str]:
        """Pretty print the progress of the test run."""
        # TODO: find a good way to pretty print the progress of a ImageBuilderJob
        return None


class FileScanJob(BaseJob):
    """This object provides an interface for monitoring a File Scan Job in the RIME backend."""

    _job_type = RimeJobType.FILE_SCAN

    def _get_progress(self, job: RimeJobMetadata) -> Optional[str]:
        """Pretty print the progress of the test run."""
        # TODO: find a good way to pretty print the progress of a FileScanJob
        return None
