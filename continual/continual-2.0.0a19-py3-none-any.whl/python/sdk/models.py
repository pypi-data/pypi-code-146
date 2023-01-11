from __future__ import annotations
from typing import List, Optional
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.model_versions import ModelVersionManager
from continual.python.sdk.promotions import PromotionManager
from continual.python.sdk.tags import TagsManager
from continual.python.sdk.metadata import MetadataManager


from continual.python.sdk.batchpredictions import (
    BatchPredictionManager,
)


class ModelManager(Manager):
    """Manages model resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}"

    def create(
        self,
        display_name: str,
        description: Optional[str] = "",
        get_if_exists: bool = True,
    ) -> Model:
        """Create model.

        Arguments:
            display_name: Dataset name or id.
            description: A brief description of this model.
            get_if_exists: If the model with the display name already exists, get it if this is true, else throw an error.

        Returns
            A Model.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> run.models.create(display_name="my_model", description="Customer churn model")
            <Model object {'name': 'projects/test_proj_4/environments/test_env/models/my_model',
            'description': 'Customer churn model', 'author': 'users/BefwyWcn6x7SNC533zfaAR',
            'display_name': 'my_model', 'create_time': '2022-12-19T16:31:26.638028Z',
            'update_time': '2022-12-19T16:31:26.638028Z', 'state': '', 'current_version': '',
            'latest_model_version': '', 'latest_batch_prediction': ''}>
        """
        req = management_pb2.CreateModelRequest(
            name=self.name(display_name),
            description=description,
            get_if_exists=get_if_exists,
            run=self.run_name,
        )
        resp = self.client._management.CreateModel(req)
        return Model.from_proto(resp, client=self.client, parent_run=self.run_name)

    def get(self, id: str) -> Model:
        """Get model.

        Arguments:
            id: Model name or id.

        Returns
            An experiment.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> run.models.get("my_model")
            <Model object {'name': 'projects/test_proj_4/environments/test_env/models/my_model',
            'description': 'Customer churn model', 'author': 'users/BefwyWcn6x7SNC533zfaAR',
            'display_name': 'my_model', 'create_time': '2022-12-19T16:31:26.638028Z',
            'update_time': '2022-12-19T16:31:26.638028Z', 'state': '', 'current_version': '',
            'latest_model_version': '', 'latest_batch_prediction': ''}>
        """
        req = management_pb2.GetModelRequest(name=self.name(id))
        resp = self.client._management.GetModel(req)
        return Model.from_proto(resp, client=self.client, parent_run=self.run_name)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: Optional[str] = None,
        latest: bool = True,
        all_projects: bool = False,
    ) -> List[Model]:
        """List model.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
            all_projects: Whether to include all instances of this resource from the project or just from the current parent.

        Returns:
            A list of models.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> models = [run.models.create(display_name=f"my_model_{i}", description="Customer churn model") for i in range(3)]
            >>> [model.display_name for model in run.models.list(page_size=3)]
            ['my_model_2', 'my_model_1', 'my_model_0']
            >>> [model.display_name for model in run.models.list(page_size=3, latest=False)]
            ['my_model_0', 'my_model_1', 'my_model_2']
        """
        req = management_pb2.ListModelsRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            latest=latest,
            all_projects=all_projects,
        )
        resp = self.client._management.ListModels(req)
        return [
            Model.from_proto(x, client=self.client, parent_run=self.run_name)
            for x in resp.models
        ]

    def list_all(self) -> Pager[Model]:
        """List all model.

        Pages through all model using an iterator.

        Returns:
            A iterator of all model.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> models = [run.models.create(display_name=f"my_model_{i}", description="Customer churn model") for i in range(3)]
            >>> [model.display_name for model in run.models.list_all()]
            ['my_model_0', 'my_model_1', 'my_model_2']
        """

        def next_page(next_page_token):
            req = management_pb2.ListModelsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListModels(req)
            return (
                [
                    Model.from_proto(x, client=self.client, parent_run=self.run_name)
                    for x in resp.models
                ],
                resp.next_page_token,
            )

        return Pager(next_page)


class Model(Resource, types.Model):
    """Model resource."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}"
    _manager: ModelManager
    """Model manager."""

    _model_versions: ModelVersionManager
    """ModelVersion manager."""

    _promotions: PromotionManager
    """Promotion manager."""

    _batch_predictions: BatchPredictionManager
    """Batch Prediction  manager."""

    _tags: TagsManager
    """Tags Manager"""

    _metadata: MetadataManager
    """Metadata Manager"""

    def _init(self):
        self._manager = ModelManager(
            parent=self.parent, client=self.client, run_name=self.parent_run
        )
        self._model_versions = ModelVersionManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )
        self._promotions = PromotionManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )
        self._batch_predictions = BatchPredictionManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )
        self._tags = TagsManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )
        self._metadata = MetadataManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )

    @property
    def model_versions(self) -> ModelVersionManager:
        """ModelVersion manager."""
        return self._model_versions

    @property
    def promotions(self) -> PromotionManager:
        """Promotion manager."""
        return self._promotions

    @property
    def batch_predictions(self) -> BatchPredictionManager:
        """Batch Prediction manager."""
        return self._batch_predictions

    @property
    def tags(self) -> TagsManager:
        """Tags Manager"""
        return self._tags

    @property
    def metadata(self) -> MetadataManager:
        """Metadata Manager"""
        return self._metadata
