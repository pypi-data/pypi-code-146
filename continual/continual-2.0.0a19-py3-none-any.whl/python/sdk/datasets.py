from __future__ import annotations
from typing import List, Optional
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.dataset_versions import DatasetVersionManager
from continual.python.sdk.promotions import PromotionManager
from continual.python.sdk.tags import TagsManager
from continual.python.sdk.metadata import MetadataManager


from continual.python.sdk.batchpredictions import (
    BatchPredictionManager,
)


class DatasetManager(Manager):
    """Manages dataset resources."""

    name_pattern: str = (
        "projects/{project}/environments/{environment}/datasets/{dataset}"
    )

    def create(
        self,
        display_name: str,
        description: Optional[str] = "",
        get_if_exists: bool = True,
    ) -> Dataset:
        """Create dataset.

        Arguments:
            display_name: Dataset name or id.
            description: A brief description of this dataset.
            get_if_exists: If True, this call will get the dataset with the display name, else throw an error.

        Returns
            A Dataset.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> dataset = run.datasets.create(display_name="my_dataset", description="Customer churn dataset")
            <Dataset object {'name': 'projects/test_proj_2/environments/test_env/datasets/my_dataset',
            'description': 'Customer churn dataset', 'author': 'users/BefwyWcn6x7SNC533zfaAR',
            'display_name': 'my_dataset', 'create_time': '2022-12-19T06:06:34.763763Z', 'update_time': '2022-12-19T06:06:34.763763Z',
            'state': '', 'current_version': ''}>
        """
        req = management_pb2.CreateDatasetRequest(
            name=self.name(display_name),
            description=description,
            get_if_exists=get_if_exists,
            run=self.run_name,
        )
        resp = self.client._management.CreateDataset(req)
        return Dataset.from_proto(resp, client=self.client, parent_run=self.run_name)

    def get(self, id: str) -> Dataset:
        """Get dataset.

        Arguments:
            id: Dataset name or id.

        Returns
            An experiment.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> dataset = run.datasets.get("my_dataset")
            <Dataset object {'name': 'projects/test_proj_2/environments/test_env/datasets/my_dataset',
            'description': 'Customer churn dataset', 'author': 'users/BefwyWcn6x7SNC533zfaAR', 'display_name': 'my_dataset',
            'create_time': '2022-12-19T06:06:34.763763Z', 'update_time': '2022-12-19T06:06:34.763763Z',
            'state': '', 'current_version': ''}>
        """
        req = management_pb2.GetDatasetRequest(name=self.name(id))
        resp = self.client._management.GetDataset(req)
        return Dataset.from_proto(resp, client=self.client, parent_run=self.run_name)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: str = None,
        latest: bool = True,
        all_projects: bool = False,
    ) -> List[Dataset]:
        """List dataset.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
            all_projects:  Whether to include all instances of this resource from the project or just from the current parent.

        Returns:
            A list of Datasets.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> ds = [run.datasets.create(display_name=f"my_dataset_{i}", description=f"Customer churn dataset {i}") for i in range(10)]
            >>> [r.display_name for r in run.datasets.list(page_size=10)]
            ['my_dataset_9', 'my_dataset_8', 'my_dataset_7', 'my_dataset_6', 'my_dataset_5', 'my_dataset_4', 'my_dataset_3', 'my_dataset_2', 'my_dataset_1', 'my_dataset_0']
            >>> [r.display_name for r in run.datasets.list(page_size=10, latest=False)]
            ['my_dataset_0', 'my_dataset_1', 'my_dataset_2', 'my_dataset_3', 'my_dataset_4', 'my_dataset_5', 'my_dataset_6', 'my_dataset_7', 'my_dataset_8', 'my_dataset_9']
            >>> [r.display_name for r in run.datasets.list(page_size=10, order_by="display_name")]
            ['my_dataset_0', 'my_dataset_1', 'my_dataset_2', 'my_dataset_3', 'my_dataset_4', 'my_dataset_5', 'my_dataset_6', 'my_dataset_7', 'my_dataset_8', 'my_dataset_9']
        """
        req = management_pb2.ListDatasetsRequest(
            parent=self.parent,
            page_size=page_size,
            all_projects=all_projects,
            order_by=order_by,
            latest=latest,
        )
        resp = self.client._management.ListDatasets(req)
        return [
            Dataset.from_proto(x, client=self.client, parent_run=self.run_name)
            for x in resp.datasets
        ]

    def list_all(self) -> Pager[Dataset]:
        """List all dataset.

        Pages through all datasets using an iterator.

        Returns:
            A iterator of all dataset.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> ds = [run.datasets.create(display_name=f"my_dataset_{i}", description=f"Customer churn dataset {i}") for i in range(10)]
            >>> [r.display_name for r in run.datasets.list_all()]
            ['my_dataset_0', 'my_dataset_1', 'my_dataset_2', 'my_dataset_3', 'my_dataset_4', 'my_dataset_5', 'my_dataset_6', 'my_dataset_7', 'my_dataset_8', 'my_dataset_9']
        """

        def next_page(next_page_token):
            req = management_pb2.ListDatasetsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListDatasets(req)
            return (
                [
                    Dataset.from_proto(x, client=self.client, parent_run=self.run_name)
                    for x in resp.datasets
                ],
                resp.next_page_token,
            )

        return Pager(next_page)


class Dataset(Resource, types.Dataset):
    """Dataset resource."""

    name_pattern: str = (
        "projects/{project}/environments/{environment}/datasets/{dataset}"
    )
    _manager: DatasetManager
    """Dataset Manager."""

    _dataset_versions: DatasetVersionManager
    """Dataset version manager."""

    _batch_predictions: BatchPredictionManager
    """Batch Prediction manager."""

    _tags: TagsManager
    """Tags Manager"""

    _metadata: MetadataManager
    """Metadata Manager"""

    def _init(self):
        self._manager = DatasetManager(
            parent=self.parent, client=self.client, run_name=self.parent_run
        )
        self._dataset_versions = DatasetVersionManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )
        self._batch_predictions = BatchPredictionManager(
            parent=self.name, client=self.client
        )
        self._tags = TagsManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )
        self._metadata = MetadataManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )

    @property
    def dataset_versions(self) -> DatasetVersionManager:
        """Dataset version manager."""
        return self._dataset_versions

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
