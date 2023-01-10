"""product.py."""
import os
from dataclasses import dataclass
from typing import List, Optional

from fastapi import Request
from jose import jwt

from sw_product_lib.client import backend, billing, job, resource
from sw_product_lib.client.billing import BillingTransaction
from sw_product_lib.client.job import File, Job
from sw_product_lib.client.platform import API, APIName
from sw_product_lib.client.resource import Resource
from sw_product_lib.errors.error import StrangeworksError


@dataclass
class RequestContext:
    resource_token_id: str
    workspace_member_slug: str
    product_slug: str
    resource_slug: str
    job_id: Optional[str] = None
    resource_entitlements: Optional[List[str]] = None
    api: Optional[API] = None

    @staticmethod
    def new(
        workspace_member_slug: str,
        product_slug: str,
        resource_slug: str,
        resource_token_id: str = "",
        job_id: str = None,
        resource_entitlements: List[str] = None,
        api: API = None,
    ):
        return RequestContext(
            resource_token_id=resource_token_id,
            workspace_member_slug=workspace_member_slug,
            product_slug=product_slug,
            resource_slug=resource_slug,
            job_id=job_id,
            resource_entitlements=resource_entitlements,
            api=api,
        )

    @staticmethod
    def from_request(request: Request):
        token = request.headers.get("x-strangeworks-access-token")
        if not token:
            raise StrangeworksError.forbidden_error(
                message="request missing access token"
            )
        return RequestContext.from_jwt(token)

    @staticmethod
    def from_jwt(token: str):
        message = jwt.decode(token=token, key=None, options={"verify_signature": False})
        return RequestContext(
            resource_token_id=message["ResourceTokenID"],
            workspace_member_slug=message["WorkspaceMemberSlug"],
            product_slug=message["ProductSlug"],
            resource_slug=message["ResourceSlug"],
            resource_entitlements=message["ResourceEntitlements"],
        )


DEFAULT_PLATFORM_BASE_URL = "https://api.strangeworks.com"
api_key = os.getenv("PRODUCT_LIB_API_KEY")
base_url = os.getenv("PRODUCT_LIB_BASE_URL", DEFAULT_PLATFORM_BASE_URL)

_api = API(api_key=api_key, base_url=base_url, api_id=APIName.PRODUCT)


def create_job(
    ctx: RequestContext,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: str = "CREATED",
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
    **kvargs
) -> Job:
    """Create a job entry for the request

    This method should be called only after the product has either has a job in place
    which will be executed either immediately or within a given period of time.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    parent_job_slug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: Optional[str]
        status of the job. Refer to the  platform for possible values.
    remote_status: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    job_data_schema: Optional[str]
        link to the json schema describing job output.
    job_data: Optional[str]
        job output.
    """
    return job.create(
        api=ctx.api or _api,
        resource_slug=ctx.resource_slug,
        workspace_member_slug=ctx.workspace_member_slug,
        parent_job_slug=parent_job_slug,
        external_identifier=external_identifier,
        status=status,
        remote_status=remote_status,
        job_data_schema=job_data_schema,
        job_data=job_data,
    )


def update_job(
    ctx: RequestContext,
    job_slug: str,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: Optional[str] = None,
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
    **kvargs
) -> Job:
    """Update the job identified by job_slug.


    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
      slug of the job that needs values updated.
    parent_job_slug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: Optional[str]
        status of the job. Refer to the  platform for possible values.
    remote_status: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    job_data_schema: Optional[str]
        link to the json schema describing job output.
    job_data: Optional[str]
        job output.
    """
    return job.update(
        api=ctx.api or _api,
        resource_slug=ctx.resource_slug,
        job_slug=job_slug,
        parent_job_slug=parent_job_slug,
        external_identifier=external_identifier,
        status=status,
        remote_status=remote_status,
        job_data_schema=job_data_schema,
        job_data=job_data,
    )


def create_billing_transaction(
    ctx: RequestContext,
    job_slug: str,
    amount: float,
    unit: str = "USD",
    description: Optional[str] = None,
) -> BillingTransaction:
    """Create a billing transaction.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
        used as identifier for the job.
    amount: float
        numerical amount. can be negative.
    unit: str
        describes the unit for the amount. for example, USD for currency.
    description: str
        a brief description that can be seen by the user.
    """
    return billing.create_transaction(
        api=ctx.api or _api,
        resource_slug=ctx.resource_slug,
        job_slug=job_slug,
        amount=amount,
        unit=unit,
        description=description,
    )


def request_job_clearance(
    ctx: RequestContext,
    amount: float,
    unit: str = "USD",
):
    """Request clearance from platform to run a job.

    Parameters
    ----------
    workspaceMemberSlug: str
            used to map workspace and user.
    amount: float
        numerical amount to indicate cost (negative amount) or credit(positive amount)
    unit: str
        unit for the amount
    """
    return billing.request_approval(
        api=ctx.api or _api,
        resource_slug=ctx.resource_slug,
        workspace_member_slug=ctx.workspace_member_slug,
        amount=amount,
        currency=unit,
    )


