from __future__ import annotations

import urllib.parse

from vectice.api.http_error_handlers import InvalidReferenceError, MissingReferenceError
from vectice.api.json import PagedResponse, ProjectInput, ProjectOutput
from vectice.api.rest_api import HttpError, RestApi
from vectice.api.workspace import WorkspaceApi

INVALID_PROJECT_MESSAGE = "The project is invalid. Please check the entered value."


class ProjectApi(RestApi):
    def create_project(self, data: ProjectInput, workspace: str | int) -> ProjectOutput:
        if isinstance(workspace, int):
            url = f"/metadata/workspace/{workspace}/project"
        elif isinstance(workspace, str):
            parent_workspace = WorkspaceApi(self.auth).get_workspace(workspace)
            url = f"/metadata/workspace/{parent_workspace.id}/project"
        else:
            raise InvalidReferenceError("workspace", workspace)
        try:
            response = self.post(url, data)
            return ProjectOutput(**response)
        except HttpError as e:
            raise self._httpErrorHandler.handle_post_http_error(e, "project")
        except IndexError:
            raise ValueError(INVALID_PROJECT_MESSAGE)

    def delete_project(self, project: str | int, workspace: str | int | None = None):
        project_output = self.get_project(project, workspace)
        url = f"/metadata/project/{project_output.id}"
        try:
            response = self.delete(url)
            return ProjectOutput(**response)
        except HttpError as e:
            raise self._httpErrorHandler.handle_delete_http_error(e, "project", project)
        except IndexError:
            raise ValueError(INVALID_PROJECT_MESSAGE)

    def get_project(self, project: str | int, workspace: str | int | None = None) -> ProjectOutput:
        parent_workspace = None
        if isinstance(project, int):
            url = f"/metadata/project/{project}"
        elif isinstance(project, str):
            if workspace is None:
                raise MissingReferenceError("workspace")
            parent_workspace = WorkspaceApi(self.auth).get_workspace(workspace)
            url = f"/metadata/workspace/{parent_workspace.id}/project/name/{urllib.parse.quote(project, safe='')}"
        else:
            raise InvalidReferenceError("project", project)
        try:
            response = self.get(url)
            project_output = ProjectOutput(**response)
            if parent_workspace:
                project_output._workspace = parent_workspace
            return project_output
        except HttpError as e:
            raise self._httpErrorHandler.handle_get_http_error(e, "project", project)
        except IndexError:
            raise ValueError(INVALID_PROJECT_MESSAGE)

    def update_project(self, data: ProjectInput, project: str | int, workspace: str | int) -> ProjectOutput:
        if isinstance(workspace, int):
            base_url = f"/metadata/workspace/{workspace}/project"
        elif isinstance(workspace, str):
            base_url = f"/metadata/workspace/name/{urllib.parse.quote(workspace, safe='')}/project"
        else:
            raise InvalidReferenceError("workspace", workspace)
        if isinstance(project, int):
            url = f"/metadata/project/{project}"
        elif isinstance(project, str):
            url = f"{base_url}/name/{urllib.parse.quote(project, safe='')}"
        else:
            raise InvalidReferenceError("project", project)
        try:
            response = self.put(url, data)
            return ProjectOutput(**response)
        except HttpError as e:
            raise self._httpErrorHandler.handle_put_http_error(e, "project", project)
        except IndexError:
            raise ValueError(INVALID_PROJECT_MESSAGE)

    def list_projects(
        self,
        workspace: str | int,
        search: str | None = None,
        page_index: int | None = 1,
        page_size: int | None = 20,
    ) -> PagedResponse[ProjectOutput]:
        if isinstance(workspace, int):
            url = f"/metadata/workspace/project?index={page_index}&size={page_size}&workspaceId={workspace}"
        elif isinstance(workspace, str):
            url = f"/metadata/workspace/project?index={page_index}&size={page_size}&workspaceName={workspace}"
        else:
            raise InvalidReferenceError("workspace", workspace)
        if search:
            url = url + f"&search={search}"
        projects = self.get(url)
        return PagedResponse(
            item_cls=ProjectOutput, total=projects["total"], page=projects["page"], items=projects["items"]
        )
