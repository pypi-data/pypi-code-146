from typing import List

from bodosdk.api.base import BackendApi
from bodosdk.exc import (
    ResourceNotFound,
    ServiceUnavailable,
    UnknownError,
    ValidationError,
)
from bodosdk.models.job import (
    JobDefinition,
    JobResponse,
    JobExecution,
    JobCreateResponse,
)


class JobApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(JobApi, self).__init__(*args, **kwargs)
        self._resource_url = "job"

    def create_job(self, job_definition: JobDefinition) -> JobCreateResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            self.get_resource_url("v2"),
            data=job_definition.json(by_alias=True),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            # remap list of variables to dict
            json_data = resp.json()
            if isinstance(json_data["variables"], list):
                json_data["variables"] = {
                    k[0].strip(): k[1].strip()
                    for k in (item.split("=", 1) for item in json_data["variables"])
                }
            return JobCreateResponse(**json_data)
        if resp.status_code == 404:
            raise ResourceNotFound("Probably wrong workspace keys")
        if resp.status_code in (400, 422):
            raise ValidationError(resp.json())
        if resp.status_code == 503:
            raise ServiceUnavailable
        if resp.status_code == 409:
            raise ServiceUnavailable(
                "There is probably a job running on the cluster. \
                Please wait for the existing job to finish and retry again later."
            )
        raise UnknownError

    def delete_job(self, job_uuid) -> None:
        headers = self.get_auth_header()
        resp = self._requests.delete(
            f"{self.get_resource_url()}/{job_uuid}", headers=headers
        )
        if resp.status_code == 200:
            return
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    def list_jobs(self) -> List[JobResponse]:
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}?withTasks=false", headers=headers
        )
        if resp.status_code == 503:
            raise ServiceUnavailable
        result = []
        for json_data in resp.json():
            # remap list of variables to dict
            if isinstance(json_data["variables"], list):
                json_data["variables"] = {
                    k[0]: k[1]
                    for k in (item.split("=", 1) for item in json_data["variables"])
                }
            result.append(JobResponse(**json_data))
        return result

    def get_job(self, uuid) -> JobResponse:
        headers = self.get_auth_header()
        resp = self._requests.get(f"{self.get_resource_url()}/{uuid}", headers=headers)
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        json_data = resp.json()
        if isinstance(json_data["variables"], list):
            # remap list of variables to dict
            json_data["variables"] = {
                k[0]: k[1]
                for k in (item.split("=", 1) for item in json_data["variables"])
            }
        return JobResponse(**json_data)

    def get_tasks(self, uuid) -> List[JobExecution]:
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}/{uuid}/tasks", headers=headers
        )
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        return [JobExecution(**data) for data in resp.json()]
