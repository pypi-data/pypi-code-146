from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_service_metadata import HttpServiceMetadata


T = TypeVar("T", bound="HttpServiceRecord")


@attr.s(auto_attribs=True)
class HttpServiceRecord:
    """
    Attributes:
        host (str):
        metadata (HttpServiceMetadata):
        name (str):
        port (int):
        ssl (Union[Unset, bool]):
    """

    host: str
    metadata: "HttpServiceMetadata"
    name: str
    port: int
    ssl: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        host = self.host
        metadata = self.metadata.to_dict()

        name = self.name
        port = self.port
        ssl = self.ssl

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "host": host,
                "metadata": metadata,
                "name": name,
                "port": port,
            }
        )
        if ssl is not UNSET:
            field_dict["ssl"] = ssl

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.http_service_metadata import HttpServiceMetadata

        d = src_dict.copy()
        host = d.pop("host")

        metadata = HttpServiceMetadata.from_dict(d.pop("metadata"))

        name = d.pop("name")

        port = d.pop("port")

        ssl = d.pop("ssl", UNSET)

        http_service_record = cls(
            host=host,
            metadata=metadata,
            name=name,
            port=port,
            ssl=ssl,
        )

        return http_service_record
