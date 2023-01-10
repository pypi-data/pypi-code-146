import itertools

from classiq.interface.generator.amplitude_estimation import AmplitudeEstimation
from classiq.interface.generator.amplitude_loading import AmplitudeLoading
from classiq.interface.generator.arith.arithmetic import Arithmetic, ArithmeticOracle
from classiq.interface.generator.arith.binary_ops import (
    Adder,
    BitwiseAnd,
    BitwiseOr,
    BitwiseXor,
    CyclicShift,
    Equal,
    GreaterEqual,
    GreaterThan,
    LessEqual,
    LessThan,
    LShift,
    Max,
    Min,
    Multiplier,
    NotEqual,
    RShift,
    Subtractor,
)
from classiq.interface.generator.arith.logical_ops import LogicalAnd, LogicalOr
from classiq.interface.generator.arith.unary_ops import BitwiseInvert, Negation, Sign
from classiq.interface.generator.credit_risk_example.linear_gci import LinearGCI
from classiq.interface.generator.credit_risk_example.weighted_adder import WeightedAdder
from classiq.interface.generator.entangler_params import (
    GridEntangler,
    HypercubeEntangler,
    TwoDimensionalEntangler,
)
from classiq.interface.generator.exponentiation import Exponentiation
from classiq.interface.generator.finance import Finance, FinanceModels, FinancePayoff
from classiq.interface.generator.function_param_library import FunctionParamLibrary
from classiq.interface.generator.grover_operator import GroverOperator
from classiq.interface.generator.hadamard_amp_load import HadamardAmpLoad
from classiq.interface.generator.hardware_efficient_ansatz import (
    HardwareEfficientAnsatz,
)
from classiq.interface.generator.hartree_fock import HartreeFock
from classiq.interface.generator.hva import HVA
from classiq.interface.generator.identity import Identity
from classiq.interface.generator.inequality_mixer import InequalityMixer
from classiq.interface.generator.linear_pauli_rotations import LinearPauliRotations
from classiq.interface.generator.mcu import Mcu
from classiq.interface.generator.mcx import Mcx
from classiq.interface.generator.qft import QFT
from classiq.interface.generator.randomized_benchmarking import RandomizedBenchmarking
from classiq.interface.generator.sparse_amp_load import SparseAmpLoad
from classiq.interface.generator.standard_gates.standard_gates_param_list import (
    standard_gate_function_param_library,
)
from classiq.interface.generator.standard_gates.u_gate import UGate
from classiq.interface.generator.state_preparation import StatePreparation
from classiq.interface.generator.state_propagator import StatePropagator
from classiq.interface.generator.suzuki_trotter import SuzukiTrotter
from classiq.interface.generator.ucc import UCC
from classiq.interface.generator.unitary_gate import UnitaryGate
from classiq.interface.generator.user_defined_function_params import CustomFunction

function_param_library_without_self_reference: FunctionParamLibrary = (
    FunctionParamLibrary(
        param_list=itertools.chain(
            {
                StatePreparation,
                StatePropagator,
                QFT,
                BitwiseAnd,
                BitwiseOr,
                BitwiseXor,
                BitwiseInvert,
                Adder,
                Arithmetic,
                ArithmeticOracle,
                Sign,
                Equal,
                NotEqual,
                GreaterThan,
                GreaterEqual,
                LessThan,
                LessEqual,
                Negation,
                LogicalAnd,
                LogicalOr,
                Subtractor,
                RShift,
                LShift,
                CyclicShift,
                TwoDimensionalEntangler,
                Finance,
                FinanceModels,
                FinancePayoff,
                HypercubeEntangler,
                AmplitudeEstimation,
                SparseAmpLoad,
                GridEntangler,
                HadamardAmpLoad,
                GroverOperator,
                Mcx,
                Mcu,
                CustomFunction,
                HardwareEfficientAnsatz,
                UnitaryGate,
                WeightedAdder,
                LinearPauliRotations,
                Multiplier,
                LinearGCI,
                HartreeFock,
                UCC,
                Min,
                Max,
                Exponentiation,
                SuzukiTrotter,
                Identity,
                RandomizedBenchmarking,
                HVA,
                InequalityMixer,
                UGate,
                AmplitudeLoading,
            },
            standard_gate_function_param_library.param_list,
        )
    )
)
