from enum import Enum
from typing import List

import pydantic

from classiq.interface.backend.quantum_backend_providers import AnalyzerProviderVendor
from classiq.interface.helpers.versioned_model import VersionedModel


class AvailabilityStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class DeviceType(str, Enum):
    SIMULATOR = "simulator"
    HARDWARE = "hardware"


class ExecutionInform(pydantic.BaseModel):
    backend_name: str = pydantic.Field(
        default=...,
        description="The name of the device",
    )
    backend_service_provider: AnalyzerProviderVendor = pydantic.Field(
        default=...,
        description="The name of the provider",
    )
    status: AvailabilityStatus = pydantic.Field(
        default=...,
        description="availability status of the hardware",
    )
    type: DeviceType = pydantic.Field(
        default=...,
        description="The type of the device",
    )
    max_qubits: int = pydantic.Field(
        default=...,
        description="number of qubits in the hardware",
    )


class ExecutionDevicesInform(VersionedModel):
    informs_params: List[ExecutionInform] = pydantic.Field(
        default=...,
        description="List of execution Information of all devices",
    )


class ExecutionInformRequestParams(pydantic.BaseModel):
    qubit_count: int = pydantic.Field(
        default=..., description="number of qubits in the data"
    )
