from __future__ import annotations
from continual.python.sdk.artifacts import ArtifactsManager
from continual.python.sdk.batchpredictions import BatchPredictionManager
from continual.python.sdk.data_profiles import DataProfilesManager
from continual.python.sdk.dataset_version_assignments import (
    DatasetVersionAssignmentManager,
)
from continual.python.sdk.dataset_versions import DatasetVersionManager
from continual.python.sdk.datasets import DatasetManager
from continual.python.sdk.events import EventManager
from continual.python.sdk.experiments import ExperimentManager
from continual.python.sdk.metadata import MetadataManager
from continual.python.sdk.metrics import MetricsManager
from continual.python.sdk.model_versions import ModelVersionManager
from continual.python.sdk.models import ModelManager
from continual.python.sdk.promotions import PromotionManager
from continual.python.sdk.resource_checks import ResourceChecksManager
from continual.python.sdk.tags import TagsManager
import grpc
from typing import Optional, Tuple
from google.protobuf.empty_pb2 import Empty
from continual.python.sdk.config import Config
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import management_pb2_grpc
from continual.python.sdk.projects import ProjectManager, Project
from continual.python.sdk.organizations import OrganizationManager
from continual.python.sdk.runs import RunManager
from continual.python.sdk.users import UserManager, User
from continual.python.sdk.interceptors import AuthInterceptor
from continual.python.sdk.exceptions import normalize_exceptions_for_class
from continual.python.utils.client_utils import get_management_channel
from importlib.metadata import version

try:
    __version__ = version("continual")
except:
    __version__ = "local-dev"
from continual.python.sdk.identifiers import ProjectEnvironmentIdentifer


