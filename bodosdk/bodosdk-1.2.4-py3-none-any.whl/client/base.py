import os
from bodosdk.api.instance_role import InstanceRoleApi
from bodosdk.api.auth import AuthApi
from bodosdk.api.cloud_config import CloudConfigApi
from bodosdk.api.cluster import ClusterApi
from bodosdk.api.job import JobApi
from bodosdk.api.catalog import CatalogApi
from bodosdk.api.request_wrapper import RequestWrapper
from bodosdk.api.secret_group import SecretGroupApi
from bodosdk.api.secrets import SecretsApi
from bodosdk.api.workspace import WorkspaceApi
from bodosdk.client.cloud_config import CloudConfigClient
from bodosdk.client.cluster import ClusterClient
from bodosdk.client.instance_role import InstanceRoleClient
from bodosdk.client.job import JobClient
from bodosdk.client.secret_group import SecretGroupClient
from bodosdk.client.secrets import SecretsClient
from bodosdk.client.workspace import WorkspaceClient
from bodosdk.client.catalog import CatalogClient
from bodosdk.exc import APIKeysMissing
from bodosdk.models import APIKeys
from bodosdk.models import PersonalKeys


class BodoClient:
    job: JobClient
    cluster: ClusterClient
    instance_role: InstanceRoleClient
    catalog: CatalogClient
    secret_group: SecretGroupClient
    secrets: SecretsClient

    def __init__(
        self,
        auth_api: AuthApi,
        job_client: JobClient,
        cluster_client: ClusterClient,
        instance_role: InstanceRoleClient,
        secret_group: SecretGroupClient,
        secrets: SecretsClient,
        catalog: CatalogClient,
    ):
        self._auth_api = auth_api
        self.job = job_client
        self.cluster = cluster_client
        self.instance_role = instance_role
        self.catalog = catalog
        self.secret_group = secret_group
        self.secrets = secrets


class BodoOrganizationClient:
    workspace: WorkspaceClient
    cloud_config: CloudConfigClient

    def __init__(
        self,
        auth_api: AuthApi,
        workspace_client: WorkspaceClient,
        cloud_config_client: CloudConfigClient,
    ):
        self._auth_api = auth_api
        self.workspace = workspace_client
        self.cloud_config = cloud_config_client


def get_bodo_client(
    auth: APIKeys = None,
    api_url="https://api.bodo.ai/api",
    auth_url="https://prod-auth.bodo.ai",
    print_logs=False,
):
    """
    :param auth: a set of client_id / seceret_key used for auth token generation
    :type auth: APIKeys
    :param api_url: api address of BodoPlatform
    :type api_url: str
    :param auth_url: api address of BodoAuthentication
    :type auth_url: str
    :param print_logs: set to True if you want to print all requests performed
    :type print_logs: boolean
    :return: BodoClient
    """

    # check BODO_CLIENT_ID/BODO_SECRET_KEY environment variables if auth keys are not
    # provided
    if not auth:
        client_id = os.environ.get("BODO_CLIENT_ID")
        secret_key = os.environ.get("BODO_SECRET_KEY")
        if client_id and secret_key:
            auth = APIKeys(client_id=client_id, secret_key=secret_key)
        else:
            raise APIKeysMissing(
                "BODO_CLIENT_ID and BODO_SECRET_KEY environment variables "
                "should be set if APIKeys are not passed to get_bodo_client()"
            )

    auth_api = AuthApi(auth, auth_url, RequestWrapper(print_logs))
    job_client = JobClient(JobApi(auth_api, api_url, RequestWrapper(print_logs)))
    cluster_client = ClusterClient(
        ClusterApi(auth_api, api_url, RequestWrapper(print_logs))
    )
    instance_role_client = InstanceRoleClient(
        InstanceRoleApi(auth_api, api_url, RequestWrapper(print_logs))
    )

    secret_group_client = SecretGroupClient(
        SecretGroupApi(auth_api, api_url, RequestWrapper(print_logs))
    )
    secrets_client = SecretsClient(
        SecretsApi(auth_api, api_url, RequestWrapper(print_logs))
    )
    catalog_client = CatalogClient(
        CatalogApi(auth_api, api_url, RequestWrapper(print_logs))
    )
    return BodoClient(
        auth_api,
        job_client,
        cluster_client,
        instance_role_client,
        secret_group_client,
        secrets_client,
        catalog_client,
    )


def get_bodo_organization_client(
    auth: PersonalKeys,
    api_url="https://api.bodo.ai/api",
    auth_url="https://prod-auth.bodo.ai",
    print_logs=False,
):
    """
    :param auth: a set of client_id / seceret_key used for auth token generation
    :type auth: PersonalKeys
    :param api_url: api address of BodoPlatform
    :type api_url: str
    :param auth_url: api address of BodoAuthentication
    :type auth_url: str
    :param print_logs: set to True if you want to print all requests performed
    :type print_logs: boolean
    :return: BodoOrganizationClient
    """
    if not auth:
        client_id = os.environ.get("BODO_CLIENT_ID")
        secret_key = os.environ.get("BODO_SECRET_KEY")
        if client_id and secret_key:
            auth = PersonalKeys(client_id=client_id, secret_key=secret_key)
        else:
            raise APIKeysMissing
    auth_api = AuthApi(auth, auth_url, RequestWrapper(print_logs))
    workspace_client = WorkspaceClient(
        WorkspaceApi(auth_api, api_url, RequestWrapper(print_logs))
    )
    cloud_config_client = CloudConfigClient(
        CloudConfigApi(auth_api, api_url, RequestWrapper(print_logs))
    )
    return BodoOrganizationClient(auth_api, workspace_client, cloud_config_client)
