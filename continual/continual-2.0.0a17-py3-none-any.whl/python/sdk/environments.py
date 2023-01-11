from __future__ import annotations
from typing import List, Optional
from continual.python.sdk.artifacts import ArtifactsManager
from continual.python.sdk.datasets import DatasetManager
from continual.python.sdk.runs import RunManager
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.models import ModelManager


class EnvironmentManager(Manager):
    """Manages environment resources."""

    name_pattern: str = "projects/{project}/environments/{environment}"

    def create(
        self, id: str, source: str = "", get_if_exists: bool = True
    ) -> Environment:
        """Create an environment.

        New environments are identified by a unique ID within
        their parent project.

        Arguments:
            id: Environment ID.
            source: Metadata about how this environment was created.
            get_if_exists: If True and the environment already exists, return the existing
                environment.  If False and the environment already exists, raise an error.

        Returns:
            A new environment.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.name)
            >>> proj.environments.create(id="example")
            <Environment object {'name': 'projects/example_proj_1/environments/example',
            'summary': {'feature_set_health': {'healthy_count': 0, 'unhealthy_count': 0, 'critical_count': 0},
            'model_health': {'healthy_count': 0, 'unhealthy_count': 0, 'critical_count': 0}, 'feature_set_count': 0,
            'feature_set_row_count': '0', 'feature_set_bytes': '0', 'feature_count': 0, 'connection_count': 0,
            'model_count': 0, 'model_version_count': 0, 'experiment_count': '0', 'prediction_count': '0'},
            'data_store': {'type': '', 'is_demo_data_store': False}, 'update_time': '2022-12-15T23:47:28.641932Z',
            'create_time': '2022-12-15T23:47:28.641932Z', 'scheduling_enabled': False, 'source': '', 'env_type': '',
            'is_protected': False, 'is_ephemeral': False}>
            >>> env = proj.environments.create(id="example")) # get_if_exists is True by default
            >>> env = proj.environments.create(id="example", get_if_exists=False) # Raises an error
            continual.python.sdk.exceptions.AlreadyExistsError: ('Resource already exists.', {'name': 'Environment with ID (example) already exists.'})
        """
        req = management_pb2.CreateEnvironmentRequest(
            parent=self.parent,
            environment_id=id,
            source=source,
            get_if_exists=get_if_exists,
        )
        resp = self.client._management.CreateEnvironment(req)
        return Environment.from_proto(resp, client=self.client)

    def name(self, id: str, parent: Optional[str] = None) -> str:
        """Get the fully qualified name of this environment.

        Arguments:
            id: The environment id.
            parent: The parent project name.

        Return:
            string name of the environment.
        """
        if "/" in id:
            # Don't allow names to override manager parent config since this is confusing
            # and is typically a bug in the user code.
            if parent is not None and parent != "" and not id.startswith(parent):
                raise ValueError(f"Resource {id} not a child of {parent}.")
            return id

        name_str = self.parent or ""
        name_str += "/environments/" + id
        return name_str

    def get(self, id: str = "production") -> Environment:
        """Get environment.

        Arguments:
            id: environment name or id.

        Returns
            A environment.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.name)
            >>> env = proj.environments.create(id="example")
            >>> proj.environments.get(id=env.name)
            <Environment object {'name': 'projects/example_proj_1/environments/example',
            'summary': {'feature_set_health': {'healthy_count': 0, 'unhealthy_count': 0, 'critical_count': 0},
            'model_health': {'healthy_count': 0, 'unhealthy_count': 0, 'critical_count': 0}, 'feature_set_count': 0,
            'feature_set_row_count': '0', 'feature_set_bytes': '0', 'feature_count': 0, 'connection_count': 0,
            'model_count': 0, 'model_version_count': 0, 'experiment_count': '0', 'prediction_count': '0'},
            'data_store': {'type': '', 'is_demo_data_store': False}, 'update_time': '2022-12-15T23:47:28.641932Z',
            'create_time': '2022-12-15T23:47:28.641932Z', 'scheduling_enabled': False, 'source': '', 'env_type': '',
            'is_protected': False, 'is_ephemeral': False}>
        """
        req = management_pb2.GetEnvironmentRequest(name=self.name(id))
        resp = self.client._management.GetEnvironment(req)
        return Environment.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: Optional[str] = None,
        latest: bool = True,
    ) -> List[Environment]:
        """List environments.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.

        Returns:
            A list of environments.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.name)
            >>> envs = [proj.environments.create(id=f"env{i}") for i in range(3)]
            >>> [env.name for env in proj.environments.list(page_size=5, latest=True)]
            ['projects/example_proj_2/environments/env2', 'projects/example_proj_2/environments/env1',
            'projects/example_proj_2/environments/env0', 'projects/example_proj_2/environments/production']
        """
        req = management_pb2.ListEnvironmentsRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            latest=latest,
        )
        resp = self.client._management.ListEnvironments(req)
        return [
            Environment.from_proto(x, client=self.client) for x in resp.environments
        ]

    def list_all(self) -> Pager[Environment]:
        """List all environments.

        Pages through all environments using an iterator.

        Returns:
            A iterator of all environments.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.name)
            >>> envs = [proj.environments.create(id=f"env{i}") for i in range(3)]
            >>> [env.name for env in proj.environments.list_all()]
            ['projects/example_proj_2/environments/env0', 'projects/example_proj_2/environments/env1',
            'projects/example_proj_2/environments/env2', 'projects/example_proj_2/environments/production']
        """

        def next_page(next_page_token):
            req = management_pb2.ListEnvironmentsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListEnvironments(req)
            return (
                [
                    Environment.from_proto(x, client=self.client)
                    for x in resp.environments
                ],
                resp.next_page_token,
            )

        return Pager(next_page)

    def delete(
        self,
        id: str,
    ) -> None:
        """Delete an Environment.

        Arguments:
            id: Environment name or id.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.name)
            >>> env = proj.environments.create(id="example")
            >>> len(proj.environments.list_all())
            1
            >>> proj.environments.delete(id=env.name)
            >>> len(proj.environments.list_all())
            0
        """

        req = management_pb2.DeleteEnvironmentRequest(name=self.name(id))
        self.client._management.DeleteEnvironment(req)


class Environment(Resource, types.Environment):
    """Environment resource."""

    name_pattern: str = "projects/{project}/environments/{environment}"
    _manager: EnvironmentManager

    _models: ModelManager

    _datasets: DatasetManager

    _artifacts: ArtifactsManager

    _runs: RunManager

    def _init(self):
        self._manager = EnvironmentManager(parent=self.parent, client=self.client)
        self._models = ModelManager(parent=self.name, client=self.client)
        self._datasets = DatasetManager(parent=self.name, client=self.client)
        self._artifacts = ArtifactsManager(parent=self.name, client=self.client)
        self._runs = RunManager(parent=self.name, client=self.client)

    @property
    def models(self) -> ModelManager:
        """Models manager."""
        return self._models

    @property
    def datasets(self) -> DatasetManager:
        """Datasets manager."""
        return self._datasets

    @property
    def artifacts(self) -> ArtifactsManager:
        """Artifacts manager."""
        return self._artifacts

    @property
    def runs(self) -> RunManager:
        """Runs manager."""
        return self._runs

    def delete(self) -> None:
        """Delete environment.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.name)
            >>> env = proj.environments.create(id="example")
            >>> len(proj.environments.list_all())
            1
            >>> env.delete()
            >>> len(proj.environments.list_all())
            0
        """
        self._manager.delete(self.name)
