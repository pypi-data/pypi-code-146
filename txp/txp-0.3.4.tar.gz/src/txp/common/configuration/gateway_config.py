from dataclasses import dataclass
from typing import List, Dict, Optional
from txp.common.protos import gateway_config_pb2 as gateway_config_proto
from txp.common.configuration.sampling_window import SamplingWindow
import dataclasses


@dataclass
class GatewayConfig:
    """The Gateway configuration class.

    Received configurations from devices management services should be converted
    to instances of this class.

    Args:
        gateway_id: The Gateway ID configured in the management interface.
        registry_id: The Registry ID to which the Gateway belongs.
        project_id: The GCP Project ID to which the Gateway belongs.
        cloud_region: The cloud region of the project in GCP.
        machines_ids: The List of MachineMetadata IDs monitored by the gateway.
    """

    gateway_id: str
    registry_id: str
    project_id: str
    cloud_region: str
    machines_ids: List[str]
    tenant_id: str

    def get_proto(self) -> gateway_config_proto.GatewayConfigProto:
        """Returns the Protobuff message for this GatewayConfig instance.

        Returns:
            GatewayConfigProto message.
        """

        def map_sampling_window_to_proto(sampling_window: SamplingWindow):
            proto = gateway_config_proto.SamplingWindowProto(
                observation_time=sampling_window.observation_time,
                sampling_time=sampling_window.sampling_time,
            )
            return proto

        config_proto = gateway_config_proto.GatewayConfigProto(
            gateway_id=self.gateway_id,
            registry_id=self.registry_id,
            project_id=self.project_id,
            cloud_region=self.cloud_region,
        )
        config_proto.machines_ids.extend(self.machines_ids)

        return config_proto

    @classmethod
    def build_from_dict(cls, d: Dict) -> Optional["GatewayConfig"]:
        known_fields = list(map(
            lambda field: field.name in d,
            dataclasses.fields(cls)
        ))

        # All the known fields are in the dict
        if not all(known_fields):
            return None

        # Remove unknown field from the dict
        known_fields = list(map(
            lambda field: field.name,
            dataclasses.fields(cls)
        ))

        invalid_keys = [key if key not in known_fields else None for key in d.keys()]

        new_dict = d.copy()
        for key in invalid_keys:
            if key:
                new_dict.pop(key)

        gateway_config = cls(**new_dict)
        return gateway_config

    @staticmethod
    def build_from_proto(
        proto: gateway_config_proto.GatewayConfigProto,
    ) -> "GatewayConfig":
        """Returns the class instance from the proto value.

        Args:
            proto: The GatewayConfigProto to build the class instance from.

        Raises:
            ValueError: if the received proto is not an instance of GatewayConfigProto.
        """
        if isinstance(proto, gateway_config_proto.GatewayConfigProto):
            gateway_id = proto.gateway_id
            registry_id = proto.registry_id
            project_id = proto.registry_id
            cloud_region = proto.cloud_region

            machines_metadata_ids = list(proto.machines_ids)

            return GatewayConfig(
                gateway_id,
                registry_id,
                project_id,
                cloud_region,
                machines_metadata_ids,
                ""  # Empty tenant-id because configuration protobuff are NOT being used.
            )

        raise ValueError(
            "Trying to build GatewayConfig from proto, but the proto instance is unknown"
        )

    def reprJSON(self) -> Dict:
        """Returns a Dict easily serializable to JSON.

        The Dictionary will contain the values required to re-create the instance from the JSON
        object in a pythonic way:
            object = MyObject( **json.loads(json_string) )
        """
        return dict(
            gateway_id=self.gateway_id,
            registry_id=self.registry_id,
            project_id=self.project_id,
            cloud_region=self.cloud_region,
            machines_ids=self.machines_ids,
            tenant_id=self.tenant_id
        )

    def __eq__(self, other):
        """Equality operator impementation to compare two instances of
        GatewayConfig"""
        if not isinstance(self, other):
            return False

        return (
                self.gateway_id == other.gateway_id and
                self.registry_id == other.registry_id and
                self.project_id == other.project_id and
                self.cloud_region == other.cloud_region and
                self.machines_ids == other.machines_ids and
                self.tenant_id == other.tenant_id
        )
