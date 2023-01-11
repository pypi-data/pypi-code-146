"""Common classes for Edge devices support.

This module contains the following classes that are commonly used in
edge definition and usage:
    - EdgeType
    - MachineMetadata
    - EdgeDescriptor
"""

# ============================ imports =========================================
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from typing import List
import txp.common.protos.gateway_config_pb2 as gateway_config_proto
from txp.devices.drivers.usb.camera.camera_handler_base import CameraType
from google.protobuf import json_format
import dataclasses
import hashlib


class EdgeType(Enum):
    """Enumeration names for the different types of defined edge devices

    The purpose of this class is to provide typed constants for edge types.

    An ACTUATOR_DEVICE, is the type of device that can be use to multiply
        edges. Concretely, we currently support the Robotic arm which is
        the only supported ACTUATOR_DEVICE.
    """

    STREAM_ONLY_DEVICE = "STREAM_ONLY_DEVICE"
    ON_OFF_DEVICE = "ON_OFF_DEVICE"
    SMART_DEVICE = "SMART_DEVICE"
    ACTUATOR_DEVICE = "ACTUATOR_DEVICE",

    def __str__(self):
        return self.name

    @staticmethod
    def from_str(type_val: str):
        if type_val == str(EdgeType.STREAM_ONLY_DEVICE.name):
            return EdgeType.STREAM_ONLY_DEVICE
        elif type_val == str(EdgeType.ON_OFF_DEVICE):
            return EdgeType.ON_OFF_DEVICE
        elif type_val == str(EdgeType.SMART_DEVICE.name):
            return EdgeType.SMART_DEVICE
        elif type_val == str(EdgeType.ACTUATOR_DEVICE.name):
            return EdgeType.ACTUATOR_DEVICE
        else:
            raise NotImplementedError


