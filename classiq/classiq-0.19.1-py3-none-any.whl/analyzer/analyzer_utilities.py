from typing import Dict, List, Union

from classiq.interface.analyzer import analysis_params
from classiq.interface.backend.quantum_backend_providers import AnalyzerProviderVendor
from classiq.interface.generator.result import GeneratedCircuit

from classiq._internals.api_wrapper import ApiWrapper
from classiq.exceptions import ClassiqAnalyzerError

DeviceName = str
ProviderName = str
ProviderLowerName = str
HardwareGraphJson = str
Availability = bool
ProviderNameEnum = Union[ProviderName, AnalyzerProviderVendor]
AvailableDevices = Dict[DeviceName, Availability]
ProviderAvailableDevices = Dict[ProviderLowerName, AvailableDevices]
HardwareGraphs = Dict[DeviceName, HardwareGraphJson]


class AnalyzerUtilities:
    def __init__(
        self,
        params: analysis_params.AnalysisParams,
        circuit: GeneratedCircuit,
        available_devices: ProviderAvailableDevices,
        hardware_graphs: HardwareGraphs,
    ):

        self._params: analysis_params.AnalysisParams = params
        self.circuit: GeneratedCircuit = circuit
        self.available_devices = available_devices
        self.hardware_graphs = hardware_graphs

    async def request_available_devices_async(
        self, providers: List[ProviderNameEnum]
    ) -> None:
        requested_providers = self._requested_providers_filter(providers)
        if not requested_providers:
            return
        params = analysis_params.AnalysisOptionalDevicesParams(
            qubit_count=self.circuit.qubit_count, providers=requested_providers
        )
        result = await ApiWrapper.call_available_devices_task(params=params)
        self.available_devices.update(result.devices.dict())

    async def request_hardware_connectivity_async(
        self, provider: ProviderNameEnum, device: DeviceName
    ) -> None:
        await self._device_validation_async(provider=provider, device=device)
        if self.hardware_graphs.get(device) is not None:
            return
        params = analysis_params.AnalysisHardwareParams(
            qasm=self._params.qasm, provider=provider, device=device
        )
        result = await ApiWrapper.call_hardware_connectivity_task(params=params)
        self.hardware_graphs.update({device: result.details})

    async def _device_validation_async(
        self, provider: ProviderNameEnum, device: DeviceName
    ) -> None:
        await self.request_available_devices_async(providers=[provider])
        provider_lower_name = _to_lower_case(provider)
        available_device_dict = self.available_devices
        if available_device_dict[provider_lower_name].get(device) is False:
            raise ClassiqAnalyzerError(device + " doesn't have enough qubits.")
        elif available_device_dict[provider_lower_name].get(device) is None:
            raise ClassiqAnalyzerError(
                device + " is not available by " + provider + " providers server."
            )

    def _requested_providers_filter(
        self, providers: List[ProviderNameEnum]
    ) -> List[ProviderNameEnum]:
        return list(
            filter(
                lambda provider: self.available_devices.get(_to_lower_case(provider))
                is None,
                providers,
            )
        )

    def _filter_devices_by_qubits_count(
        self, provider: ProviderNameEnum
    ) -> List[DeviceName]:
        device_avail_dict = self.available_devices[_to_lower_case(provider)]
        return list(
            filter(lambda device: device_avail_dict[device], device_avail_dict.keys())
        )


def _to_lower_case(name: ProviderNameEnum) -> ProviderLowerName:
    return name.lower().replace(" ", "_")
