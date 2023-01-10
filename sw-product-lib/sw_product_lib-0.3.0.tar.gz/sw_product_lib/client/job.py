from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from sw_product_lib.client.platform import API, Operation
from sw_product_lib.errors.error import StrangeworksError


@dataclass
class Job:
    id: str
    child_jobs: Optional[List]
    external_identifier: Optional[str]
    slug: Optional[str]
    resource: Optional[Dict[str, Any]]
    status: Optional[str]
    is_terminal_state: Optional[str]
    remote_status: Optional[str] = None
    job_data_schema: Optional[str] = None
    job_data: Optional[Dict[str, Any]] = None

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(res: dict):
        child_jobs: List[Job] = []
        if "childJobs" in res:
            for _, child_job in res["childJobs"]:
                child_jobs.append(Job.from_dict(child_job))

        return Job(
            id=res["id"],
            external_identifier=res["externalIdentifier"],
            slug=res["slug"],
            resource=res["resource"] if "resource" in res else None,
            status=res["status"],
            is_terminal_state=res["isTerminalState"]
            if "isTerminalState" in res
            else None,
            remote_status=res["remoteStatus"] if "remoteStatus" in res else None,
            job_data_schema=res["jobDataSchema"] if "jobDataSchema" in res else None,
            job_data=res["jobData"] if "jobData" in res else None,
            child_jobs=child_jobs,
        )


@dataclass
class File:
    id: str
    slug: Optional[str] = None
    label: Optional[str] = None
    file_name: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict):
        return File(
            id=d["id"],
            slug=d["slug"],
            label=d["label"],
            url=d["url"],
            file_name=d["fileName"],
        )


create_request = Operation(
    query="""
        mutation jobCreate(
            $resource_slug: String!,
            $workspace_member_slug: String!,
            $parent_job_slug: String,
            $external_identifier: String,
            $status: JobStatus,
            $remote_status: String,
            $job_data_schema: String,
            $job_data: JSON) {
            jobCreate(input: {
                resourceSlug: $resource_slug,
                workspaceMemberSlug: $workspace_member_slug,
                parentJobSlug: $parent_job_slug,
                externalIdentifier: $external_identifier,
                status: $status,
                remoteStatus: $remote_status,
                jobDataSchema: $job_data_schema,
                jobData: $job_data,
            }) {
                job {
                id
                externalIdentifier
                slug
                status
                isTerminalState
                remoteStatus
                jobDataSchema
                jobData
                }
            }
        }
        """,
)


def create(
    api: API,
    resource_slug: str,
    workspace_member_slug: str,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: Optional[str] = None,
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
) -> Job:
    """Create a job entry

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        used as identifier for the resource.
    workspaceMemberSlug: str
        used to map workspace and user.
    parentJobSlug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: {Optionapstr
        status of the job. Refer to the  platform for possible values.
    remoteStatus: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    jobDataSchema: Optional[str]
        link to the json schema describing job output.
    jobData: Optional[str]
        job output.

    Returns
    -------
    : Job
        The ``Job`` object
    """
    platform_result = api.execute(
        op=create_request,
        **locals(),
    )

    return Job.from_dict(platform_result["jobCreate"]["job"])


update_request = Operation(
    query="""
        mutation jobUpdate(
            $resource_slug: String!,
            $job_slug: String!,
            $parent_job_slug: String,
            $external_identifier: String,
            $status: JobStatus,
            $remote_status: String,
            $job_data_schema: String,
            $job_data: JSON) {
            jobUpdate(input: {
                resourceSlug: $resource_slug,
                jobSlug: $job_slug,
                parentJobSlug: $parent_job_slug,
                externalIdentifier: $external_identifier,
                status: $status,
                remoteStatus: $remote_status,
                jobDataSchema: $job_data_schema,
                jobData: $job_data,
            }) {
                job {
                id
                externalIdentifier
                slug
                status
                isTerminalState
                remoteStatus
                jobDataSchema
                jobData
                }
            }
        }
        """,
)


def update(
    api: API,
    resource_slug: str,
    job_slug: str,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: Optional[str] = None,
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
) -> Job:
    """Make an update to a job entry.

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        used as identifier for the resource.
    job_slug: str
        identifier used to retrieve the job.
    parent_job_slug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: {Optionapstr
        status of the job. Refer to the  platform for possible values.
    remote_status: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    job_data_schema: Optional[str]
        link to the json schema describing job output.
    job_data: Optional[str]
        job output.

    Returns
    -------
    : Job
        The ``Job`` object
    """
    platform_result = api.execute(
        op=update_request,
        **locals(),
    )
    return Job.from_dict(platform_result["jobUpdate"]["job"])


