import time
from typing import Type, TypeVar

import httpx

from pytailor.clients.auth import TailorAuth
from pytailor.clients.handling import (
    handle_retry,
    handle_exception,
    handle_wait_retry,
    handle_waited_for,
)
from pytailor.config import (
    API_BASE_URL,
    SYNC_REQUEST_TIMEOUT,
    SYNC_CONNECT_TIMEOUT,
    REQUEST_RETRY_COUNT,
    WAIT_RETRY_COUNT,
)
from pytailor.models import *

T = TypeVar("T")


class RestClient(httpx.Client):
    def __init__(self):
        timeout = httpx.Timeout(timeout=SYNC_REQUEST_TIMEOUT, connect=SYNC_CONNECT_TIMEOUT)
        super().__init__(base_url=API_BASE_URL, auth=TailorAuth(), timeout=timeout)

    def __handle_request(
        self,
        method: str,
        url: str,
        request_data: Optional[BaseModel] = None,
        response_model: Optional[Type[T]] = None,
        return_none_on: Optional[List[httpx.codes]] = None,
        error_msg: str = "Error.",
        wait: bool = False,
        **kwargs,
    ) -> Optional[Union[httpx.Response, T, List[T]]]:

        if request_data:
            kwargs["data"] = request_data.json()

        if return_none_on is None:
            return_none_on = []

        try:
            no_of_error_retries = 0
            no_of_wait_retries = 0
            while True:
                try:
                    result = self.__make_request(method, url, response_model, **kwargs)

                    if wait:
                        retry, no_of_wait_retries, sleep_time = handle_wait_retry(result, no_of_wait_retries)
                        if retry and no_of_wait_retries < WAIT_RETRY_COUNT:
                            # set method and url for subsequent calls
                            method = "get"
                            url = f"tasks/results/{result.processing_id}"
                        else:
                            return handle_waited_for(result)  # may raise BackendResponseError, which will NOT cause
                    else:  # error retry, and will hence be re-raised below
                        return result

                except Exception as exc:
                    retry, no_of_error_retries, sleep_time = handle_retry(exc, no_of_error_retries)
                    if not (retry and no_of_error_retries < REQUEST_RETRY_COUNT):
                        raise
                time.sleep(sleep_time)

        except Exception as exc:
            handle_exception(exc, return_none_on, error_msg)

    def __make_request(
        self, method: str, url: str, response_model: Optional[Type[T]] = None, **kwargs
    ) -> Optional[Union[httpx.Response, T, List[T]]]:
        response = self.request(method, url, **kwargs)
        if response.status_code == httpx.codes.OK:
            if response_model:
                return self.__parse_data(response, response_model)
            else:
                return response
        else:
            response.raise_for_status()

    @staticmethod
    def __parse_data(response: httpx.Response, response_model: Type[T]) -> Union[T, List[T]]:
        parsed = response.json()
        if isinstance(parsed, list) and response_model is not PermissionList:
            return [response_model.parse_obj(obj) for obj in parsed]
        else:
            return response_model.parse_obj(parsed)

    # accounts

    def get_accounts(self) -> List[Account]:
        url = "accounts"
        return self.__handle_request(
            "get",
            url,
            response_model=Account,
            error_msg=f"Error while fetching accounts.",
        )

    # projects

    def get_projects(self) -> List[Project]:
        url = "projects"
        return self.__handle_request(
            "get",
            url,
            response_model=Project,
            error_msg=f"Error while fetching projects.",
        )

    def get_project(self, project_id: str) -> Project:
        url = f"projects/{project_id}"
        return self.__handle_request(
            "get",
            url,
            response_model=Project,
            error_msg=f"Could not find project with id {project_id}.",
        )

    # filesets

    def new_fileset(self, project_id: str) -> FileSet:
        url = f"projects/{project_id}/filesets"
        return self.__handle_request(
            "post",
            url,
            response_model=FileSet,
            error_msg="An error occurred during fileset creation.",
        )

    def get_download_urls(self, project_id: str, fileset_id: str, fileset_download: FileSetDownload) -> FileSet:
        url = f"projects/{project_id}/filesets/{fileset_id}/downloads"
        return self.__handle_request(
            "post",
            url,
            request_data=fileset_download,
            response_model=FileSet,
            error_msg=f"Could not retrieve fileset with id {fileset_id}",
        )

    def get_download_urls_from_wf_id(self, project_id: str, wf_id: str, fileset_download: FileSetDownload) -> FileSet:
        url = f"projects/{project_id}/workflows/{wf_id}/downloads"
        return self.__handle_request(
            "post",
            url,
            request_data=fileset_download,
            response_model=FileSet,
            error_msg=f"Could not retrieve fileset for workflow with id {wf_id}",
        )

    def get_upload_urls(self, project_id: str, fileset_id: str, fileset_upload: FileSetUpload) -> FileSet:
        url = f"projects/{project_id}/filesets/{fileset_id}/uploads"
        return self.__handle_request(
            "post",
            url,
            request_data=fileset_upload,
            response_model=FileSet,
            error_msg="Error while getting upload urls from the backend.",
        )

    # workflows

    def get_workflow(self, project_id: str, wf_id: str) -> Workflow:
        url = f"projects/{project_id}/workflows/{wf_id}"
        return self.__handle_request(
            "get",
            url,
            response_model=Workflow,
            error_msg="Could not retrieve workflow.",
        )

    def get_workflows(self, project_id: str) -> List[Workflow]:
        url = f"projects/{project_id}/workflows"
        return self.__handle_request(
            "get",
            url,
            response_model=Workflow,
            error_msg="Could not retrieve workflows.",
        )

    def new_workflow(self, project_id: str, create_data: WorkflowCreate) -> Workflow:
        url = f"projects/{project_id}/workflows"
        return self.__handle_request(
            "post",
            url,
            request_data=create_data,
            response_model=Workflow,
            error_msg="Could not create workflow.",
        )

    def delete_workflow(self, project_id: str, wf_id: str) -> Optional[httpx.Response]:
        url = f"projects/{project_id}/workflows/{wf_id}"
        return self.__handle_request(
            "delete",
            url,
            return_none_on=[httpx.codes.NOT_FOUND],
            error_msg="Could not delete workflow.",
        )

    # workflow definitions

    def get_workflow_definition_project(self, project_id: str, wf_def_id: str) -> WorkflowDefinition:
        url = f"projects/{project_id}/workflow_definitions/{wf_def_id}"
        return self.__handle_request(
            "get",
            url,
            response_model=WorkflowDefinition,
            error_msg="Error while fetching workflow definition.",
        )

    def get_workflow_definition_summaries_project(self, project_id: str) -> List[WorkflowDefinitionSummary]:
        url = f"projects/{project_id}/workflow_definitions"
        return self.__handle_request(
            "get",
            url,
            response_model=WorkflowDefinitionSummary,
            error_msg="Could not retrieve workflow definition summaries.",
        )

    def new_workflow_definition(self, account_id, create_data: WorkflowDefinitionCreate) -> WorkflowDefinition:
        url = f"accounts/{account_id}/workflow_definitions"
        return self.__handle_request(
            "post",
            url,
            request_data=create_data,
            response_model=WorkflowDefinition,
            error_msg="Could not add workflow definition to backend.",
        )

    def update_workflow_definitions_for_project(
        self, project_id: str, permission_change: PermissionChange
    ) -> PermissionList:
        url = f"/projects/{project_id}/permissions/workflow-definitions"
        return self.__handle_request(
            "post",
            url,
            request_data=permission_change,
            response_model=PermissionList,
            error_msg=f"Error while updating workflow definitions for project.",
        )

    # task checkout/checkin

    def checkout_task(self, checkout_query: TaskCheckout) -> TaskExecutionData:
        url = f"tasks/checkouts"
        return self.__handle_request(
            "post",
            url,
            request_data=checkout_query,
            response_model=TaskExecutionData,
            error_msg="Error during task checkout.",
            return_none_on=[httpx.codes.NOT_FOUND],
        )

    def checkin_task(self, task_update: TaskUpdate, wait: bool = False) -> TaskExecutionData:
        url = f"tasks/checkins"
        return self.__handle_request(
            "post",
            url,
            request_data=task_update,
            response_model=TaskExecutionData,
            error_msg="Could not check in task.",
            wait=wait,
        )

    def perform_task_operation(
        self, wf_id: str, project_id: str, task_id: str, task_operation: TaskOperation
    ) -> TaskSummary:
        url = f"projects/{project_id}/workflows/{wf_id}/tasks/{task_id}/operations"
        return self.__handle_request(
            "post",
            url,
            request_data=task_operation,
            response_model=TaskSummary,
            error_msg=f"Could not perform operation {task_operation.type.name} for task " f"{task_id}",
        )

    def get_task_result(self, processing_id: str) -> TaskExecutionData:
        url = f"tasks/results/{processing_id}"
        return self.__handle_request(
            "get",
            url,
            response_model=TaskExecutionData,
            error_msg="Could not get operation result from backend.",
        )

    def get_task(self, project_id: str, wf_id: str, task_id: str) -> Task:
        url = f"projects/{project_id}/workflows/{wf_id}/tasks/{task_id}"
        return self.__handle_request(
            "get",
            url,
            response_model=Task,
            error_msg="Could not retrieve task.",
        )
