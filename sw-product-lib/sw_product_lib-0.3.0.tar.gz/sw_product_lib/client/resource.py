from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from sw_product_lib.client.platform import API, Operation


class ResourceConfigurationValueType(Enum):
    BOOL = "BOOL"
    STRING = "STRING"
    SECURE = "SECURE"
    INT = "INT"
    JSON = "JSON"
    DATE = "DATE"
    FLOAT = "FLOAT"

    def equals(self, type: str) -> bool:
        return self.name == type


class ResourceConfiguration:
    def __init__(
        self,
        key: str,
        value: Any,
        is_secure: bool = False,
        is_editable: bool = True,
        is_internal: bool = False,
    ):
        self.key: str = key
        self.value: Any = value
        if is_secure:
            self.value_type = "SECURE"
        else:
            _val_type = type(value).__name__.upper()
            self.value_type = "STRING" if _val_type == "STR" else _val_type

        self.is_editable = is_editable
        self.is_internal = is_internal

    @classmethod
    def from_dict(cls, rc: Dict[str, Any]) -> ResourceConfiguration:
        _value_type = rc["type"]
        _value_key = f"value{_value_type.capitalize()}"
        return ResourceConfiguration(
            key=rc["key"],
            value=rc[_value_key],
            is_secure=rc["type"] == "SECURE",
            is_editable=rc["isEditable"],
            is_internal=rc["isInternal"],
        )

    def to_dict(self) -> Dict[str, Any]:
        valueKey = f"value{self.value_type.capitalize()}"

        return {
            "key": self.key,
            "type": self.value_type,
            "isEditable": self.is_editable,
            "isInternal": self.is_internal,
            valueKey: self.value,
        }


class Resource:
    def __init__(
        self,
        configurations: Optional[List[ResourceConfiguration]] = None,
        id: str = "",
        slug: str = "",
        status: str = "",
    ) -> None:
        self.configurations = configurations
        self.id = id
        self.slug = slug
        self.status = status

    @classmethod
    def from_dict(cls, res: dict) -> Resource:
        return Resource(
            id=res["id"],
            slug=res["slug"],
            status=res["status"],
            configurations=None
            if "configurations" not in res
            else list(
                map(lambda x: ResourceConfiguration.from_dict(x), res["configurations"])
            ),
        )


create_req = Operation(
    query="""
        mutation resourceCreate(
            $activation_id: String!,
            $status: ResourceStatus!,
            $api_route: String,
            $configurations: [StoreConfigurationInput!],
        ){
            resourceCreate(input: {
                resourceActivationId: $activation_id,
                status: $status,
                api_route: $api_route,
                resourceConfigurations: $configurations,
            }) {
                resource {
                id
                slug
                isDeleted
                status
                dateCreated
                dateUpdated
                configurations {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
              }
            }
        }
        """
)


def create(
    api: API,
    activation_id: str,
    status: str,
    api_route: Optional[str] = None,
    configurations: Optional[List[ResourceConfiguration]] = None,
) -> Resource:
    """Create a new resource definition on the platform.

    Parameters
    ----------
     api: API
        provides access to the platform API.
    """
    api_args = {
        "activation_id": activation_id,
        "status": status,
        "api_route": api_route,
    }

    if configurations:
        api_args["configurations"] = list(map(lambda x: x.to_dict(), configurations))

    result = api.execute(
        op=create_req,
        **api_args,
    )

    return Resource.from_dict(result["resourceCreate"]["resource"])


list_req = Operation(
    query="""
        query resources($status_list: [ResourceStatus!]){
            resources(status: $status_list) {
                id
                slug
                status
                isDeleted
                dateCreated
                dateUpdated
                configurations {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
            }
        }
        """
)


def fetch(
    api: API,
    status_list: Optional[List[str]] = None,
) -> Optional[List[Resource()]]:
    """Retrieve a list of available resources.

    Parameters
    ----------
    status_list: Optional(List[str])
        retrieve only those resources whose status is included in this list.
    """
    result = api.execute(op=list_req, **locals())
    return list(map(lambda x: Resource.from_dict(x), result["resources"]))


store_config_op = Operation(
    query="""
        mutation resourceStoreConfiguration(
            $key: String!,
            $resource_slug: String!,
            $type: ResourceConfigurationValueType!,
            $isEditable: Boolean!,
            $isInternal: Boolean!,
            $valueBool: Boolean,
            $valueString: String,
            $valueSecure: String,
            $valueInt: Int,
            $valueJson: String,
            $valueDate: Time,
            $valueFloat: Float,
        ){
            resourceStoreConfiguration(
                input: {
                    resourceSlug: $resource_slug,
                    configuration: {
                        key: $key,
                        type: $type,
                        isEditable: $isEditable,
                        isInternal: $isInternal,
                        valueBool: $valueBool,
                        valueString: $valueString,
                        valueSecure: $valueSecure,
                        valueInt: $valueInt,
                        valueJson: $valueJson,
                        valueDate: $valueDate,
                        valueFloat: $valueFloat,
                    }
                }
            ) {
                resourceConfiguration {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
            }
        }
        """,
)


def store_config(
    api: API,
    resource_slug: str,
    config: ResourceConfiguration,
) -> ResourceConfiguration:
    # params = {
    #     "resource_slug": resource_slug,
    #     "configuration": config.to_dict(),
    # }
    params = config.to_dict()
    params["resource_slug"] = resource_slug
    result = api.execute(op=store_config_op, **params)
    return ResourceConfiguration.from_dict(
        result["resourceStoreConfiguration"]["resourceConfiguration"]
    )


get_op = Operation(
    query="""
        query resource($resource_slug: String!) {
            resource(resourceSlug: $resource_slug){
                id
                slug
                status
                isDeleted
                dateCreated
                dateUpdated
                configurations {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
            }
        }
    """,
)


def get(
    api: API,
    resource_slug: str,
) -> Resource:
    """Retrieve a resource entry from platform."""
    raw_result = api.execute(op=get_op, **locals())
    return Resource.from_dict(raw_result["resource"])
