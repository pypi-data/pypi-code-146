from __future__ import annotations

import logging
from datetime import datetime
from typing import BinaryIO, TYPE_CHECKING

from gql import Client as GQLClient
from gql.transport.requests import RequestsHTTPTransport

from vectice.__version__ import __version__
from vectice.api._auth import Auth
from vectice.api.attachment import AttachmentApi
from vectice.api.compatibility import CompatibilityApi
from vectice.api.gql_code import GqlCodeApi
from vectice.api.gql_code_version import GqlCodeVersionApi
from vectice.api.gql_dataset import GqlDatasetApi
from vectice.api.gql_model import GqlModelApi
from vectice.api.http_error_handlers import MissingReferenceError, StepIdError, StepNameError
from vectice.api.iteration import IterationApi
from vectice.api.version import VersionApi
from vectice.api.json import (
    CodeInput,
    CodeVersionCreateBody,
    ModelRegisterInput,
    ModelRegisterOutput,
    ModelType,
    ModelVersionStatus,
    ModelVersionOutput,
    Page,
    PagedResponse,
    ProjectInput,
    PropertyInput,
    StepOutput,
    ArtifactName,
)
from vectice.api.json.dataset_register import DatasetRegisterInput, DatasetRegisterOutput
from vectice.api.json.metric import MetricInput
from vectice.api.json.step import StepUpdateInput
from vectice.api.last_assets import LastAssetApi
from vectice.api.phase import PhaseApi
from vectice.api.project import ProjectApi
from vectice.api.step import StepApi
from vectice.api.workspace import WorkspaceApi

if TYPE_CHECKING:
    from io import BytesIO

    from vectice.api.json import AttachmentOutput, ProjectOutput, WorkspaceOutput
    from vectice.api.json.compatibility import CompatibilityOutput
    from vectice.api.json.iteration import IterationInput, IterationOutput, IterationStepArtifactInput
    from vectice.api.json.phase import PhaseOutput
    from vectice.api.json.workspace import WorkspaceInput
    from vectice.models.datasource.datawrapper import DataWrapper
    from vectice.models.datasource.datawrapper.metadata import SourceUsage
    from vectice.models.model import Model


_logger = logging.getLogger(__name__)


