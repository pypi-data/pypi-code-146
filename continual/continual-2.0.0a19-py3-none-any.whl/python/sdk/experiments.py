from __future__ import annotations
from typing import List, Optional
from continual.python.sdk.metrics import MetricsManager
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.artifacts import ArtifactsManager
from continual.python.sdk.tags import TagsManager
from continual.python.sdk.metadata import MetadataManager


class ExperimentManager(Manager):
    """Manages experiment resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/versions/{version}/experiments/{experiment}"

    def create(self) -> Experiment:
        """Create experiment.

        Returns
            An experiment.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> model_version.experiments.create()
            <Experiment object {'name': 'projects/test_project_1/environments/test_env/models/test_model/versions/cegl9qq5lsrkc0osu0ug/experiments/ceglm7a5lsrkc0osu120',
            'run_name': 'projects/test_project_1/environments/test_env/runs/test_run', 'state': 'PENDING', 'create_time': '2022-12-20T06:50:05.351093Z',
            'performance_metric_name': '', 'performance_metric_val': 0.0, 'training_config': '', 'error_message': '', 'stack_trace': ''}>
        """
        req = management_pb2.CreateExperimentRequest(
            parent=self.parent, run_name=self.run_name
        )
        resp = self.client._management.CreateExperiment(req)
        return Experiment.from_proto(resp, client=self.client)

    def get(self, id: str) -> Experiment:
        """Get experiment.

        Arguments:
            id: Experiment name or id.

        Returns
            An experiment.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> experiment = model_version.experiments.create()
            >>> model_version.experiments.get(experiment.id)
            <Experiment object {'name': 'projects/test_project_1/environments/test_env/models/test_model/versions/cegl9qq5lsrkc0osu0ug/experiments/ceglm7a5lsrkc0osu120',
            'run_name': 'projects/test_project_1/environments/test_env/runs/test_run', 'state': 'PENDING', 'create_time': '2022-12-20T06:50:05.351093Z',
            'performance_metric_name': '', 'performance_metric_val': 0.0, 'training_config': '', 'error_message': '', 'stack_trace': ''}>
        """
        req = management_pb2.GetExperimentRequest(name=self.name(id))
        resp = self.client._management.GetExperiment(req)
        return Experiment.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: str = None,
        latest: bool = True,
        all_projects: bool = False,
    ) -> List[Experiment]:
        """List experiments.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
            all_projects:  Whether to include all instances of this resource from the project or just from the current parent.

        Returns:
            A list of experiments.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> experiments = [model_version.experiments.create() for _ in range(100)]
            >>> len(model_version.experiments.list(page_size=10))
            10
            >>> len(model_version.experiments.list(page_size=50))
            50
        """
        req = management_pb2.ListExperimentsRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            latest=latest,
            all_projects=all_projects,
        )
        resp = self.client._management.ListExperiments(req)
        return [Experiment.from_proto(x, client=self.client) for x in resp.experiments]

    def list_all(self) -> Pager[Experiment]:
        """List all experiments.

        Pages through all experiments using an iterator.

        Returns:
            A iterator of all experiments.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> experiments = [model_version.experiments.create() for _ in range(100)]
            >>> len(list(model_version.experiments.list_all()))
            100
        """

        def next_page(next_page_token):
            req = management_pb2.ListExperimentsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListExperiments(req)
            return (
                [
                    Experiment.from_proto(x, client=self.client)
                    for x in resp.experiments
                ],
                resp.next_page_token,
            )

        return Pager(next_page)


class Experiment(Resource, types.Experiment):
    """Experiment resource."""

    _manager: ExperimentManager
    """Experiment manager."""

    _metrics: MetricsManager
    """Metrics Manager"""

    _artifacts: ArtifactsManager
    """Artifacts Manager"""

    _tags: TagsManager
    """Tags Manager"""

    _metadata: MetadataManager
    """Metadata Manager"""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/versions/{version}/experiments/{experiment}"

    def _init(self):
        self._manager = ExperimentManager(parent=self.parent, client=self.client)
        self._metrics = MetricsManager(parent=self.name, client=self.client)
        self._artifacts = ArtifactsManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )
        self._tags = TagsManager(parent=self.name, client=self.client)
        self._metadata = MetadataManager(parent=self.name, client=self.client)

    @property
    def metrics(self) -> MetricsManager:
        """Metrics Manager"""
        return self._metrics

    @property
    def artifacts(self) -> ArtifactsManager:
        """Artifacts Manager"""
        return self._artifacts

    @property
    def tags(self) -> TagsManager:
        """Tags Manager"""
        return self._tags

    @property
    def metadata(self) -> MetadataManager:
        """Metadata Manager"""
        return self._metadata