def get_job_request(query: str, job_param_name: str) -> Operation:
    return Operation(
        query=f"""
        query {query} (
            $resource_slug: String!,
            $id: String!) {{
            {query}(
                resourceSlug: $resource_slug,
                {job_param_name}: $id
            )
            {{
                id
                childJobs {{
                    id
                }}
                externalIdentifier
                slug
                status
                isTerminalState
                remoteStatus
                jobDataSchema
                jobData
            }}
        }}
        """
    )


def get(
    api: API,
    resource_slug: str,
    id: str,
) -> Job:
    """Retrieve job info

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        identifier for the resource.
    id: str
        the job_slug identifier used to retrieve the job.

    Returns
    -------
    Job
        The ``Job`` object identified by the slug.
    """
    platform_result = api.execute(
        op=get_job_request("job", "jobSlug"),
        **locals(),
    )
    return Job.from_dict(platform_result["job"])


get_jobs_request = Operation(
    query="""
        query jobs(
            $external_identifier: String,
            $resource_slug: String,
            $parent_job_slug: String,
        ) {
            jobs(
                externalIdentifier: $external_identifier,
                resourceSlug: $resource_slug,
                parentJobSlug: $parent_job_slug
            ) {
                edges {
                    node {
                        id
                        slug
                        status
                        resource {
                            slug
                        }
                        externalIdentifier
                        isTerminalState
                        remoteStatus
                        dateJobCreated
                        dateJobCompleted
                    }
                }
            }
        }
""",
)


def get_by_external_identifier(
    api: API,
    id: str,
) -> Optional[Job]:
    """Retrieve job info

    Parameters
    ----------
    api: API
        provides access to the platform API.
    id: str
        the external_identifier used to retrieve the job.

    Returns
    -------
    Job
        The ``Job`` object identified by id or None.
    """
    platform_result = api.execute(
        op=get_jobs_request,
        external_identifier=id,
    )
    if "jobs" not in platform_result:
        raise StrangeworksError(
            message="Missing field ('jobs') in response to jobs query", status_code=400
        )
    if "edges" not in platform_result["jobs"]:
        raise StrangeworksError(
            message="Missing field ('edges') in response to jobs query", status_code=400
        )

    if len(platform_result["jobs"]["edges"]) == 0:
        return None

    if len(platform_result["jobs"]["edges"]) > 1:
        raise StrangeworksError(
            message="More than one job returned for product identifier", status_code=400
        )

    if "node" not in platform_result["jobs"]["edges"][0]:
        raise StrangeworksError(
            message="Missing field ('node') in response to jobs query", status_code=400
        )

    val = platform_result["jobs"]["edges"][0]["node"]
    return Job.from_dict(val)


upload_file_request = Operation(
    query="""
        mutation jobUploadFile(
            $resource_slug: String!,
            $job_slug: String!,
            $override_existing: Boolean!,
            $file_desc: Upload!,
            $file_name: String,
            $json_schema: String,
            $is_hidden: Boolean!,
            $sort_weight: Int!,
            $label: String,
        ){
            jobUploadFile(
                input: {
                    resourceSlug: $resource_slug,
                    jobSlug: $job_slug,
                    shouldOverrideExistingFile: $override_existing,
                    file: $file_desc,
                    fileName: $file_name,
                    jsonSchema: $json_schema,
                    isHidden: $is_hidden,
                    sortWeight: $sort_weight
                    label: $label
                }
            ){
                file {
                    id
                    slug
                    label
                    fileName
                    url
                    metaFileType
                    metaDateCreated
                    metaDateModified
                    metaSizeBytes
                    jsonSchema
                    dateCreated
                    dateUpdated
                }
            }
        }
        """,
    upload_files=True,
)


def upload_file(
    api: API,
    resource_slug: str,
    job_slug: str,
    file_path: str,
    file_name: Optional[str],
    json_schema: Optional[str],
    label: Optional[str] = None,
    override_existing: bool = False,
    is_hidden: bool = False,
    sort_weight: int = 0,
) -> File:
    """Upload a file associated with a job."""
    with open(file_path, "rb") as fd:
        platform_result = api.execute(
            op=upload_file_request,
            resource_slug=resource_slug,
            job_slug=job_slug,
            file_desc=fd,
            file_name=file_name,
            override_existing=override_existing,
            json_schema=json_schema,
            is_hidden=is_hidden,
            sort_weight=sort_weight,
            label=label,
        )
        return File.from_dict(platform_result["jobUploadFile"]["file"])
