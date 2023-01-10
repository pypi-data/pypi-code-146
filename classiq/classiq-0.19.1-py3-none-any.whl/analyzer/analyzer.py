"""Analyzer module, implementing facilities for analyzing circuits using Classiq platform."""
import json
import webbrowser
from importlib.util import find_spec
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin

import plotly.graph_objects as go

from classiq.interface.analyzer import analysis_params, result as analysis_result
from classiq.interface.analyzer.analysis_params import (
    AnalysisComparisonParams,
    ComparisonProperties,
)
from classiq.interface.backend.quantum_backend_providers import AnalyzerProviderVendor
from classiq.interface.generator import result as generator_result
from classiq.interface.generator.model import Model, Preferences
from classiq.interface.server import routes

from classiq._internals import client
from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import Asyncify
from classiq._internals.type_validation import validate_type
from classiq.analyzer.analyzer_utilities import (
    AnalyzerUtilities,
    DeviceName,
    HardwareGraphs,
    ProviderAvailableDevices,
    ProviderNameEnum,
)
from classiq.analyzer.generate_graphs import (
    _create_gate_histogram,
    _create_heatmap_graph,
)
from classiq.analyzer.url_utils import circuit_page_uri, client_ide_base_url
from classiq.exceptions import ClassiqAnalyzerError
from classiq.model_designer.model_designer import ModelDesigner

find_ipywidgets = find_spec("ipywidgets")
VBox = Any

if find_ipywidgets is not None:
    from ipywidgets import VBox  # type: ignore[import, no-redef]

    from classiq._analyzer_extras.interactive_hardware import InteractiveHardware


