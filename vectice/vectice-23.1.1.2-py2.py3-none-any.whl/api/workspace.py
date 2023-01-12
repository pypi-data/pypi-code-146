from __future__ import annotations

import urllib.parse
from typing import TYPE_CHECKING

from vectice.api.http_error_handlers import InvalidReferenceError
from vectice.api.json import PagedResponse, WorkspaceOutput
from vectice.api.rest_api import HttpError, RestApi

if TYPE_CHECKING:
    from vectice.api.json.workspace import WorkspaceInput


INVALID_WORKSPACE_MESSAGE = "The workspace is invalid. Please check the entered value."


class WorkspaceApi(RestApi):
    def get_workspace(self, workspace: str | int) -> WorkspaceOutput:
        if isinstance(workspace, int):
            url = f"/metadata/workspace/{workspace}"
        elif isinstance(workspace, str):
            url = f"/metadata/workspace/name/{urllib.parse.quote(workspace, safe='')}"
        else:
            raise InvalidReferenceError("workspace", workspace)
        try:
            response = self.get(url)
            return WorkspaceOutput(**response)
        except HttpError as e:
            raise self._httpErrorHandler.handle_get_http_error(e, "workspace", workspace)
        except TypeError:
            raise ValueError(INVALID_WORKSPACE_MESSAGE)

    def list_workspaces(
        self, search: str | None = None, page_index: int = 1, page_size: int = 20
    ) -> PagedResponse[WorkspaceOutput]:
        if search is None or search == "":
            url = f"/metadata/workspace?index={page_index}&size={page_size}"
        else:
            url = f"/metadata/workspace?index={page_index}&size={page_size}&search={search}"
        workspaces = self.get(url)
        return PagedResponse(
            item_cls=WorkspaceOutput, total=workspaces["total"], page=workspaces["page"], items=workspaces["items"]
        )

    def create_workspace(self, data: WorkspaceInput) -> WorkspaceOutput:
        url = "/metadata/workspace"
        try:
            response = self.post(url, data.__dict__)
            return WorkspaceOutput(**response)
        except HttpError as e:
            raise self._httpErrorHandler.handle_post_http_error(e, "workspace")
        except TypeError:
            raise ValueError(INVALID_WORKSPACE_MESSAGE)

    def update_workspace(self, data: WorkspaceInput, workspace: str | int) -> WorkspaceOutput:
        if isinstance(workspace, int):
            url = f"/metadata/workspace/{workspace}"
        elif isinstance(workspace, str):
            workspace_object = self.get_workspace(workspace)
            url = f"/metadata/workspace/{workspace_object.id}"
        else:
            raise InvalidReferenceError("workspace", workspace)
        try:
            response = self.put(url, data)
            return WorkspaceOutput(**response)
        except HttpError as e:
            raise self._httpErrorHandler.handle_put_http_error(e, "workspace", workspace)
        except TypeError:
            raise ValueError(INVALID_WORKSPACE_MESSAGE)
