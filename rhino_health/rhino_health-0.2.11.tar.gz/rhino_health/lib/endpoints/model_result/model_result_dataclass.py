import time
from enum import Enum
from typing import Any, List, Optional

import arrow
from funcy import flatten
from pydantic import Field
from typing_extensions import Annotated

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA


class ModelResultStatus(str, Enum):
    INITIALIZING = "Initializing"
    STARTED = "Started"
    COMPLETED = "Completed"
    FAILED = "Failed"


class ModelResult(RhinoBaseModel, extra=RESULT_DATACLASS_EXTRA):
    uid: str
    """The unique ID of the ModelResult"""
    action_type: str
    """The type of action preformed"""
    status: ModelResultStatus
    """The action status"""
    start_time: str
    """The action start time"""
    end_time: Any = None
    """The action end time"""
    _aimodel: Any = None
    _input_cohorts: Any = None
    _output_cohorts: Any = None
    input_cohort_uids: Optional[List[List[str]]]
    """
    A list of cohort uids. Each entry is a list of cohorts corresponding to a data_schema on the ai model
    [[first_cohort_for_first_run, second_cohort_for_first_run ...], [first_cohort_for_second_run, second_cohort_for_second_run ...], ...]
    """
    output_cohort_uids: Optional[List[List[str]]]
    """
    A list of cohort uids. Each entry is a list of of cohorts corresponding to a data_schema on the ai model
    [[first_cohort_for_first_run, second_cohort_for_first_run ...], [first_cohort_for_second_run, second_cohort_for_second_run ...], ...]
    """
    aimodel_uid: Annotated[dict, Field(alias="aimodel")]
    """The relevant aimodel object"""
    result_info: Optional[str]
    """The run result info"""
    results_report: Optional[str]
    """The run result report"""
    report_images: List[Any]
    """The run result images"""
    model_params_external_storage_path: Optional[str]
    """The external storage path"""

    @property
    def aimodel(self):
        """
        @autoapi True
        Return the AIModel associated with this ModelResult

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes

        Returns
        -------
        aimodel: AIModel
            DataClasses representing the AIModel
        """
        if self._aimodel:
            return self._aimodel
        if self.aimodel_uid:
            self._aimodel = self.session.aimodel.get_aimodel(self._aimodel)
            return self._aimodel
        else:
            return None

    @property
    def input_cohorts(self):
        """
        @autoapi True
        Return the Input Cohorts that were used for this modelresult

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes

        Returns
        -------
        cohorts: List[Cohort]
            DataClasses representing the Cohorts
        """
        if self._input_cohorts:
            return self._input_cohorts
        results = []
        for cohort_uid in list(flatten(self.input_cohort_uids)):
            results.append(self.session.cohort.get_cohort(cohort_uid))
        self._input_cohorts = results
        return results

    @property
    def output_cohorts(self):
        """
        @autoapi True
        Return the Output Cohorts that were used for this modelresult

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes

        Returns
        -------
        cohorts: List[Cohort]
            DataClasses representing the Cohorts
        """
        if self._output_cohorts:
            return self._output_cohorts
        results = []
        for cohort_uid in list(flatten(self.output_cohort_uids)):
            results.append(self.session.cohort.get_cohort(cohort_uid))
        self._output_cohorts = results
        return results

    def save_model_params(self, file_name):
        """
        Saves the model params to a file.

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        file_name: str
            Name of the file to save to
        """
        model_params = self.session.model_result.get_model_params()
        with open(file_name, "wb") as output_file:
            output_file.write(model_params.getbuffer())

    @property
    def _process_finished(self):
        """
        @autoapi False
        """
        return self.status in {ModelResultStatus.COMPLETED, ModelResultStatus.FAILED}

    def wait_for_completion(
        self, timeout_seconds: int = 500, poll_frequency: int = 10, print_progress: bool = True
    ):
        """
        @autoapi True
        Wait for the asynchronous AI Model Result to complete

        Parameters
        ----------
        timeout_seconds: int = 500
            How many seconds to wait before timing out
        poll_frequency: int = 10
            How frequent to check the status, in seconds
        print_progress: bool = True
            Whether to print how long has elapsed since the start of the wait

        Returns
        -------
        model_result: ModelResult
            DataClasses representing the ModelResult of the run

        See Also
        --------
        rhino_health.lib.endpoints.model_result.model_result_dataclass.ModelResult: Response object
        """
        if self._process_finished:
            return self
        start_time = arrow.utcnow()
        timeout_time = start_time.shift(seconds=timeout_seconds)
        while arrow.utcnow() < timeout_time:
            try:
                model_result = self.session.model_result.get_model_result(self.uid)
                new_status = model_result.status
                if new_status and new_status not in {
                    ModelResultStatus.STARTED,
                    ModelResultStatus.FAILED,
                }:
                    return model_result
            except Exception as e:
                raise Exception(f"Exception in wait_for_completion() calling get_status(): {e}")
            if print_progress:
                time_eclipsed = arrow.utcnow().humanize(
                    start_time, granularity=["hour", "minute", "second"], only_distance=True
                )
                print(f"Waiting for model result to complete ({time_eclipsed})")
            if poll_frequency:
                time.sleep(poll_frequency)
        raise Exception("Timeout waiting for model result to complete")