class Client:
    """
    Low level Vectice API client.
    """

    def __init__(
        self,
        workspace: str | int | None = None,
        project: str | int | None = None,
        token: str | None = None,
        api_endpoint: str | None = None,
        auto_connect=True,
        allow_self_certificate=True,
    ):
        self.auth = Auth(
            api_endpoint=api_endpoint,
            api_token=token,
            auto_connect=auto_connect,
            allow_self_certificate=allow_self_certificate,
        )
        transport = RequestsHTTPTransport(url=self.auth.api_base_url + "/graphql", verify=self.auth.verify_certificate)
        logging.getLogger("gql.transport.requests").setLevel("WARNING")
        self._gql_client = GQLClient(transport=transport)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._workspace = None
        self._project = None
        if auto_connect and workspace is not None:
            if isinstance(project, int):
                self._project = self.get_project(project)
                self._workspace = self._project.workspace
                if workspace is not None:
                    if isinstance(workspace, str):
                        if workspace != self._workspace.name:
                            raise ValueError(
                                f"Inconsistency in configuration: project {project} does not belong to workspace {workspace}"
                            )
                    else:
                        if workspace != self._workspace.id:
                            raise ValueError(
                                f"Inconsistency in configuration: project {project} does not belong to workspace {workspace}"
                            )
                _logger.info(
                    f"Successfully authenticated. You'll be working on Project: {self._project.name} part of Workspace: {self._workspace.name}"
                )
            else:
                self._workspace = self.get_workspace(workspace)
                if project is not None:
                    self._project = self.get_project(project, workspace)
                    _logger.info(
                        f"Successfully authenticated. You'll be working on Project: {self._project.name} part of Workspace: {self._workspace.name}"
                    )
                else:
                    _logger.info(f"Your current workspace: {self._workspace.name}")
        elif auto_connect and workspace is None and project:
            self._project = self.get_project(project)
            if self._project is not None:
                self._workspace = self._project.workspace
            _logger.info(
                f"Successfully authenticated. You'll be working on Project: {self._project.name} part of Workspace: {self._workspace.name}"
            )

    @property
    def workspace(self) -> WorkspaceOutput | None:
        """
        The workspace object.
        :return: WorkspaceOutput
        """
        return self._workspace

    @property
    def project(self) -> ProjectOutput | None:
        """
        The project object.
        :return: ProjectOutput
        """
        return self._project

    @property
    def version_api(self) -> str:
        return __version__

    @property
    def version_backend(self) -> str:
        versions = VersionApi(self._gql_client, self.auth).get_public_config().versions
        for version in versions:
            if version.artifact_name == ArtifactName.BACKEND:
                return version.version
        raise ValueError("No version found for backend.")

    def check_compatibility(self) -> CompatibilityOutput:
        return CompatibilityApi(self.auth).check_version()

    def create_project(self, data: ProjectInput, workspace: str | int) -> ProjectOutput:
        """
         Creates a project.

        :param data: The ProjectInput json structure
        :param workspace: The workspace name or id

        :return: The ProjectOutput json structure
        """
        result = ProjectApi(self.auth).create_project(data, workspace)
        _logger.info(f"Project with id: {result.id} successfully created.")
        return result

    def delete_project(self, project: str | int, workspace: str | int | None = None):
        """
         Deletes a project.

        :param project: The project name or id
        :param workspace: The workspace name or id

        :return: None
        """
        ProjectApi(self.auth).delete_project(project, workspace)

    def update_project(self, data: ProjectInput, project: str | int, workspace: str | int) -> ProjectOutput:
        """
        Updates a project.

        :param data: The ProjectInput json structure
        :param project: The project name or id
        :param workspace: The workspace name or id

        :return: The ProjectOutput json structure
        """
        return ProjectApi(self.auth).update_project(data, project, workspace)

    def list_projects(
        self,
        workspace: str | int,
        search: str | None = None,
        page_index: int | None = Page.index,
        page_size: int | None = Page.size,
    ) -> PagedResponse[ProjectOutput]:
        """
        Lists the projects in a workspace.

        :param workspace: The workspace name or id
        :param search: A text to search for
        :param page_index: The index of the page
        :param page_size: The size of the page

        :return: PagedResponse[ProjectOutput]
        """
        return ProjectApi(self.auth).list_projects(workspace, search, page_index, page_size)

    def get_project(self, project: str | int, workspace: str | int | None = None) -> ProjectOutput:
        """
        Gets a project.

        :param project: The project name or id
        :param workspace: The workspace name or id

        :return: The ProjectOutput json structure
        """
        return ProjectApi(self.auth).get_project(project, workspace)

    def get_workspace(self, workspace: str | int) -> WorkspaceOutput:
        """
        Gets a workspace.

        :param workspace: The workspace name or id

        :return: The WorkspaceOutput json structure
        """
        return WorkspaceApi(self.auth).get_workspace(workspace)

    def create_workspace(self, data: WorkspaceInput) -> WorkspaceOutput:
        """
        Creates a workspace.

        :param data: The WorkspaceInput json structure

        :return: The WorkspaceOutput json structure
        """
        result = WorkspaceApi(self.auth).create_workspace(data)
        return result

    def update_workspace(self, data: WorkspaceInput, workspace: str | int) -> WorkspaceOutput:
        """
        Updates a workspace.

        :param data: The WorkspaceInput json structure
        :param workspace: The workspace name or id

        :return: The WorkspaceOutput json structure
        """
        return WorkspaceApi(self.auth).update_workspace(data, workspace)

    def list_workspaces(
        self, search: str | None = None, page_index: int = 1, page_size: int = 20
    ) -> PagedResponse[WorkspaceOutput]:
        """
        Lists the workspaces.

        :param search: A text to search for
        :param page_index: The index of the page
        :param page_size: The size of the page

        :return: PagedResponse[WorkspaceOutput]
        """
        return WorkspaceApi(self.auth).list_workspaces(search, page_index, page_size)

    def create_model_attachments(
        self, files: list[tuple[str, tuple[str, BinaryIO]]], model_version: ModelVersionOutput
    ):
        """
        Creates an attachment

        :param files: The paths to the files to attach
        :param model_version: The model version to attach files to

        :return: The json structure
        """
        return AttachmentApi(self.auth).post_attachment(files, model_version)

    def create_model_predictor(self, model_type: str, model_content: BytesIO, model_version: ModelVersionOutput):
        """
        Creates an attachment

        :param model_type: The type of model to attach
        :param model_content: The binary content of the model
        :param model_version: The model version to attach files to

        :return: The json structure
        """
        return AttachmentApi(self.auth).post_model_predictor(model_type, model_content, model_version)

    def list_attachments(self, model_version: ModelVersionOutput) -> PagedResponse[AttachmentOutput]:
        """
        Lists the attachments of an artifact.

        :param model_version: The model version to list attachments from

        :return: PagedResponse[AttachmentOutput]
        """
        return AttachmentApi(self.auth).list_attachments(model_version)

    def list_phases(
        self,
        search: str | None = None,
        project: str | int | None = None,
        workspace: str | int | None = None,
    ) -> list[PhaseOutput]:
        project, workspace = self.get_project_and_workspace_references_or_raise_error(project, workspace)
        project_object = self.get_project(project, workspace)
        return PhaseApi(self._gql_client, self.auth).list_phases(project_object.id, search)

    def get_phase(self, phase: str | int, project_id: int | None = None) -> PhaseOutput:
        if project_id is None:
            raise MissingReferenceError("project")
        return PhaseApi(self._gql_client, self.auth).get_phase(phase, project_id)

    def get_step(self, step_reference: str | int, phase_id: int) -> StepOutput:
        if phase_id is None:
            raise MissingReferenceError("iteration")
        steps = self.list_steps(phase_id)
        if isinstance(step_reference, int):
            for step in steps:
                if step.id == step_reference:
                    return step
            raise StepIdError(step_reference)
        elif isinstance(step_reference, str):
            for step in steps:
                if step.name == step_reference:
                    return step
            raise StepNameError(step_reference)
        raise ValueError(f"No such step reference '{step_reference}' exists in the phase '{phase_id}'")

    def get_step_by_name(self, step_reference: str, phase_id: int) -> StepOutput:
        return StepApi(self._gql_client, self.auth).get_step(step_reference, phase_id)

    def list_steps(
        self,
        phase_id: int,
        iteration_index: int | None = None,
        phase_name: str | None = None,
    ) -> list[StepOutput]:
        if iteration_index:
            return StepApi(self._gql_client, self.auth).list_steps_for_iteration(phase_id, iteration_index, phase_name)
        return StepApi(self._gql_client, self.auth).list_steps(phase_id, phase_name)

    def close_step(self, step_id: int, message: str | None = None) -> StepOutput:
        step_update = StepUpdateInput(text=message)
        return StepApi(self._gql_client, self.auth).close_step(step_id, step_update)

    def add_iteration_step_artifact(self, step_id: int, step_artifacts: IterationStepArtifactInput) -> StepOutput:
        return StepApi(self._gql_client, self.auth).add_iteration_step_artifact(step_artifacts, step_id)

    def list_iterations(self, phase: int) -> list[IterationOutput]:
        return IterationApi(self._gql_client, self.auth).list_iterations(phase)

    def get_iteration(self, iteration_id: int) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_iteration(iteration_id)

    def get_iteration_by_index(self, phase_id: int, index: int) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_iteration_by_index(phase_id, index)

    def get_iteration_last_assets(self, iteration_id: int) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_iteration_last_assets(iteration_id)

    def get_or_create_iteration(self, phase_id: int) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_or_create_iteration(phase_id)

    def update_iteration(self, iteration_id: int, iteration: IterationInput) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).update_iteration(iteration, iteration_id)

    def register_dataset_from_source(
        self,
        data_source: DataWrapper,
        source_usage: SourceUsage,
        project_id: int | None = None,
        phase_id: int | None = None,
        iteration_id: int | None = None,
        code_version_id: int | None = None,
    ) -> DatasetRegisterOutput:
        name = self.get_dataset_name(data_source)
        inputs = self.get_dataset_inputs(data_source)
        metadata_asdict = data_source.metadata.asdict()

        dataset_register_input = DatasetRegisterInput(
            name=name,
            type=source_usage.value,
            datasetSources=metadata_asdict,
            inputs=inputs,
            codeVersionId=code_version_id,
        )
        return self.register_dataset(dataset_register_input, project_id, phase_id, iteration_id)

    @staticmethod
    def get_dataset_name(data_source: DataWrapper) -> str:
        return f"dataset {datetime.time}" if data_source.name is None else data_source.name

    @staticmethod
    def get_dataset_inputs(data_source: DataWrapper) -> list[int]:
        return [] if data_source.inputs is None else data_source.inputs

    def register_dataset(
        self,
        dataset_register_input: DatasetRegisterInput,
        project_id: int | None = None,
        phase_id: int | None = None,
        iteration_id: int | None = None,
    ) -> DatasetRegisterOutput:
        try:
            data: DatasetRegisterOutput = GqlDatasetApi(self._gql_client, self.auth).register_dataset(
                dataset_register_input, project_id, phase_id, iteration_id
            )
            _logger.info(
                f"Successfully registered Dataset("
                f"name='{dataset_register_input.name}', "
                f"id={data['datasetVersion']['id']}, "
                f"version='{data['datasetVersion']['name']}', "
                f"type={dataset_register_input.type})."
            )
            return data
        except Exception as e:
            raise ValueError(f"The dataset register failed due to {e}")

    def get_project_and_workspace_references(
        self, project: str | int | None = None, workspace: str | int | None = None
    ):
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return project, workspace

    def get_project_and_workspace_refs_if_project_ref_is_str(
        self, project: str | int | None = None, workspace: str | int | None = None
    ):
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return project, workspace

    def get_project_and_workspace_refs_if_project_ref_is_str_or_raise_error(
        self, project: str | int | None = None, workspace: str | int | None = None
    ) -> tuple[str | int, str | int | None]:
        project, workspace = self.get_project_and_workspace_refs_if_project_ref_is_str(project, workspace)
        if project is None:
            raise MissingReferenceError("project")
        return project, workspace

    def get_project_and_workspace_references_or_raise_error(
        self, project: str | int | None = None, workspace: str | int | None = None
    ) -> tuple[str | int, str | int | None]:
        project, workspace = self.get_project_and_workspace_references(project, workspace)
        if project is None:
            raise MissingReferenceError("project")
        return project, workspace

    @staticmethod
    def _get_model_name(library: str, technique: str, name: str | None = None) -> str:
        return name if name else f"{library} {technique} model"

    def register_model(
        self,
        model: Model,
        project_id: int,
        phase_id: int | None = None,
        iteration_id: int | None = None,
        code_version_id: int | None = None,
        inputs: list[int] | None = None,
    ) -> ModelRegisterOutput:
        metrics = [vars(MetricInput(metric.key, metric.value)) for metric in model.metrics] if model.metrics else None
        properties = (
            [vars(PropertyInput(prop.key, prop.value)) for prop in model.properties] if model.properties else None
        )
        model_register_input = ModelRegisterInput(
            name=model.name,
            modelType=ModelType.OTHER.value,
            status=ModelVersionStatus.EXPERIMENTATION.value,
            inputs=inputs if inputs else [],
            metrics=metrics,
            properties=properties,
            algorithmName=model.technique,
            framework=model.library,
            codeVersionId=code_version_id,
        )
        return GqlModelApi(self._gql_client, self.auth).register_model(
            model_register_input, project_id, phase_id, iteration_id
        )

    def get_last_assets(self, target_types: list[str], page):
        return LastAssetApi(self._gql_client, self.auth).get_last_assets(target_types, page)

    def create_code_gql(self, project_id: int, code: CodeInput):
        return GqlCodeApi(self._gql_client, self.auth).create_code(project_id, code)

    def create_code_version_gql(self, code_id: int, code_version: CodeVersionCreateBody):
        return GqlCodeVersionApi(self._gql_client, self.auth).create_code_version(code_id, code_version)

    def get_code(self, code: str | int, project_id: int | None = None):
        if project_id is None:
            raise MissingReferenceError("project")
        return GqlCodeApi(self._gql_client, self.auth).get_code(code, project_id)

    def get_code_version(self, code_version: str | int, code_id: int | None = None):
        if code_id is None:
            raise MissingReferenceError("code")
        return GqlCodeVersionApi(self._gql_client, self.auth).get_code_version(code_version, code_id)
