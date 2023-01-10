import base64
import enum
import io
from datetime import datetime
from pathlib import Path
from typing import Collection, Dict, List, Optional, Tuple, Union

import pydantic
from PIL import Image

from classiq.interface.backend.backend_preferences import BackendPreferences
from classiq.interface.backend.quantum_backend_providers import ProviderVendor
from classiq.interface.executor import quantum_program
from classiq.interface.executor.quantum_instruction_set import QuantumInstructionSet
from classiq.interface.executor.register_initialization import RegisterInitialization
from classiq.interface.generator.model.model import Model
from classiq.interface.generator.model.preferences.preferences import (
    CustomHardwareSettings,
    QuantumFormat,
)
from classiq.interface.generator.synthesis_metrics import SynthesisMetrics
from classiq.interface.helpers.versioned_model import VersionedModel

from classiq._internals.registers_initialization import (
    InitialConditions,
    RegisterName,
    get_registers_from_generated_functions,
)
from classiq.exceptions import (
    ClassiqDefaultQuantumProgramError,
    ClassiqStateInitializationError,
)

_MAXIMUM_STRING_LENGTH = 250

IOQubitMapping = Dict[str, Tuple[int, ...]]


class LongStr(str):
    def __repr__(self):
        if len(self) > _MAXIMUM_STRING_LENGTH:
            length = len(self)
            return f'"{self[:4]}...{self[-4:]}" (length={length})'
        return super().__repr__()


class QasmVersion(str, enum.Enum):
    V2 = "2.0"
    V3 = "3.0"


class HardwareData(pydantic.BaseModel):
    _is_default: bool = pydantic.PrivateAttr(default=False)
    custom_hardware_settings: CustomHardwareSettings
    backend_preferences: Optional[BackendPreferences]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._is_default = (
            self.custom_hardware_settings.is_default
            and self.backend_preferences is None
        )

    @property
    def is_default(self) -> bool:
        return self._is_default


class CircuitWithOutputFormats(pydantic.BaseModel):
    outputs: Dict[QuantumFormat, str]
    qasm_version: QasmVersion

    @pydantic.validator("outputs")
    def reformat_long_string_output_formats(
        cls, outputs: Dict[QuantumFormat, str]
    ) -> Dict[QuantumFormat, LongStr]:
        return {key: LongStr(value) for key, value in outputs.items()}

    @property
    def qasm(self) -> Optional[str]:
        return self.outputs.get(QuantumFormat.QASM)

    @property
    def qsharp(self) -> Optional[str]:
        return self.outputs.get(QuantumFormat.QSHARP)

    @property
    def qir(self) -> Optional[str]:
        return self.outputs.get(QuantumFormat.QIR)

    @property
    def ionq(self) -> Optional[str]:
        return self.outputs.get(QuantumFormat.IONQ)

    @property
    def cirq_json(self) -> Optional[str]:
        return self.outputs.get(QuantumFormat.CIRQ_JSON)

    @property
    def qasm_cirq_compatible(self) -> Optional[str]:
        return self.outputs.get(QuantumFormat.QASM_CIRQ_COMPATIBLE)

    @property
    def output_format(self) -> List[QuantumFormat]:
        return list(self.outputs.keys())


class TranspiledCircuitData(CircuitWithOutputFormats):
    depth: int
    count_ops: Dict[str, int]
    logical_to_physical_input_qubit_map: List[int]
    logical_to_physical_output_qubit_map: List[int]


