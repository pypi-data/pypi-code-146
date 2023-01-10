import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from sw_product_lib.client.platform import API, Operation
from sw_product_lib.errors.error import StrangeworksError


@dataclass
class BackendTags:
    id: str
    tag: str
    display_name: str
    tag_group: str
    is_system: bool


@dataclass
class BackendType:
    id: str
    slug: str
    display_name: str
    description: str
    schema_url: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(res: dict):
        return BackendType(
            id=res["id"],
            slug=res["slug"],
            display_name=res["displayName"],
            description=res["description"],
            schema_url=res["schemaURL"],
        )


@dataclass
class BackendRegsitration:
    backend_type_id: str
    backend_type: str
    data: dict

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(res: dict):
        br = BackendRegsitration(
            backend_type_id=res["id"],
            data=res["data"],
        )
        if "backendType" in res:
            br.backend_type = BackendType.from_dict(res["backendType"])
        return br


@dataclass
class Backend:
    id: str
    name: str
    data_schema: Optional[str] = None
    remote_backend_id: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[str] = None
    backend_registration: Optional[List[BackendRegsitration]] = None
    remote_status: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

    def dict(self):
        return self.__dict__

    def to_create_request(self):
        return {
            "data": json.dumps(self.data),
            "dataSchema": self.data_schema,
            "name": self.name,
            "remoteBackendId": self.remote_backend_id,
            "remoteStatus": self.remote_status,
            "status": self.status,
        }

    def to_update_request(self):
        return {
            "backendSlug": self.slug,
            "data": json.dumps(self.data),
            "dataSchema": self.data_schema,
            "name": self.name,
            "remoteBackendId": self.remote_backend_id,
            "remoteStatus": self.remote_status,
            "status": self.status,
        }

    @staticmethod
    def from_dict(res: dict):
        b = Backend(
            id=res["id"],
            data=res["data"],
            data_schema=res["dataSchema"],
            name=res["name"],
            remote_backend_id=res["remoteBackendId"],
            remote_status=res["remoteStatus"],
            slug=res["slug"],
            status=res["status"],
        )
        if "backendRegistration" in res:
            for br in res["backendRegistration"]:
                b.backend_registration.append(BackendRegsitration.from_dict(br))
        return b


get_backends_request = Operation(
    query="""
    query backends($status: BackendStatus, $remote_backend_id: String) {
        backends(status: $status, remoteBackendId: $remote_backend_id) {
            id
            slug
            name
            status
            remoteBackendId
            remoteStatus
            data
            dataSchema
            dateRefreshed
            backendRegistrations {
                backendType {
                    id
                    schemaURL
                    slug
                    displayName
                    description
                }
                backendTypeId
                data
            }
        }
    }
    """,
)


def get_backends(
    api: API,
    status: str = None,
    remote_backend_id: str = None,
) -> List[Backend]:
    """Fetch backends for product

    Parameters
    ----------
    api: API
        provides access to the product API
    status: str
        filter by backend status
    remote_backend_id: str
        filter by the backend id set by the product

    Returns
    -------
    List[Backend]
        The list of backends filtered by the params
    """
    platform_res = api.execute(op=get_backends_request, **locals())
    b = []
    for r in platform_res["backends"]:
        b.append(Backend.from_dict(r))
    return b


backend_add_type_mutation = Operation(
    query="""
    mutation backendAddTypes($backend_slug: String!,$backend_types: List!){
        backendAddTypes(input: {
            backendSlug: $backend_slug,
            backendTypes: $backend_types
        }) {
            backendSlug
            backendTypeSlugs
        }
    }
    """,
)


def backend_add_type(
    api: API,
    backend_slug: str,
    backend_types: List,
) -> None:
    api.execute(op=backend_add_type_mutation, **locals())
    return None


backend_remove_types_mutation = Operation(
    query="""
    mutation backendRemoveTypes($backend_slug: String!,$backend_type_slugs: List!){
        backendRemoveTypes(input: {
            backendSlug: $backend_slug,
            backendTypeSlugs: $backend_type_slugs
        }) {
            backendSlug
            backendTypeSlugs
        }
    }
    """,
)


def backend_remove_types(
    api: API,
    backend_slug: str,
    backend_type_slugs: List,
) -> None:
    api.execute(op=backend_remove_types_mutation, **locals())
    return None


backend_create_mutation = Operation(
    query="""
    mutation backendCreate($backends: [ProductBackendInput!]){
        backendCreate(input: {backends: $backends}) {
            backends {
                id
                slug
                name
                status
                remoteBackendId
                remoteStatus
                data
                dataSchema
                dateRefreshed
                backendRegistrations {
                    backendType {
                        id
                        schemaURL
                        slug
                        displayName
                        description
                    }
                    backendTypeId
                    data
                }
            }
        }
    }
    """
)


def backend_create(
    api: API,
    payload: List[Backend],
) -> List[Backend]:
    backends = []
    for b in payload:
        backends.append(b.to_create_request())
    platform_res = api.execute(op=backend_create_mutation, backends=backends)
    res = []
    if (
        "backendCreate" not in platform_res
        and "backends" not in platform_res["backendCreate"]
    ):
        raise StrangeworksError.server_error(f"invalid response {platform_res}")
    for r in platform_res["backendCreate"]["backends"]:
        res.append(Backend.from_dict(r))
    return res


backend_delete_mutation = Operation(
    query="""
    mutation backendDelete($backend_slug: String!){
        backendDelete(input: { backendSlug: $backend_slug })
    }
    """,
)


def backend_delete(
    api: API,
    backend_slug: str,
) -> None:
    api.execute(op=backend_delete_mutation, **locals())


backend_update_mutation = Operation(
    query="""
    mutation backendUpdate($backends: [ProductBackendUpdateInput!]){
        backendUpdate(input: {backends: $backends}) {
            backends {
                id
                slug
                name
                status
                remoteBackendId
                remoteStatus
                data
                dataSchema
                dateRefreshed
                backendRegistrations {
                    backendType {
                        id
                        schemaURL
                        slug
                        displayName
                        description
                    }
                    backendTypeId
                    data
                }
            }
        }
    }
    """,
)


def backend_update(
    api: API,
    backend_update_input: List[Backend],
) -> Backend:
    backends = []
    for b in backend_update_input:
        backends.append(b.to_update_request())
    platform_res = api.execute(op=backend_update_mutation, backends=backends)
    if (
        "backendUpdate" not in platform_res
        and "backends" not in platform_res["backendUpdate"]
    ):
        raise StrangeworksError.server_error(f"invalid response {platform_res}")
    res = []
    for r in platform_res["backendUpdate"]["backends"]:
        res.append(Backend.from_dict(r))
    return res