class SingletonMeta(type):
    """
    This is meta class for implementation of a singleton.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


@dataclass
class MachineMetadata:
    """Encapsulates the metadata from the machine monitored by an edge
    device.

    TODO: This class should contain whatever informtion associated to
        the machine is required for collected data interpretation.

    TODO: this class should contain information about the bearing
        mechanism
    """

    machine_id: str
    model: str
    manufacturer: str
    edges_ids: List[str]
    state_manager: str = ""
    tasks: dict = dataclasses.field(default_factory=dict)

    """edges_ids: The list of edge ids associated with this machine"""

    def get_proto(self) -> gateway_config_proto.MachineMetadataProto:
        """Returns the proto for the object.

        Returns:
            A MachineMetadataProto instance from this object.
        """
        proto = gateway_config_proto.MachineMetadataProto(
            machine_id=self.machine_id,
            model=self.model,
            manufacturer=self.manufacturer
        )
        proto.edges_ids.extend(self.edges_ids)
        return proto

    @classmethod
    def build_from_dict(cls, d: Dict) -> Optional["MachineMetadata"]:
        optional_fields = ['state_manager',
                           'tasks']

        known_fields = list(map(
            lambda field: field.name in d if field.name not in optional_fields else True,
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

        m_m = MachineMetadata(**new_dict)
        return m_m

    @staticmethod
    def build_from_proto(
        proto: gateway_config_proto.MachineMetadataProto,
    ) -> "MachineMetadata":
        """Returns the class instance from the proto value.

        Args:
            proto: The MachineMetadataProto to build the class instance from.

        Raises:
            ValueError: if the received proto is not an instance of MachineMetadataProto.
        """
        if isinstance(proto, gateway_config_proto.MachineMetadataProto):
            return MachineMetadata(
                proto.machine_id,
                proto.model,
                proto.manufacturer,
                list(proto.edges_ids)
            )

        raise ValueError(
            "Trying to build MachineMetadata from proto, but the proto instance is unknown"
        )

    def reprJSON(self) -> Dict:
        """Returns a Dict easily serializable to JSON.

        The Dictionary will contain the values required to re-create the instance from the JSON
        object in a pythonic way:
            object = MyObject( **json.loads(json_string) )
        """
        return dict(machine_id=self.machine_id, model=self.model, manufacturer=self.manufacturer,
                    edges_ids=self.edges_ids, state_manager=self.state_manager, tasks=self.tasks)


@dataclasses.dataclass(frozen=True)
class VirtualSensorObject:
    """Class to track the necessary information required for a virtual sensor.

    For example, a Camera or Thermocamera configured in a robotic virtual edge.
    """
    physical_id: str = ""
    camera_type: CameraType = None

    def __bool__(self):
        return bool(str(self.physical_id))  # Empty physical ID evaluates to False

    def reprJSON(self) -> Dict:
        return dict(physical_id=self.physical_id, camera_type=str(self.camera_type))

    @classmethod
    def build_from_dict(cls, d: Dict) -> Optional["VirtualSensorObject"]:
        known_fields = list(map(
            lambda field: field.name in d,
            dataclasses.fields(cls)
        ))

        # All the known fields are in the dict
        if not all(known_fields):
            return None

        return cls(d['physical_id'], CameraType(d['camera_type']))


@dataclasses.dataclass(frozen=True)
class VirtualEdgeInformation:
    """Class to encapsulate the virtual information for an EdgeDescriptor.

    Args:
        position (Tuple): The captured position for this virtual edge.
        virtual_id_hash (str): The virtual ID produced for the captured positions.
            This virtual ID is used with the edge logical ID to get a new
            virtual logical ID.
    """
    position: Tuple
    virtual_id_hash: str

    def reprJSON(self) -> Dict:
        return dict(position=self.position, virtual_id_hash=self.virtual_id_hash)

    @classmethod
    def build_from_dict(cls, d: Dict) -> Optional["VirtualEdgeInformation"]:
        known_fields = list(map(
            lambda field: field.name in d,
            dataclasses.fields(cls)
        ))

        # All the known fields are in the dict
        if not all(known_fields):
            return None

        return cls(tuple(d["position"]), d["virtual_id_hash"])


@dataclass
class EdgeDescriptor:
    """This EdgeDescriptor encapsulates information about an edge.

    Specifically, and EdgeDescriptor holds the information to know:
        - What's the identity of the edge
        - What's the type of the edge
        - Which system driver interacts with the edge
        - Which machine is being monitored by that edge.
        - Configuration parameters for the edge.

    Args:
        logical_id: The serial defined in the IoT management as a registered device.
        device_kind: the device kind from the project model.
            For example: Voyager.
        device_type: the edge type from the project model.
            For example: SMART_DEVICE
        machine_metadata: The machine metadata for the machine monitored
            by the edge.
        edge_parameters: A dictionary of edge parameters.
        perceptions: A Dictionary containing the perceptions definition for the edge.
    """

    logical_id: str
    device_kind: str
    device_type: str
    edge_parameters: Dict
    perceptions: Dict

    def __post_init__(self):
        """Post initializations to keep consistency across the system.

        If the 'physical_key' is not in the edge_parameters, then the device hasn't been paired
        and a default empty value is set.
        """
        if "physical_id" not in self.edge_parameters:
            self.edge_parameters["physical_id"] = ""

    def get_proto(self) -> gateway_config_proto.EdgeDescriptorProto:
        """TODO: Gateway Packages send the EdgeDescriptorProto. That's not really required
            and the GatewayPackage could just remove the EdgeDescriptorProto dependency.
        """
        proto = gateway_config_proto.EdgeDescriptorProto(
            logical_id=self.logical_id,

            device_kind=str(self.device_kind),

            device_type=self.device_type,
        )
        # Edge parameters not required, and probably they will be deprecated as
        # as parameter of the EdgeDescriptorProto.
        # proto.edge_params.update(self.edge_parameters)
        return proto

    @staticmethod
    def build_from_proto(
        proto: gateway_config_proto.EdgeDescriptorProto,
    ) -> "EdgeDescriptor":
        """Returns the class instance from the proto value.

        Args:
            proto: The EdgeDescriptorProto to build the class instance from.

        Raises:
            ValueError: if the received proto is not an instance of EdgeDescriptorProto.

        TODO: Configuration objects are handled using JSON entities. Protos for
            configuration objects are legacy and they should be removed.
        """
        if isinstance(proto, gateway_config_proto.EdgeDescriptorProto):
            return EdgeDescriptor(
                proto.logical_id,
                proto.device_kind,
                proto.device_type,
                json_format.MessageToDict(proto.edge_params),
                {}
            )

        raise ValueError(
            "Trying to build EdgeDescriptor from proto, but the proto instance is unknown"
        )

    def reprJSON(self) -> Dict:
        """Returns a Dict easily serializable to JSON.

        The Dictionary will contain the values required to re-create the instance from the JSON
        object in a pythonic way
            object = MyObject( **json.loads(json_string) )
        """
        return dict(logical_id=self.logical_id, device_kind=self.device_kind,
                    device_type=self.device_type, edge_parameters=self.edge_parameters,
                    perceptions=self.perceptions)

    @classmethod
    def build_from_dict(cls, d: Dict) -> Optional["EdgeDescriptor"]:
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

        if "sensors" in new_dict["edge_parameters"]:
            new_dict['edge_parameters']["sensors"] = list(map(
                lambda sensor_d: VirtualSensorObject.build_from_dict(sensor_d),
                new_dict['edge_parameters']["sensors"]
            ))

            if not any(new_dict['edge_parameters']["sensors"]):
                return None

        if "virtual_device" in new_dict["edge_parameters"]:
            new_dict["edge_parameters"]["virtual_device"] = VirtualEdgeInformation.build_from_dict(
                new_dict["edge_parameters"]["virtual_device"]
            )

            if not new_dict["edge_parameters"]["virtual_device"]:
                return None

        edge_descriptor = cls(**new_dict)
        return edge_descriptor

    def set_physical_id(self, physical_id: str) -> None:
        self.edge_parameters.update({'physical_id': physical_id})

    def is_paired(self) -> bool:
        """Returns True if the device is paired."""
        return bool(self.edge_parameters['physical_id'])  # Empty physical ID will return false

    def set_virtual_sensors(self, sensors: List[VirtualSensorObject]) -> None:
        """Adds the sensors object configured to this virtual Edge descriptor"""
        self.edge_parameters['sensors'] = sensors

    def get_virtual_sensors(self) -> Optional[List[VirtualSensorObject]]:
        """Returns the Virtual sensors of this virtual EdgeDescriptor.
        """
        return self.edge_parameters.get('sensors', None)

    def set_virtual_edge_information(self, virtual_info: VirtualEdgeInformation) -> None:
        """Set the virtual edge information configured for this virtual Edge"""
        self.edge_parameters["virtual_device"] = virtual_info

    def get_virtual_edge_information(self) -> Optional[VirtualEdgeInformation]:
        """Returns the virtual edge information saved in this virtual edge"""
        return self.edge_parameters.get("virtual_device", None)

    def is_actuator_device(self) -> bool:
        return EdgeType.from_str(self.device_type) == EdgeType.ACTUATOR_DEVICE

    @staticmethod
    def get_hashed_virtual_id(positions: Tuple) -> str:
        """Returns the unique virtual ID string for the positions coordinates"""
        m = hashlib.md5()
        for pos in positions:
            m.update(str(pos).encode())
        return m.hexdigest()

    @staticmethod
    def get_complete_virtual_id(actuator_logical_id: str, hashed_id: str) -> str:
        return actuator_logical_id + '_' + hashed_id

    @staticmethod
    def split_virtual_id(virtual_id: str) -> Tuple[str, str]:
        return tuple(virtual_id.split('_'))


@dataclasses.dataclass(frozen=True)
class PairedEdgesPayload:
    """An object to encapsulate the payload sent to the cloud
    when the system finished a devices pairing process."""
    devices: List[EdgeDescriptor]
    machines: List[MachineMetadata]
    tenant_id: str

    def reprJSON(self) -> Dict:
        """Returns a Dict easily serializable to JSON.

        The Dictionary will contain the values required to re-create the instance from the JSON
        object in a pythonic way:
            object = MyObject( **json.loads(json_string) )
        """
        l = []
        machines = []
        for d in self.devices:
            l.append(d.reprJSON())

        for m in self.machines:
            machines.append(m.reprJSON())

        return dict(devices=l, machines=machines, tenant_id=self.tenant_id)

    @classmethod
    def build_from_dict(cls, d: Dict) -> Optional["PairedEdgesPayload"]:
        # All the known fields are in the dict
        if 'devices' not in d:
            return None

        edge_descriptors: List[EdgeDescriptor] = list(map(
            lambda edge_descriptor_d: EdgeDescriptor.build_from_dict(edge_descriptor_d),
            d['devices']
        ))

        machines: List[MachineMetadata] = list(map(
            lambda machine_dict: MachineMetadata.build_from_dict(machine_dict),
            d['machines']
        ))

        return cls(edge_descriptors, machines, d['tenant_id'])
