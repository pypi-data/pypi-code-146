"""
This module contains the implementations of the Job concept from a
Gateway configuration.
"""
# ====================== Imports ===============================
from dataclasses import dataclass
import dataclasses
from txp.common.configuration import SamplingWindow
from typing import List, Dict, Union
import datetime
from txp.common.config import settings


# ==============================================================================
# SamplingParameters class
# ==============================================================================
@dataclass
class SamplingParameters:
    """This class encapsulates the sampling parameters that can be assigned to a
    Job or a Job Task

    Note on the args `predicates`: Imagine that we want to cover cases where the sampling
        of a machine depends on something else that is also being monitored. A predicate
        represents a dependency of this kind, with functions that returns a boolean and has
        an ID.

    Args:
        sampling_window: The Sampling Window defined as parameter.

        start_date: Start Date of the Job/Job Task in isoformat YYYY-MM-DD

        end_date: End date of the Job/Job Task in isoformat YYYY-MM-DD. After this date is reached,
            the Job/Job Task will not be executed anymore.

        active_week_days: a week days mask from Sunday to Saturday.
            Example of a mask active from monday to friday: '0111110'

        start_time: Start time of the Job/Job Task within a 24 hrs range, in isoformat HH:MM.

        end_time: Explicit end time of the Job/Job Task within a 24 hrs range, in isoformt HH:MM.

        predicates: A List of predicate names, on which the sampling depends on. For example: 'power_on'.

        samplings: A positive number to indicate how many sampling windows the Driver should execute.
            TODO: This samplings arg should be deleted. Is only provided given the current Driver implementation.
    """
    sampling_window: SamplingWindow
    start_date: datetime.date
    end_date: datetime.date
    active_week_days: str
    start_time: datetime.time
    end_time: datetime.time
    predicates: List[str]

    def __post_init__(self):
        self._week_days_mask: List[int] = list(
            map(lambda char: int(char), self.active_week_days)
        )

    @property
    def week_days_mask(self) -> List[int]:
        """Returns the mask of active week days"""
        return self._week_days_mask

    @classmethod
    def build_from_dict(cls, d: Dict) -> Union["SamplingParameters", None]:
        if not cls._validate_dict(d):
            return None

        sampling_window = SamplingWindow(d['sampling_window']['observation_time'], d['sampling_window']['sampling_time'])
        start_date = datetime.datetime.strptime(d['start_date'], settings.time.date_format)
        end_date = datetime.datetime.strptime(d['end_date'], settings.time.date_format)
        start_time = datetime.datetime.strptime(d['start_time'], settings.time.time_format)
        end_time = datetime.datetime.strptime(d['end_time'], settings.time.time_format)

        return cls(
            sampling_window, start_date.date(), end_date.date(), d['active_week_days'], start_time.time(), end_time.time(),
            d['predicates']
        )

    @classmethod
    def _validate_dict(cls, d: Dict) -> bool:
        known_fields = list(map(
            lambda field: field.name in d,
            dataclasses.fields(cls)
        ))

        return all(known_fields)

    def reprJSON(self) -> Dict:
        """Returns a Dict easily serializable to JSON.

        The Dictionary will contain the values required to re-create the instance from the JSON
        object in a pythonic way:
            object = MyObject( **json.loads(json_string) )
        """
        return dict(
            sampling_window=self.sampling_window,
            start_date=self.start_date.strftime(settings.time.date_format),
            end_date=self.end_date.strftime(settings.time.date_format),
            active_week_days=self.active_week_days,
            start_time=self.start_time.strftime(settings.time.time_format),
            end_time=self.end_time.strftime(settings.time.time_format),
            predicates=self.predicates
        )


# ==============================================================================
# JobTask class
# ==============================================================================
@dataclass
class JobTask:
    """The encapsulation of a Job Task that is defined inside a Gateway Job.

    Args:
        machines (List[str]): The List of Machines to collect data from during the task.
        parameters (SamplingParameters): The configured parameters for the Job Task.
    """
    machines: List[str]
    parameters: SamplingParameters

    @classmethod
    def build_from_dict(cls, d: Dict) -> Union["JobTask", None]:
        if not cls._validate_dict(d):
            return None

        sampling_parameters = SamplingParameters.build_from_dict(d['parameters'])
        if not sampling_parameters:
            return None

        return cls(d['machines'], sampling_parameters)

    @classmethod
    def _validate_dict(cls, d: Dict) -> bool:
        known_fields = list(map(
            lambda field: field.name in d,
            dataclasses.fields(cls)
        ))

        return all(known_fields)

    def reprJSON(self) -> Dict:
        """Returns a Dict easily serializable to JSON.

        The Dictionary will contain the values required to re-create the instance from the JSON
        object in a pythonic way:
            object = MyObject( **json.loads(json_string) )
        """
        return dict(
            machines=self.machines,
            parameters=self.parameters.reprJSON()
        )


# ==============================================================================
# JobConfig class
# ==============================================================================
@dataclass
class JobConfig:
    """The encapsulation of a Job assigned to the Gateway.

    A Job will define all the sampling operations of the Gateway and the Telemetry dispatch
    operation associated to the monitoring process.

    Args:
        parameters (SamplingParameters): The configured parameters for the job.

        telemetry_rollover_policy (str): The selected policy for the Telemetry dispatching to follow
            when no all packages produced during an sampling window were sent in that window.

        Tasks (List[JobTask]): The List of Job Tasks configured for the monitoring.
    """
    parameters: SamplingParameters
    telemetry_rollover_policy: str
    tasks: List[JobTask]

    @classmethod
    def build_from_dict(cls, d: Dict) -> Union["JobConfig", None]:
        if not cls._validate_dict(d):
            return None

        job_params = SamplingParameters.build_from_dict(d['parameters'])

        if not job_params:
            return None

        tasks = list(map(
            lambda task_dict: JobTask.build_from_dict(task_dict),
            d['tasks']
        ))

        if any(map(
            lambda t: t is None, tasks
        )):
            return None

        return cls(job_params, d['telemetry_rollover_policy'], tasks)

    @classmethod
    def _validate_dict(cls, d: Dict) -> bool:
        known_fields = list(map(
            lambda field: field.name in d,
            dataclasses.fields(cls)
        ))

        return all(known_fields)

    def reprJSON(self) -> Dict:
        """Returns a Dict easily serializable to JSON.

        The Dictionary will contain the values required to re-create the instance from the JSON
        object in a pythonic way:
            object = MyObject( **json.loads(json_string) )
        """
        return dict(
            parameters=self.parameters,
            telemetry_rollover_policy=self.telemetry_rollover_policy,
            tasks=list(map(
                lambda task: task.reprJSON(),
                self.tasks
            )),
        )
