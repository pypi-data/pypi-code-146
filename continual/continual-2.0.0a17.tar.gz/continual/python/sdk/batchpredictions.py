from __future__ import annotations
from typing import Iterator, List, Optional
from continual.python.sdk.metrics import MetricsManager

from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.artifacts import ArtifactsManager
from continual.python.sdk.resource_checks import ResourceChecksManager
from continual.python.sdk.tags import TagsManager
from continual.python.sdk.metadata import MetadataManager


class BatchPredictionManager(Manager):
    """Manages Batch Prediction resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/batchPredictions/{batch_prediction_job}"

    def create(self, model_version_name: str) -> BatchPrediction:
        """Get batch prediction job.

        Arguments:
            model_version_name: Name of the model version to use for prediction

        Returns
            A Batch prediction.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> model.batch_predictions.create(model_version_name=model_version.name)     # Create from specific model version
            <BatchPrediction object {'name': 'projects/test_proj_4/environments/test_env/models/my_model/batchPredictions/ceg9bk25lsrt9r5a8l5g',
            'state': 'CREATED', 'model_version': 'projects/test_proj_4/environments/test_env/models/my_model/versions/ceg99oq5lsrt9r5a8l2g',
            'create_time': '2022-12-19T16:48:16.368146Z', 'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0',
            'prediction_count': '0', 'error_message': '', 'stack_trace': ''}>
        """
        req = management_pb2.CreateBatchPredictionRequest(
            parent=self.parent,
            run_name=self.run_name,
            trained_model_version_name=model_version_name,
        )
        resp = self.client._management.CreateBatchPrediction(req)
        return BatchPrediction.from_proto(resp, client=self.client)

    def get(self, id: str) -> BatchPrediction:
        """Get batch prediction job.

        Arguments:
            id: Batch Prediction  name or id.

        Returns
            A Batch prediction.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> batchprediction = model.batch_predictions.create(model_version_name=model_version.name)
            >>> model.batch_predictions.get(batchprediction.id)     # Get from id
            <BatchPrediction object {'name': 'projects/test_proj_4/environments/test_env/models/my_model/batchPredictions/ceg9bk25lsrt9r5a8l5g',
            'state': 'CREATED', 'model_version': 'projects/test_proj_4/environments/test_env/models/my_model/versions/ceg99oq5lsrt9r5a8l2g',
            'create_time': '2022-12-19T16:48:16.368146Z', 'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0',
            'prediction_count': '0', 'error_message': '', 'stack_trace': ''}>
        """
        req = management_pb2.BatchPredictionRequest(name=self.name(id))
        resp = self.client._management.GetBatchPrediction(req)
        return BatchPrediction.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        latest: bool = True,
        order_by: Optional[str] = None,
        all_projects: bool = False,
    ) -> List[BatchPrediction]:
        """List batch prediction jobs.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
            all_projects: Whether to include all instances of this resource from the project or just from the current parent.

        Returns:
            A list of batch prediction jobs.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> batchpredictions = [model.batch_predictions.create(model_version_name=model_version.name) for _ in range(10)]
            >>> len(model.batch_predictions.list(page_size=10))     # List 10 batch predictions
            10
        """
        req = management_pb2.ListBatchPredictionsRequest(
            parent=self.parent,
            latest=latest,
            order_by=order_by,
            page_size=page_size,
            all_projects=all_projects,
        )
        resp = self.client._management.ListBatchPredictions(req)
        return [
            BatchPrediction.from_proto(u, client=self.client)
            for u in resp.batch_predictions
        ]

    def list_all(self) -> Iterator[BatchPrediction]:
        """List all batch prediction jobs.

        Pages through all batch prediction jobs using an iterator.

        Returns:
            A iterator of all batch prediction jobs.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> batchpredictions = [model.batch_predictions.create(model_version_name=model_version.name) for _ in range(10)]
            >>> len(list(model.batch_predictions.list_all()))     # List all batch predictions
            10
        """

        def next_page(next_page_token):
            req = management_pb2.ListBatchPredictionsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListBatchPredictions(req)
            return (
                [
                    BatchPrediction.from_proto(u, client=self.client)
                    for u in resp.batch_predictions
                ],
                resp.next_page_token,
            )

        return Pager(next_page)


class BatchPrediction(Resource, types.BatchPrediction):
    """BatchPrediction resource."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/batchPredictions/{batch_prediction_job}"

    _manager: BatchPredictionManager
    """BatchPrediction manager"""

    _metrics: MetricsManager
    """Metrics Manager"""

    _artifacts: ArtifactsManager
    """Artifacts Manager"""

    _tags: TagsManager
    """Tags Manager"""

    _metadata: MetadataManager
    """Metadata Manager"""

    _resource_checks: ResourceChecksManager

    def _init(self):
        self._manager = BatchPredictionManager(parent=self.parent, client=self.client)
        self._artifacts = ArtifactsManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )
        self._tags = TagsManager(parent=self.name, client=self.client)
        self._metadata = MetadataManager(parent=self.name, client=self.client)
        self._metrics = MetricsManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )
        self._resource_checks = ResourceChecksManager(
            parent=self.name, client=self.client, run_name=self.run_name
        )

    @property
    def artifacts(self) -> ArtifactsManager:
        """Artifacts Manager."""
        return self._artifacts

    @property
    def tags(self) -> TagsManager:
        """Tags Manager."""
        return self._tags

    @property
    def metadata(self) -> MetadataManager:
        """Metadata Manager."""
        return self._metadata

    @property
    def metrics(self) -> MetricsManager:
        """Metrics Manager."""
        return self._metrics

    @property
    def resource_checks(self) -> ResourceChecksManager:
        """Resource Checks manager."""
        return self._resource_checks
