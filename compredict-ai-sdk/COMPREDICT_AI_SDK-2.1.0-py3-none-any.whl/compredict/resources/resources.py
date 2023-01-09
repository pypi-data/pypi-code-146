from tempfile import NamedTemporaryFile
from typing import Union, List

from pandas import DataFrame

from compredict.resources.base import BaseResource


class Algorithm(BaseResource):

    def __init__(self, **kwargs):
        super(Algorithm, self).__init__(**kwargs)
        self._last_result = None
        # create version
        for i, version in enumerate(self.versions):
            self.versions[i] = Version(algorithm_id=self.id, **version)

    def run(self, features: Union[str, DataFrame, dict], **kwargs) -> Union["Task", "Result"]:
        """ Will call the last version of an algorithm."""
        self._last_result = self.client.run_algorithm(self.id, features, **kwargs)
        return self.last_results

    def get_versions(self) -> List["Version"]:
        """Ordered by latest version alphabetically."""
        return self.versions

    def get_detailed_template(self, file_type: str = 'input') -> NamedTemporaryFile:
        """return the template of the latest version"""
        return self.client.get_template(self.id, file_type)

    def get_detailed_graph(self, file_type: str = 'input') -> NamedTemporaryFile:
        """return the graph of the latest version"""
        return self.client.get_graph(self.id, file_type)

    def get_response_time(self) -> str:
        return self.versions[0].result

    def get_template(self, file_type: str = 'input') -> dict:
        return self.versions[0].output_format if file_type == 'output' else self.versions[0].features_format

    @property
    def last_results(self) -> "Result":
        return self._last_result

    def __str__(self):
        return self.name


class Version(BaseResource):

    def __init__(self, **kwargs):
        super(Version, self).__init__(**kwargs)
        if self.algorithm_id is None:
            raise ValueError("Please provide `algorithm_id`!")
        self._last_result = None

    def run(self, data: Union[str, DataFrame, dict], **kwargs) -> Union["Task", "Result"]:
        """Will call its specific version of the algorithm."""
        self._last_result = self.client.run_algorithm(self.algorithm_id, data, version=self.version, **kwargs)
        return self.last_results

    def get_detailed_template(self, file_type: str = 'input') -> NamedTemporaryFile:
        return self.client.get_template(self.algorithm_id, file_type=file_type, version=self.version)

    def get_detailed_graph(self, file_type: str = 'input') -> NamedTemporaryFile:
        return self.client.get_graph(self.algorithm_id, file_type=file_type, version=self.version)

    def get_response_time(self) -> str:
        return self.result

    def get_template(self, file_type: str = 'input') -> dict:
        return self.output_format if file_type == 'output' else self.features_format

    @property
    def last_results(self) -> "Result":
        return self._last_result

    def __str__(self):
        return self.algorithm_id + ":" + self.version

    def __repr__(self):
        return "Object: {}:{}".format(self.algorithm_id, self.version)


class Evaluation(BaseResource):

    def __init__(self, **kwargs):
        super(Evaluation, self).__init__(**kwargs)


class Result(BaseResource):

    def __init__(self, **kwargs):
        super(Result, self).__init__(**kwargs)


class Monitor(BaseResource):

    def __init__(self, **kwargs):
        super(Monitor, self).__init__(**kwargs)


class Task(BaseResource):
    STATUS_PENDING = "Pending"
    STATUS_PROGRESS = "In Progress"
    STATUS_FINISHED = "Finished"

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.status = self.status if self.status is not None else Task.STATUS_PENDING
        self.success = self.success if self.success is not None else None
        self.error = self.error if self.error is not None else None
        self._set_results(self.predictions, self.evaluations, self.monitors)

    def update(self):
        task = self.client.get_task_results(self.job_id)
        self.__dict__.update(task.__dict__)

    def get_current_status(self) -> str:
        return self.status

    def cancel(self):
        task = self.client.cancel_task(self.job_id)
        self.__dict__.update(task.__dict__)

    def _set_results(self, predictions: dict, evaluations: dict, monitors: dict):
        self.predictions = None
        self.evaluations = None
        self.monitors = None
        if self.status == Task.STATUS_FINISHED and self.success is True:
            self.predictions = predictions
            self.evaluations = evaluations
            self.monitors = monitors