class Client:
    """Continual client."""

    _users: UserManager

    _projects: ProjectManager

    _organizations: OrganizationManager

    _runs: RunManager

    _models: ModelManager

    _model_versions: ModelVersionManager

    _experiments: ExperimentManager

    _batch_predictions: BatchPredictionManager

    _promotions: PromotionManager

    _datasets: DatasetManager

    _dataset_versions: DatasetVersionManager

    _data_profiles: DataProfilesManager

    _assignments: DatasetVersionAssignmentManager

    _events: EventManager

    _metadata: MetadataManager

    _metrics: MetricsManager

    _tags: TagsManager

    _resource_checks: ResourceChecksManager

    _artifacts: ArtifactsManager

    _config: Config

    _management: management_pb2_grpc.ManagementAPIStub

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        project: Optional[str] = None,
        environment: Optional[str] = None,
        verify: bool = True,
    ):
        """Initialize client.

        It is recommended to use `continual login` to generate a
        local on-disk API key.

        Arguments:
            api_key: API key.
            project: Default project.
            endpoint: Continual endpoint. Default is http://sdk.continual.ai.
            environment: Project environment
            verify: Whether or not to verify the arguments on init

        Examples:
            >>> from continual import Client
            >>> c = Client(verify=False)   # Does not verify API key and project name
            <continual.python.sdk.client.Client object at 0x7f63a3e2b4c0>
            >>> c = Client(endpoint="http://sdk.continual.ai", api_key="sessions/l123kjnal34AiS2", project="example-project", environment="example-env", verify=False)
            <continual.python.sdk.client.Client object at 0x7f63a3e2b4c0>
            >>> c.config.endpoint, c.config.project, c.config.environment
            ('http://sdk.continual.ai', 'projects/example-project', 'example-env')
            >>> Client(verify=True)  # Will attempt to verify API key, project name, and environment in YAML or ENV config
        """
        # Initialize config to process args
        self._config = Config(
            endpoint=endpoint, api_key=api_key, project=project, environment=environment
        )

        if self.config.api_key and verify:
            self.set_config_api_key(api_key=self.config.api_key, save=False)
        else:
            # At the very least initialie the management channel to allow register and login
            self._init_grpc_connnections(api_key=self.config.api_key)
            self._init_managers()

        # Initialize managers that only depend on client
        self._users = UserManager(client=self)
        self._organizations = OrganizationManager(client=self)
        self._projects = ProjectManager(client=self)

        # Verify and set proj and env IF they are set in config
        if self.config.project and verify:
            self.set_config_project(
                project=self.config.project,
                save=False,
                environment=self.config.environment,
            )
            if self.config.environment is None or self.config.environment == "":
                self.set_config_environment(self.config.environment, save=False)

        if environment is not None and verify:
            self.set_config_environment(environment, save=False)

    @property
    def users(self) -> UserManager:
        """User manager."""
        return self._users

    @property
    def projects(self) -> ProjectManager:
        """Project manager."""
        return self._projects

    @property
    def organizations(self) -> OrganizationManager:
        """Organization manager."""
        return self._organizations

    @property
    def runs(self) -> RunManager:
        """Run manager."""
        return self._runs

    @property
    def models(self) -> ModelManager:
        """Model manager."""
        return self._models

    @property
    def model_versions(self) -> ModelVersionManager:
        """Model version manager."""
        return self._model_versions

    @property
    def experiments(self) -> ExperimentManager:
        """Experiment manager."""
        return self._experiments

    @property
    def batch_predictions(self) -> BatchPredictionManager:
        """Batch prediction manager."""
        return self._batch_predictions

    @property
    def promotions(self) -> PromotionManager:
        """Promotion manager."""
        return self._promotions

    @property
    def datasets(self) -> DatasetManager:
        """Dataset manager."""
        return self._datasets

    @property
    def dataset_versions(self) -> DatasetVersionManager:
        """Dataset version manager."""
        return self._dataset_versions

    @property
    def data_profiles(self) -> DataProfilesManager:
        """Data profiles manager."""
        return self._data_profiles

    @property
    def assignments(self) -> DatasetVersionAssignmentManager:
        """Dataset version assignment manager."""
        return self._assignments

    @property
    def events(self) -> EventManager:
        """Event manager."""
        return self._events

    @property
    def metadata(self) -> MetadataManager:
        """Metadata manager."""
        return self._metadata

    @property
    def metrics(self) -> MetricsManager:
        """Metrics manager."""
        return self._metrics

    @property
    def tags(self) -> TagsManager:
        """Tags manager."""
        return self._tags

    @property
    def resource_checks(self) -> ResourceChecksManager:
        """Resource checks manager."""
        return self._resource_checks

    @property
    def artifacts(self) -> ArtifactsManager:
        """Artifact manager."""
        return self._artifacts

    @property
    def config(self) -> Config:
        """User manager."""
        return self._config

    def _init_managers(self):
        # Initialize managers.
        parent = self.config.environment
        if parent is None:
            parent = "projects/-"
        else:
            env = self.config.environment
            if (
                env == None
                or env == "master"
                or env == "main"
                or env == "production"
                or len(env) == 0
            ):
                env = "production"

            splits = self.config.environment.split("/")
            if (
                len(splits) != 4
                or splits[0] != "projects"
                or splits[2] != "environments"
            ):
                parent = f"{self.config.project}/environments/{self.config.environment}"

        self._runs = RunManager(client=self, parent=parent)
        self._models = ModelManager(client=self, parent=parent)
        self._model_versions = ModelVersionManager(client=self, parent=parent)
        self._experiments = ExperimentManager(client=self, parent=parent)
        self._batch_predictions = BatchPredictionManager(client=self, parent=parent)
        self._promotions = PromotionManager(client=self, parent=parent)
        self._datasets = DatasetManager(client=self, parent=parent)
        self._dataset_versions = DatasetVersionManager(client=self, parent=parent)
        self._data_profiles = DataProfilesManager(client=self, parent=parent)
        self._assignments = DatasetVersionAssignmentManager(client=self, parent=parent)
        self._events = EventManager(client=self, parent=parent)
        self._metadata = MetadataManager(client=self, parent=parent)
        self._metrics = MetricsManager(client=self, parent=parent)
        self._tags = TagsManager(client=self, parent=parent)
        self._resource_checks = ResourceChecksManager(client=self, parent=parent)
        self._artifacts = ArtifactsManager(client=self, parent=parent)

    def _init_grpc_connnections(self, api_key):
        """Init auth"""
        auth_interceptor = AuthInterceptor(lambda: api_key)
        self._mgmt_channel = get_management_channel(self.config.endpoint)

        self._mgmt_channel = grpc.intercept_channel(
            self._mgmt_channel, auth_interceptor
        )
        self._management = normalize_exceptions_for_class(
            management_pb2_grpc.ManagementAPIStub(self._mgmt_channel)
        )

    def _verify_api_key(self):
        """Verifies that the API key is valid by calling CheckViewer"""
        try:
            self.check_viewer()
        except Exception as e:
            api_key = self._mgmt_channel._interceptor.api_key_getter()
            raise Exception(f"Unable to verify API key {api_key}. {str(e)}")

    def set_config_api_key(self, api_key: str, save: bool = False) -> None:
        """Sets config API key.

        Arguments:
            api_key: The API key to set on this client.
            save: Whether to save the API key to the config file on disk.

        Examples:
            >>> from continual import Client
            >>> c = Client(verify=False)
            >>> c.config.api_key # If a YAML config is present in the OS env or filesystem this will not be empty
            ''
            >>> c.set_config_api_key(api_key='sessions/aJcVPD9Vh6q3ofYkuWyzQS', save=False)
            >>> c.config.api_key
            'sessions/aJcVPD9Vh6q3ofYkuWyzQS'

        """
        # Reinitalize Initialize GRPC connections.
        self._init_grpc_connnections(api_key=api_key)

        self._verify_api_key()
        # if api key is an api key and not a session, set project
        if api_key.startswith("apikey/"):
            api_key_project = self._api_key_project(api_key=api_key)
            # check api key project with configured project
            if (
                self.config.project != ""
                and self.config.project != api_key_project.name
            ):
                raise Exception(
                    f"\nERROR: apikey used is not valid for current configured project [{self.config.project}]\nview config with 'continual config show'\nclear config with 'continual config clear-all'"
                )
            self.config.set_project(project=api_key_project.name, save=save)

        self.config.set_api_key(api_key=api_key, save=save)

        # set environment to default
        if hasattr(self, "_projects"):
            if not self.config.environment:
                self.set_config_environment(environment="", save=save)
        else:
            if not self.config.environment:
                self.config._environment = ""

        # Reset managers
        self._init_managers()

    def _verify_project(self, project: str) -> str:
        # Verify project name and return fully qualified name
        try:
            for p in self.projects.list_all():
                if project == p.name or project.split("/")[-1] in {
                    p.id,
                    p.display_name,
                }:
                    return p.name

            raise Exception(
                f"Project '{project}' not found. Make sure to provide fully qualified project name or unique project ID."
            )
        except Exception as e:
            raise Exception(f"Unable to verify project '{project}'. {str(e)}")

    def set_config_project(
        self, project: str, save: bool = False, environment: str = None
    ) -> str:
        """Sets config project.

        Arguments:
            project: The project to set on this client.
            save: Whether to save the project to the config file on disk.

        Examples:
            >>> from continual import Client
            >>> c = Client(verify=False)
            >>> c.config.project # If a YAML config is present in the OS env or filesystem this will not be empty
            ''
            >>> c.set_config_project(project='example-project', save=False) # Attempt to verify that project exists, API key must be valid
            >>> c.config.project
            'example-project'
        """
        # Here ensure that if the API key is blank, you cannot set a project (you need to login first)
        if not self.config.api_key and project:
            raise Exception(
                f"API key is empty. Cannot set project '{project}' until client has valid API key."
            )

        project_name = self._verify_project(project=project)
        self.config.set_project(project=project_name, save=save)
        # set environment to default env
        self.set_config_environment(environment=environment, save=save)

        # Reset managers
        self._init_managers()

    def _verify_environment(self, project: str, environment: str) -> str:
        # Verify environment name after project is verified
        try:
            proj = self.projects.get(project)
            if environment == None or environment == "":
                if proj is None:
                    return ""
                environment = proj.default_environment
            env_identifier_to_verify = ProjectEnvironmentIdentifer(
                project_name_or_id=project, environment_name_or_id=environment
            )
            environment_names = [e.name for e in proj.environments.list_all()]
            if env_identifier_to_verify.environment_name not in environment_names:
                raise Exception(f"Environment '{environment}' not found.")

            return environment
        except Exception as e:
            raise Exception(f"Unable to verify environment '{environment}'. {str(e)}")

    def set_config_environment(self, environment: str, save: bool = False) -> None:
        """Sets config environment.

        Arguments:
            environment: The environment to set on this client.
            save: Whether to save the environment to the config file on disk.

        Examples:
            >>> from continual import Client
            >>> c = Client(verify=False)
            >>> c.config.environment # If a YAML config is present in the OS env or filesystem this will not be empty
            ''
            >>> c.set_config_environment(environment='example-env', save=False) # Attempts to verify that environment exists, API key and project must be valid
            >>> c.config.environment
            'example-env'
        """

        environment = self._verify_environment(
            project=self.config.project, environment=environment
        )
        self.config.set_environment(environment=environment, save=save)

        # Reset managers
        self._init_managers()

    def __del__(self) -> None:
        if hasattr(self, "_mgmt_channel"):
            self._mgmt_channel.close()
        if hasattr(self, "_fs_channel"):
            self._fs_channel.close()
        if hasattr(self, "_gw_channel"):
            self._gw_channel.close()

    def viewer(self) -> User:
        """Currently authenticated user."""
        resp = self._management.GetViewer(Empty())
        return User.from_proto(resp, client=self)

    def check_viewer(self) -> None:
        """Verify if client's user is authenticated."""
        self._management.CheckViewer(Empty())

    def _api_key_project(self, api_key: str) -> Project:
        """Get project associated with the API key."""
        req = management_pb2.GetApiKeyProjectRequest(name=api_key)
        resp = self._management.GetApiKeyProject(req)
        return Project.from_proto(resp, client=self)

    def register(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        save: bool = True,
    ) -> User:
        """Register a new account.

        This function registers and authenticates a new user
        and saves the authenticated user information in local config.

        Arguments:
            first_name: First name of user.
            last_name: Last name of user
            email: Email address.
            password: Password.
            save: Whether to persist API key to config file

        Returns:
            The newly created authenticated user.

        Examples:
            >>> from continual import Client
            >>> client = Client(verify=False)
            >>> client.register(first_name='test', last_name='user', email='test@continual.ai', password='test123')
            <User object {'name': 'users/zxNbTXkbxLeyjb3SUhJ2fR', 'email': 'test@continual.ai', 'email_verified': True,
            'full_name': 'test user', 'update_time': '2022-12-15T01:00:20.707583Z', 'create_time': '2022-12-15T01:00:20.707583Z',
            'trial_available': True, 'first_name': 'test', 'last_name': 'user', 'bio': '', 'location': '', 'password': '',
            'service_account': False, 'disabled': False}>
            >>> client.config.show()
            Config Files:
            ${HOME}/continual/continual.yaml
            ${HOME}/continual/.continual.yaml
            Email: test@continual.ai
            Endpoint: http://sdk.continual.ai
            Project:
            Environment:
            Style: GREEN
            Raise Exception: True
            Debug:
            API Key: *******************************
        """
        req = management_pb2.RegisterRequest(
            first_name=first_name, last_name=last_name, email=email, password=password
        )
        resp = self._management.Register(req)

        # No need to reverify API key in response
        self.config.set_api_key(resp.auth_token, save=save)
        self._init_grpc_connnections(self.config.api_key)
        self.config._email = email
        return User.from_proto(resp.user, client=self)

    def login(self, email: str, password: str, save: bool = True) -> User:
        """Login to Continual.

        It is strongly recommended to use `continual login` CLI
        or an API key instead of logging in via the SDK.

        Args:
            email: Email address.
            password: Password.
            save: Whether to persist API key to config file
        Returns:
            The authenticated user.

        Examples:
            >>> from continual import Client
            >>> client = Client(verify=False)
            >>> client.login(email='test@continual.ai', password='test123') # Assuming user is already registered
            <User object {'name': 'users/zxNbTXkbxLeyjb3SUhJ2fR', 'email': 'test@continual.ai', 'email_verified': True,
            'full_name': 'test user', 'update_time': '2022-12-15T01:00:20.707583Z', 'create_time': '2022-12-15T01:00:20.707583Z',
            'trial_available': True, 'first_name': 'test', 'last_name': 'user', 'bio': '', 'location': '', 'password': '',
            'service_account': False, 'disabled': False}>
            >>> client.config.show()
            Config Files:
            ${HOME}/continual/continual.yaml
            ${HOME}/continual/.continual.yaml
            Email: test@continual.ai
            Endpoint: http://sdk.continual.ai
            Project:
            Environment:
            Style: GREEN
            Raise Exception: True
            Debug:
            API Key: *******************************
        """
        req = management_pb2.LoginRequest(email=email, password=password)
        resp = self._management.Login(req)

        # No need to reverify API key in response
        self.config.set_api_key(resp.auth_token, save=save)
        self._init_grpc_connnections(self.config.api_key)
        self.config._email = email
        return User.from_proto(resp.user, client=self)

    def logout(self) -> None:
        """Logout.

        Logs out current session deleting the associated API key.
        """
        if self.config.api_key is not None and self.config.api_key != "":
            self._management.Logout(Empty())
            self.config.set_api_key(api_key=None)
            self.config._email = None
            self.config.save()

    def version(self) -> Tuple[str, str, bool]:
        """Get the current server version.

        Returns:
          A tuple of the client version string, server version string, and a boolean
          true if client needs an update.
        """
        client_version = __version__
        req = management_pb2.GetServerVersionRequest(client_version=client_version)
        resp = self._management.GetServerVersion(req)
        return client_version, resp.server_version, resp.upgrade_required