class GeneratedCircuit(VersionedModel, CircuitWithOutputFormats):
    qubit_count: int
    transpiled_circuit: Optional[TranspiledCircuitData]
    image_raw: Optional[str]
    interactive_html: Optional[str]
    synthesis_metrics: Optional[SynthesisMetrics]
    analyzer_data: Dict
    hardware_data: HardwareData
    logical_input_qubit_mapping: IOQubitMapping = pydantic.Field(default_factory=dict)
    logical_output_qubit_mapping: IOQubitMapping = pydantic.Field(default_factory=dict)
    physical_input_qubit_mapping: IOQubitMapping = pydantic.Field(default_factory=dict)
    physical_output_qubit_mapping: IOQubitMapping = pydantic.Field(default_factory=dict)
    model: Optional[Model] = None

    def show(self) -> None:
        self.image.show()

    @property
    def image(self):
        if self.image_raw is None:
            raise ValueError("Missing image. Set draw_image=True to create the image.")
        return Image.open(io.BytesIO(base64.b64decode(self.image_raw)))

    def save_results(self, filename: Optional[Union[str, Path]] = None) -> None:
        """
        Saves generated circuit results as json.
            Parameters:
                filename (Union[str, Path]): Optional, path + filename of file.
                                             If filename supplied add `.json` suffix.

            Returns:
                  None
        """
        if filename is None:
            time_stamp = datetime.now().isoformat()
            filename = f"synthesised_circuit_{time_stamp}.json"

        with open(filename, "w") as file:
            file.write(self.json(indent=4))

    def _hardware_unaware_program_code(
        self,
    ) -> Tuple[Optional[str], QuantumInstructionSet]:
        if self.transpiled_circuit is not None:
            return self.transpiled_circuit.qasm, QuantumInstructionSet.QASM
        elif self.qasm is not None:
            return self.qasm, QuantumInstructionSet.QASM
        elif self.qsharp is not None:
            return self.qsharp, QuantumInstructionSet.QSHARP
        elif self.ionq is not None:
            return self.ionq, QuantumInstructionSet.IONQ
        return None, QuantumInstructionSet.QASM

    def _default_program_code(self) -> Tuple[Optional[str], QuantumInstructionSet]:
        if self.hardware_data.backend_preferences is None:
            return self._hardware_unaware_program_code()

        backend_provider = (
            self.hardware_data.backend_preferences.backend_service_provider
        )
        if backend_provider == ProviderVendor.IONQ and self.ionq:
            return self.ionq, QuantumInstructionSet.IONQ
        elif backend_provider == ProviderVendor.AZURE_QUANTUM and self.qsharp:
            return self.qsharp, QuantumInstructionSet.QSHARP
        return (
            getattr(self.transpiled_circuit, "qasm", None),
            QuantumInstructionSet.QASM,
        )

    def to_base_program(self) -> quantum_program.QuantumBaseProgram:
        code, syntax = self._default_program_code()
        if code is None:
            raise ClassiqDefaultQuantumProgramError
        return quantum_program.QuantumBaseProgram(
            code=code,
            syntax=syntax,
        )

    def to_program(
        self, initial_values: Optional[InitialConditions] = None
    ) -> quantum_program.QuantumProgram:
        code, syntax = self._default_program_code()
        if code is None:
            raise ClassiqDefaultQuantumProgramError
        if initial_values is not None:
            registers_initialization = self.get_registers_initialization(
                initial_values=initial_values
            )
        else:
            registers_initialization = None
        return quantum_program.QuantumProgram(
            code=code,
            syntax=syntax,
            output_qubits_map=self.physical_output_qubit_mapping,
            registers_initialization=registers_initialization,
        )

    def get_registers(self, register_names: Collection[RegisterName]):
        if self.synthesis_metrics is None:
            raise ClassiqStateInitializationError(
                "The circuit doesn't contain synthesis_metrics."
            )
        return get_registers_from_generated_functions(
            generated_functions=self.synthesis_metrics.generated_functions,
            register_names=register_names,
        )

    def get_registers_initialization(
        self,
        initial_values: InitialConditions,
    ) -> Dict[RegisterName, RegisterInitialization]:
        registers = self.get_registers(
            register_names=initial_values.keys(),
        )
        registers_initialization = RegisterInitialization.initialize_registers(
            registers=registers, initial_conditions=initial_values.values()
        )
        return registers_initialization

    @pydantic.validator("image_raw", "interactive_html")
    def reformat_long_strings(cls, v):
        if v is None:
            return v
        return LongStr(v)
