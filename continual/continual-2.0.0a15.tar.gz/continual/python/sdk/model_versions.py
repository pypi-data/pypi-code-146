from __future__ import annotations

from typing import List, Optional
from continual.python.sdk.batchpredictions import (
    BatchPredictionManager,
)
from continual.python.sdk.events import EventManager
from continual.python.sdk.resource_checks import ResourceChecksManager
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.experiments import ExperimentManager
from continual.python.sdk.promotions import PromotionManager
from continual.python.sdk.metrics import MetricsManager
from continual.python.sdk.artifacts import ArtifactsManager
from continual.python.sdk.tags import TagsManager
from continual.python.sdk.metadata import MetadataManager


class ModelVersionManager(Manager):
    """Manages Model Version resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/versions/{version}"

    def create(self) -> ModelVersion:
        """Create a model version for local development

        Returns
            A Model Version.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model.model_versions.create()
            <ModelVersion object {'name': 'projects/test_proj_4/environments/test_env/models/my_model/versions/ceg98ea5lsrt9r5a8l10',
            'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0',
            'state': 'CREATED', 'create_time': '2022-12-19T16:41:29.232614Z', 'update_time': '2022-12-19T16:41:29.232614Z',
            'experiment_name': '', 'error_message': '', 'stack_trace': '', 'training_row_count': '0', 'validation_row_count': '0',
            'test_row_count': '0', 'performance_metric': '', 'performance_metric_val': 0.0, 'promotion': '', 'promoted': False}>
        """
        req = management_pb2.CreateModelVersionRequest(
            parent=self.parent, run_name=self.run_name
        )
        resp = self.client._management.CreateModelVersion(req)
        return ModelVersion.from_proto(resp, client=self.client)

    def get(self, id: str) -> ModelVersion:
        """Get model version.

        Arguments:
            id: Model name or id.

        Returns
            An Model Version.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> model.model_versions.get(model_version.id)
            <ModelVersion object {'name': 'projects/test_proj_4/environments/test_env/models/my_model/versions/ceg98ea5lsrt9r5a8l10',
            'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0',
            'state': 'CREATED', 'create_time': '2022-12-19T16:41:29.232614Z', 'update_time': '2022-12-19T16:41:29.232614Z',
            'experiment_name': '', 'error_message': '', 'stack_trace': '', 'training_row_count': '0', 'validation_row_count': '0',
            'test_row_count': '0', 'performance_metric': '', 'performance_metric_val': 0.0, 'promotion': '', 'promoted': False}>
        """
        req = management_pb2.GetModelVersionRequest(name=self.name(id))
        resp = self.client._management.GetModelVersion(req)
        return ModelVersion.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: str = None,
        latest: bool = True,
        all_projects: bool = False,
    ) -> List[ModelVersion]:
        """List model versions.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
            all_projects: Whether to include all instances of this resource from the project or just from the current parent.

        Returns:
            A list of model versions.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> models = [model.model_versions.create() for _ in range(3)]
            >>> first_model_version = model.model_versions.list(page_size=10)[0]               # Get first model version
            >>> latest_model_version = model.model_versions.list(page_size=10, latest=True)[0] # Get latest model version
        """
        req = management_pb2.ListModelVersionsRequest(
            parent=self.parent,
            page_size=page_size,
            all_projects=all_projects,
            order_by=order_by,
            latest=latest,
        )
        resp = self.client._management.ListModelVersions(req)
        return [
            ModelVersion.from_proto(x, client=self.client) for x in resp.model_versions
        ]

    def list_all(self) -> Pager[ModelVersion]:
        """List all model versions.

        Pages through all model versions using an iterator.

        Returns:
            A iterator of all model versions.

        Examples:
            >>> ... # Assume client, project, environment are defined
            >>> run = env.runs.create("My run")
            >>> model = run.models.get("my_model")
            >>> dvs = [model.model_versions.create() for _ in range(3)]
            >>> len(list(model.model_versions.list_all())) # List all model versions
            3
        """

        def next_page(next_page_token):
            req = management_pb2.ListModelVersionsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListModelVersions(req)
            return (
                [
                    ModelVersion.from_proto(x, client=self.client)
                    for x in resp.model_versions
                ],
                resp.next_page_token,
            )

        return Pager(next_page)


class ModelVersion(Resource, types.ModelVersion):
    """Model version resource."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/versions/{version}"

    _manager: ModelVersionManager

    _experiments: ExperimentManager

    _events: EventManager

    _promotions: PromotionManager

    _resource_checks: ResourceChecksManager

    _batch_predictions: BatchPredictionManager

    _metrics: MetricsManager

    _artifacts: ArtifactsManager

    _tags: TagsManager

    _metadata: MetadataManager

    def _init(self):
        self._manager = ModelVersionManager(
            parent=self.parent, client=self.client, run_name=self.run_name
        )
        self._promotions = PromotionManager(
            parent=self.parent, client=self.client, run_name=self.run_name
        )
        self._batch_predictions = BatchPredictionManager(
            parent=self.parent, client=self.client, run_name=self.run_name
        )
        self._experiments = ExperimentManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )
        self._events = EventManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )
        self._metrics = MetricsManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )
        self._artifacts = ArtifactsManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )
        self._tags = TagsManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )
        self._metadata = MetadataManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )

        self._resource_checks = ResourceChecksManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )

    @property
    def promotions(self) -> PromotionManager:
        """Promotion manager."""
        return self._promotions

    @property
    def batch_predictions(self) -> BatchPredictionManager:
        """Batch Prediction manager."""
        return self._batch_predictions

    @property
    def experiments(self) -> ExperimentManager:
        """Experiment manager."""
        return self._experiments

    @property
    def metrics(self) -> MetricsManager:
        """Metrics manager."""
        return self._metrics

    @property
    def artifacts(self) -> ArtifactsManager:
        """Artifacts manager."""
        return self._artifacts

    @property
    def tags(self) -> TagsManager:
        """Tags manager."""
        return self._tags

    @property
    def resource_checks(self) -> ResourceChecksManager:
        """Resource Checks manager."""
        return self._resource_checks

    @property
    def metadata(self) -> MetadataManager:
        """Metadata manager."""
        return self._metadata

    @property
    def events(self) -> EventManager:
        """Event manager."""
        return self._events
