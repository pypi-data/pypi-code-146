"""
Defines a common encoder designed to work with the dataclasses that requires
to be handled in JSON-string format in IoT Core:
    - GatewayConfig
    - EdgeDescriptor
    - SamplingWindow
    - MachineMetadata
"""
import json
import abc
from typing import Dict


class ComplexEncoder(json.JSONEncoder):
    """Our common complex encoder to use when serializing a class instance to JSON.

    Example:
        edge_descriptor = EdgeDescriptor(...)
        js = json.dumps(edge_descriptor_1, cls=ComplexEncoder)

    For nested cases like the GatewayConfig, this encoder will also work recursively
    as long as the nested classes defines the reprJSON() method.

    Example:
        gateway_config = GatewayConfig(
            "gateway-test-proto",
            "registry-test-proto",
            "project-test-proto",
            "region-test-proto",
            [sampling_window],
            [machine_metadata.machine_id]
        )
        json_str = json.dumps(
            gateway_config, cls=ComplexEncoder, indent=4
        )
    """
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


class ComplexEncoderSerializable(abc.ABC):

    @abc.abstractmethod
    def reprJSON(self) -> Dict:
        """Every child class that wants to use the ComplexEncoder,
        should implement this method."""
        pass