class Analyzer(AnalyzerUtilities, metaclass=Asyncify):
    """Analyzer is the wrapper object for all analysis capabilities."""

    def __init__(self, circuit: generator_result.GeneratedCircuit):
        """Init self.

        Args:
            circuit (): The circuit to be analyzed.
        """
        if circuit.qasm is None:
            raise ClassiqAnalyzerError(
                "Analysis requires a circuit with valid QASM code"
            )
        self._params: analysis_params.AnalysisParams = analysis_params.AnalysisParams(
            qasm=circuit.qasm
        )
        self.circuit: generator_result.GeneratedCircuit = circuit
        self.qc_graph: Optional[go.Figure] = None
        self.heatmap: Optional[go.Figure] = None
        self.gate_histogram: Optional[go.Figure] = None
        self.hardware_comparison_table: Optional[go.Figure] = None
        self.available_devices: ProviderAvailableDevices = dict()
        self.hardware_graphs: HardwareGraphs = dict()

    async def analyze_async(self) -> analysis_result.Analysis:
        """Runs the circuit analysis.

        Returns:
            The analysis result.
        """
        result = await ApiWrapper.call_analysis_task(self._params)

        details = validate_type(
            obj=result,
            expected_type=analysis_result.Analysis,
            operation="Analysis",
            exception_type=ClassiqAnalyzerError,
        )

        dashboard_path = routes.ANALYZER_DASHBOARD
        self._open_route(path=dashboard_path)
        return details

    async def analyzer_app_async(self) -> None:
        """Opens the analyzer app with synthesis interactive results.

        Returns:
            None.
        """
        result = await ApiWrapper.call_analyzer_app(self.circuit)
        webbrowser.open_new_tab(
            urljoin(
                client_ide_base_url(),
                circuit_page_uri(
                    circuit_id=result.id, circuit_version=self.circuit.version
                ),
            )
        )

    async def get_available_devices_async(
        self, providers: Optional[List[ProviderNameEnum]] = None
    ) -> Dict[ProviderNameEnum, List[DeviceName]]:
        """Returns dict of the available devices by the providers. only devices
        with sufficient number of qubits are returns

        Args: providers (): List of providers (string or `AnalyzerProviderVendor`).
        if None, the table include all the available hardware.

        Returns:
            available devices (): dict of the available devices (Dict[str,List[str]]).
        """
        if providers is None:
            providers = list(AnalyzerProviderVendor)
        await self.request_available_devices_async(providers=providers)
        return {
            provider: self._filter_devices_by_qubits_count(provider)
            for provider in providers
        }

    async def get_qubits_connectivity_async(self) -> None:
        """create a network connectivity graph of the analysed circuit.

        Returns:
            None.
        """
        result = await ApiWrapper.call_qubits_connectivity_graphs_task(self._params)
        self.qc_graph = go.Figure(json.loads(result.details))

    async def plot_qubits_connectivity_async(self) -> None:
        """plot the connectivity graph. if it has not been created it, it first creates the graph.

        Returns:
            None.
        """
        if self.qc_graph is None:
            await self.get_qubits_connectivity_async()
        self.qc_graph.show()  # type: ignore[union-attr]

    async def plot_hardware_connectivity_async(
        self,
        provider: Optional[ProviderNameEnum] = None,
        device: Optional[DeviceName] = None,
    ) -> VBox:
        """plot the hardware_connectivity graph. It is required to required  install the
        analyzer_sdk extra.

        Args:
            provider (): provider name (optional - string or `AnalyzerProviderVendor`).
            device (): device name (optional - string).
        Returns:
         hardware_connectivity_graph (): interactive graph.
        """

        self._validate_analyzer_extra()
        interactive_hardware = InteractiveHardware(
            circuit=self.circuit,
            params=self._params,
            available_devices=self.available_devices,
            hardware_graphs=self.hardware_graphs,
        )
        await interactive_hardware.enable_interactivity_async()
        if provider is not None:
            interactive_hardware.providers_combobox.value = provider
            if device is not None:
                interactive_hardware.devices_combobox.value = device

        return interactive_hardware.show_interactive_graph()

    async def get_hardware_comparison_table_async(
        self,
        providers: Optional[List[Union[str, AnalyzerProviderVendor]]] = None,
        devices: Optional[List[str]] = None,
    ) -> None:
        """create a comparison table between the transpiled circuits result on different hardware.
        The  comparison table included the depth, multi qubit gates count,and total gates count of the circuits.

        Args: providers (): List of providers (string or `AnalyzerProviderVendor`). if None, the table include all
        the available hardware.
        devices (): List of devices (string). if None, the table include all the available devices of the selected
        providers.
        Returns: None.
        """
        if providers is None:
            providers = list(AnalyzerProviderVendor)
        params = analysis_params.AnalysisHardwareListParams(
            qasm=self._params.qasm, providers=providers, devices=devices
        )
        result = await ApiWrapper.call_table_graphs_task(params=params)
        self.hardware_comparison_table = go.Figure(json.loads(result.details))

    async def plot_hardware_comparison_table_async(
        self,
        providers: Optional[List[Union[str, AnalyzerProviderVendor]]] = None,
        devices: Optional[List[str]] = None,
    ) -> None:
        """plot the comparison table. if it has not been created it, it first creates the table using all the
        available hardware.

        Returns:
            None.
        """
        await self._hardware_comparison_condition_async(
            providers=providers, devices=devices
        )
        self.hardware_comparison_table.show()  # type: ignore[union-attr]

    async def get_heatmap_async(self) -> None:
        """create a heatmap of the analysed circuit.

        Returns:
            None.
        """
        result = await ApiWrapper.call_heatmap_graphs(self._params)
        self.heatmap = _create_heatmap_graph(result, self.circuit.qubit_count)

    async def plot_heatmap_async(self) -> None:
        """plot the circuit heatmap. if it has not been created it, it will create the graph.

        Returns:
            None.
        """
        if self.heatmap is None:
            await self.get_heatmap_async()
        self.heatmap.show()  # type: ignore[union-attr]

    async def plot_gate_histogram_async(self) -> None:
        """plot the circuit gate histogram. if it has not been created it, it will create the graph.

        Returns:
            None.
        """
        if self.gate_histogram is None:
            await self.get_gate_histogram_async()
        self.gate_histogram.show()  # type: ignore[union-attr]

    async def get_gate_histogram_async(self) -> None:
        """create a gate histogram of the analysed circuit.

        Returns:
            None.
        """
        result = await ApiWrapper.call_gate_histogram_graphs(params=self._params)
        self.gate_histogram = _create_gate_histogram(
            result=result, num_qubits=self.circuit.qubit_count
        )

    async def hardware_aware_resynthesize_async(
        self, device: str, provider: Union[str, AnalyzerProviderVendor]
    ) -> generator_result.GeneratedCircuit:
        """resynthesize the analyzed circuit using its original model, and a new  backend preferences.

        Args:
            provider (): Provider company or cloud for the requested backend (string or `AnalyzerProviderVendor`).
            device (): Name of the requested backend"
        Returns:
            circuit (): resynthesize circuit (`GeneratedCircuit`).
        """

        update_preferences = self._validated_update_preferences(
            device=device, provider=provider
        )

        model_designer = ModelDesigner()
        model_designer._model = self.circuit.model.copy(deep=True)  # type: ignore[union-attr]
        return await model_designer.synthesize_async(preferences=update_preferences)

    async def optimized_hardware_resynthesize_async(
        self,
        comparison_property: Union[str, ComparisonProperties],
        providers: Optional[List[Union[str, AnalyzerProviderVendor]]] = None,
        devices: Optional[List[str]] = None,
    ) -> generator_result.GeneratedCircuit:
        """Re-synthesize the analyzed circuit using its original model, and a new backend preferences, which is the
         devices with the best fit to the selected comparison property.

        Args: comparison_property (): A comparison properties using to compare between the devices (string or
        `ComparisonProperties`).
        providers (): List of providers (string or `AnalyzerProviderVendor`). If None, the comparison include all the
        available hardware.
        devices (): List of devices (string). If None, the comparison include all the available devices of the selected
        providers.
        Returns: circuit (): resynthesize circuit (`GeneratedCircuit`).
        """
        optimized_device, optimized_provider = await self._get_optimized_hardware_async(
            providers=providers,
            devices=devices,
            comparison_property=comparison_property,
        )
        return await self.hardware_aware_resynthesize_async(
            provider=optimized_provider, device=optimized_device
        )

    async def _get_optimized_hardware_async(
        self,
        comparison_property: Union[str, ComparisonProperties],
        providers: Optional[List[Union[str, AnalyzerProviderVendor]]] = None,
        devices: Optional[List[str]] = None,
    ) -> Tuple[str, str]:
        await self._hardware_comparison_condition_async(
            providers=providers, devices=devices
        )
        optimized_device, optimized_provider = self._choose_optimized_hardware(
            comparison_property=comparison_property
        )
        return optimized_device, optimized_provider

    def _choose_optimized_hardware(
        self, comparison_property: Union[str, ComparisonProperties]
    ) -> Tuple[str, str]:
        comparison_params = AnalysisComparisonParams(property=comparison_property)
        if not isinstance(self.hardware_comparison_table, go.Figure):
            raise ClassiqAnalyzerError(
                "The analyzer does not contains a valid hardware comparison table"
            )
        column_names = self.hardware_comparison_table.data[0].header.values
        property_index = column_names.index(comparison_params.property.upper())

        sort_button = self.hardware_comparison_table.layout.updatemenus[0]
        sort_data = sort_button.buttons[property_index].args[0]["cells"]["values"]
        return sort_data[0][0], sort_data[1][0]

    def _validated_update_preferences(
        self, device: str, provider: Union[str, AnalyzerProviderVendor]
    ) -> Preferences:

        if not isinstance(self.circuit.model, Model):
            raise ClassiqAnalyzerError("The circuit does not contains a valid model")

        preferences_dict = self.circuit.model.preferences.dict()
        preferences_dict.update(
            dict(backend_service_provider=provider, backend_name=device)
        )

        return Preferences.parse_obj(preferences_dict)

    async def _hardware_comparison_condition_async(
        self,
        providers: Optional[List[Union[str, AnalyzerProviderVendor]]] = None,
        devices: Optional[List[str]] = None,
    ) -> None:
        if (
            providers is not None
            or devices is not None
            or self.hardware_comparison_table is None
        ):
            await self.get_hardware_comparison_table_async(
                providers=providers, devices=devices
            )

    @staticmethod
    def _open_route(path: str) -> None:
        backend_uri = client.client().get_backend_uri()
        webbrowser.open_new_tab(f"{backend_uri}{path}")

    @staticmethod
    def _validate_analyzer_extra() -> None:
        if find_ipywidgets is None:
            raise ClassiqAnalyzerError(
                "To use this method, please install the `analyzer sdk`. Run the  \
                following line: - pip install classiq[analyzer_sdk]"
            )