def get_resource(ctx: RequestContext) -> Resource:
    """Retrieve a resource definition.

    The resource slug, which is used to identify the resource entry, is retrieved
    from the request context object passed in.

    Parameters:
    ctx: RequestContext
        contains key-values specific to the current request.

    """
    return resource.get(api=_api, resource_slug=ctx.resource_slug)


def upload_job_file(
    ctx: RequestContext,
    job_slug: str,
    name: Optional[str],
    path: str,
    json_schema: Optional[str],
    label: Optional[str] = None,
    overwrite: bool = False,
    is_hidden: bool = False,
    sort_weight: int = 0,
) -> File:
    """Upload a file associated with a job.

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
        identifies which job the file is associated with.
    name: Optional[str]
        file name.
    path: str
        fully qualified path to the file.
    json_schema: Optional[str]
        identifier or link to a json schema which corresponds to the file contents. If
        the file contents adhere to a schema, it is highly recommended that this field
        is populated.
    label: Optional[str]
        Optional string to set the display name of the file. Used by the platform
        portal.
    overwrite: bool
        indicates whether the file should be overwritten if its already been uploaded
        for the job. Defaults to False.
    is_hidden: bool
        If true, this file will not be displayed in the portal.
        This can be useful for supporting files that should be saved against the job,
        but typically would be referenced by URL in other contexts.
        (i.e.: an image file which is referenced in a JSON model.)
        This does **not*** prevent a user from accessing this file in other contexts,
        such as job archives.
    sort_weight: int
        This is the primary sorting instruction for JobFiles
        when returned to the client.
        The default is 0.
        Files with a higher sort order will be returned first.
        This allows you to control the order of files in the portal if desired.

    Return
    ------
    File
        Object with information about the file that was uploaded.
    """
    return job.upload_file(
        api=ctx.api or _api,
        resource_slug=ctx.resource_slug,
        job_slug=job_slug,
        file_path=path,
        file_name=name,
        override_existing=overwrite,
        json_schema=json_schema,
        is_hidden=is_hidden,
        sort_weight=sort_weight,
        label=label,
    )


def get_job(ctx: RequestContext, job_slug: str) -> Job:
    """Get the job identified by job_slug.


    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    job_slug: str
        job_slug identifies the job which is fetched.

    Returns
    -------
    Job
        A Job object identified by the slug.
    """
    return job.get(api=ctx.api or _api, resource_slug=ctx.resource_slug, id=job_slug)


def get_job_by_external_identifier(
    ctx: RequestContext, external_identifier: str
) -> Optional[Job]:
    """Get the job identified by external_identifier.


    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    external_identifier: str
        external_identifier identifies the job which is fetched.

    Returns
    -------
    Optional[Job]
        A Job object identified by the product identifier or None.
    """
    return job.get_by_external_identifier(
        api=ctx.api or _api,
        id=external_identifier,
    )


def get_backends(
    ctx: RequestContext,
    status: Optional[str] = None,
    remote_backend_id: Optional[str] = None,
) -> List[backend.Backend]:
    """Get the backends filtered by status or remote_backend_id

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    status: Optional[str]
        filter by status, optional
    remote_backend_id: Optional[str]
        filter by remote backend id, optional

    Returns
    -------
    List[Backend]
        The list of backend filtered by the params
    """
    return backend.get_backends(
        api=ctx.api or _api, status=status, remote_backend_id=remote_backend_id
    )


def create_backends(
    ctx: RequestContext, backends: List[backend.Backend]
) -> List[backend.Backend]:
    """Create backends specified by the payload

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    backends: List[Backend]
        backends to create

    Returns
    -------
    List[Backend]
        The list of backends created
    """
    return backend.backend_create(api=ctx.api or _api, payload=backends)


def delete_backend(ctx: RequestContext, backend_slug: str) -> None:
    """Delete backend by slug

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    backend_slug: str
        backend to delete

    Returns
    -------
    None
    """
    return backend.backend_delete(api=ctx.api or _api, backend_slug=backend_slug)


def update_backends(
    ctx: RequestContext, backends: List[backend.Backend]
) -> List[backend.Backend]:
    """Update backends specified by the payload
    Overwites all write-able fields, so must include
    original payload, otherwise some fields could be deleted

    Parameters
    ----------
    ctx: RequestContext
        contains key-values specific to the current request.
    backends: List[Backend]
        backends to update

    Returns
    -------
    List[Backend]
        The list of backends updated
    """
    return backend.backend_update(api=ctx.api or _api, backend_update_input=backends)


def get_token(ctx: RequestContext) -> str:
    """
    returns the current token in use by the api
    """
    api = ctx.api or _api
    return api.auth_token
