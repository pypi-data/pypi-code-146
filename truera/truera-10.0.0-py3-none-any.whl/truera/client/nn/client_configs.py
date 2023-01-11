from __future__ import annotations

#pylint: disable=unsupported-membership-test
from enum import Enum
from enum import unique
import logging
from logging import Logger
import typing
from typing import Dict, Optional, Sequence, Union

from pydantic.dataclasses import dataclass

from truera.protobuf.public.aiq import rnn_config_pb2 as rnn_config_proto
from truera.protobuf.public.aiq.rnn_config_pb2 import \
    NLPAttributionConfig  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.rnn_config_pb2 import \
    RNNAttributionConfig  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.rnn_config_pb2 import \
    RNNUIConfig  # pylint: disable=no-name-in-module

# Used for cache hash, associated with the background split. Some NN use cases do not need a background split, so this is the default string.
DEFAULT_NN_HASH_BG = 'default_nn_hash_bg'


def validate_config(obj, logger: Logger):
    logger.setLevel(logging.WARNING)
    pass_validation = True
    for field_name, field_def in typing.get_type_hints(type(obj)).items():

        value = getattr(obj, field_name)
        actual_type = type(value)
        comparison_type = field_def
        # Check optional Optional types
        comparison_type = getattr(comparison_type, '__args__', comparison_type)

        # Do a special check for these fields to make sure they are either None or a list/tuple
        if field_name in [
            'input_dimension_order', 'output_dimension_order',
            'internal_dimension_order'
        ]:
            if value and not (
                isinstance(value, tuple) or isinstance(value, list)
            ):
                logger.warning(
                    f"Incorrect Config Type: \t{field_name}: '{actual_type}' instead of 'list' or 'tuple'"
                )
                pass_validation = False
            else:
                continue
        '''
        Validation is: (None-is-OK and val is None) or Types-match
        not predicate is: not None-is-OK or val is not None and not Types-match

        Code equivalent:
        None-is-OK = isinstance(comparison_type, tuple) and type(None) in comparison_type
        Types-match = isinstance(actual_type, comparison_type)
        '''
        if (
            (
                not isinstance(comparison_type, tuple) or
                not (type(None) in comparison_type) or value is not None
            ) and not isinstance(value, comparison_type)
        ):
            logger.warning(
                f"Incorrect Config Type: \t{field_name}: '{actual_type}' instead of '{field_def}'"
            )
            pass_validation = False
    if not pass_validation:
        raise Exception('Misconfigured configuration. See warnings.')


@unique
class NNBackend(Enum):
    PYTORCH = 'pytorch'
    TENSORFLOW_V1 = 'tf_v1'
    TENSORFLOW_V2 = 'tf_v2'
    KERAS = 'keras'

    def get_backend(self):
        return 'tf' if 'tf' in self.value else self.value

    @classmethod
    def create_backend(cls, backend_str, backend_version=None):
        if backend_str.lower() in ['torch', 'pytorch']:
            return cls.PYTORCH
        elif backend_str.lower() in ['tf', 'tensorflow', 'tf2', 'tf1']:
            if (backend_version and
                int(backend_version) == 1) or backend_str.lower() == 'tf1':
                return cls.TENSORFLOW_V1
            elif (backend_version and
                  int(backend_version) == 2) or backend_str.lower() == 'tf2':
                return cls.TENSORFLOW_V2
            else:
                raise NotImplementedError(
                    'Please specify a backend version for Tensorflow.'
                )
        elif backend_str.lower() in ['keras']:
            return cls.KERAS
        raise NotImplementedError(
            'The {} backend is not supported.'.format(backend_str)
        )

    def _to_protobuf(self):
        if self.value == NNBackend.PYTORCH:
            return rnn_config_proto.NNBackend.Backend.PYTORCH
        elif self.value == NNBackend.TENSORFLOW_V1:
            return rnn_config_proto.NNBackend.Backend.TENSORFLOW_V1
        elif self.value == NNBackend.TENSORFLOW_V2:
            return rnn_config_proto.NNBackend.Backend.TENSORFLOW_V2
        elif self.value == NNBackend.KERAS:
            return rnn_config_proto.NNBackend.Backend.KERAS


@unique
class LayerAnchor(str, Enum):
    IN = 'in'
    OUT = 'out'

    def _to_protobuf(self):
        if self.value == LayerAnchor.IN.value:
            return rnn_config_proto.LayerAnchor.Anchor.IN
        elif self.value == LayerAnchor.OUT.value:
            return rnn_config_proto.LayerAnchor.Anchor.OUT

    @staticmethod
    def to_string(i: LayerAnchor) -> str:
        return str(i)

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_string(i: str) -> LayerAnchor:
        if i is None:
            return None
        elif i == LayerAnchor.IN.value:
            return LayerAnchor.IN
        elif i == LayerAnchor.OUT.value:
            return LayerAnchor.OUT
        else:
            raise ValueError(f"unhandled anchor {i}")

    def _to_string(self) -> str:
        return self.to_string(self)


@unique
class Layer(str, Enum):
    INPUT = 'tru_input_layer_const'
    OUTPUT = 'tru_output_layer_const'


@unique
class Dimension(Enum):
    BATCH = 1
    TIMESTEP = 2
    FEATURE = 3
    CLASS = 4
    NEURON = 5
    POSITION = 6
    EMBEDDING = 7


@unique
class ModelPartition(Enum):
    '''
    Used to initialize configuration.

    INPUT_OUTPUT: Data flows from input layer to the output layer of the model
    INPUT_INTERMEDIATE: Data flows from input layer to the intermediate layer of the model
    INTERMEDIATE_OUTPUT: Data flows from intermediate layer to the output layer of the model

    Cuts and anchors are defined in configuration appropriately which is helpful to store activations and attributions
    '''

    INPUT_OUTPUT = 0
    INPUT_INTERMEDIATE = 1
    INTERMEDIATE_OUTPUT = 2


class AttributionConfiguration:

    def validate(self):
        validate_config(self, self.logger)

    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
        validate_config(self, self.logger)


@dataclass(eq=True)
class RNNAttributionConfiguration(AttributionConfiguration):
    """
    RNNAttributionConfiguration keeps track of important parameters needed to run attributions on a model.

    Parameters
    =========================
    forward_padded (required): bool, The padding of the RNN.

    baseline_split (required): str, The split with the most representative data distribution. Usually one of train/validation/all.
        This split must be ingested into the system at run time.

    input_layer (required): str, The name of the layer to run attributions.
        Can also be a `truera.client.nn.client_configs.Layer.INPUT`.
    n_time_step_input (required): int, The number of input timesteps.
    n_features_input (required): int, The number of input features.

    output_layer (required): str, The name of the final layer that is being explained when examining model outputs.
        Can also be a `truera.client.nn.client_configs.Layer.OUTPUT`.
    n_time_step_output (required): int, The number of output timesteps.
    n_output_neurons (required): int, The number of output classes.

    Optional Parameters
    =========================
    n_baseline_records: int, The number of records to to generate a baseline for attributions.
        Higher numbers may increase reliability of attributions.
        If unspecified, a Truera selected default will be used.

    internal_layer: str, The name of an intermediate layer that is being explained when examining internal neuron outputs.
        This is used to explain neurons in a network.
    n_internal_neurons: int, The number of neurons in the internal tensor.

    input_anchor: client_configs.LayerAnchor, Determines the tensor to run attributions.
        It can be the `in` or `out` tensor of the `input_layer`. Defaults to `out`
    output_anchor: client_configs.LayerAnchor, determines the output tensor to explain.
        It can be the `in` or `out` tensor of the `output_layer`. Defaults to `out`
    internal_anchor: client_configs.LayerAnchor, Determines the internal tensor to run attributions.
        It can be the `in` or `out` tensor of the `internal_layer`. Defaults to `out`

    input_dimension_order: list/tuple[Dimension], The order of which input feature dimensions are expected.
        If not supplied, the input will be expected to be in (batch x n_time_step_input x n_features_input).
        If supplied, the dimensions must be a list of size 3, containing in any order: Dimension.BATCH, Dimension.TIMESTEP, Dimension.FEATURE
    output_dimension_order: list/tuple[Dimension], The order of which input feature dimensions are expected.
        If not supplied, the input will be expected to be in (batch x n_time_step_input x n_output_neurons)
        If supplied, the dimensions must be a list of size 3, containing in any order: Dimension.BATCH, Dimension.TIMESTEP, Dimension.CLASS
    internal_dimension_order: list/tuple[Dimension], The order of which input feature dimensions are expected.
        If not supplied, the input will be expected to be in (batch x n_time_step_input x n_internal_neurons)
        If supplied, the dimensions must be a list of size 3, containing in any order: Dimension.BATCH, Dimension.TIMESTEP, Dimension.NEURON

    use_cuda: bool, Whether to use CUDA for accelerated computing. Defaults to True
    use_training_mode: bool, Determines to set the model to training mode which could cause nondeterministic model behavior. Defaults to False
    """
    forward_padded: bool

    baseline_split: str

    input_layer: Union[str, Layer]
    n_time_step_input: int
    n_features_input: int

    output_layer: Union[str, Layer]
    n_time_step_output: int
    n_output_neurons: int

    n_baseline_records: Optional[int] = None

    internal_layer: Optional[str] = None
    n_internal_neurons: Optional[int] = None

    input_anchor: Optional[LayerAnchor] = None
    output_anchor: Optional[LayerAnchor] = None
    internal_anchor: Optional[LayerAnchor] = None

    input_dimension_order: Optional[Sequence[Dimension]] = None
    output_dimension_order: Optional[Sequence[Dimension]] = None
    internal_dimension_order: Optional[Sequence[Dimension]] = None

    use_cuda: Optional[bool] = True

    # Use training mode is a bug fix configuration in case of this issue: https://discuss.pytorch.org/t/cudnn-rnn-backward-can-only-be-called-in-training-mode/37622
    # If influence generation runs into that error, it will tell you to set this attribute.
    use_training_mode: Optional[bool] = False

    def _to_protobuf(self) -> RNNAttributionConfig():
        return RNNAttributionConfig(
            forward_padded=self.forward_padded,
            baseline_split=self.baseline_split,
            n_baseline_records=self.n_baseline_records,
            input_layer=str(self.input_layer),
            input_anchor=self.input_anchor._to_protobuf()
            if self.input_anchor is not None else None,
            n_time_step_input=self.n_time_step_input,
            n_features_input=self.n_features_input,
            output_layer=str(self.output_layer),
            output_anchor=self.output_anchor._to_protobuf()
            if self.output_anchor is not None else None,
            n_time_step_output=self.n_time_step_output,
            n_output_neurons=self.n_output_neurons,
            internal_layer=str(self.internal_layer),
            internal_anchor=self.internal_anchor._to_protobuf()
            if self.internal_anchor is not None else None,
            n_internal_neurons=self.n_internal_neurons
        )

    @staticmethod
    def from_dict(
        attr_config_dict: Dict[str, Union[str, int, float, bool]]
    ) -> RNNAttributionConfiguration:
        parsed_attr_config = {}
        parsed_attr_config["forward_padded"] = attr_config_dict.get(
            "forward_padded", False
        )

        parsed_attr_config["baseline_split"] = attr_config_dict.get(
            "baseline_split"
        )
        parsed_attr_config["n_baseline_records"] = attr_config_dict.get(
            "n_baseline_records"
        )

        parsed_attr_config["input_layer"] = attr_config_dict.get("input_layer")
        parsed_attr_config["input_anchor"] = LayerAnchor.__members__.get(
            attr_config_dict.get("input_anchor")
        )
        parsed_attr_config["n_time_step_input"] = attr_config_dict.get(
            "n_time_step_input"
        )
        parsed_attr_config["n_features_input"] = attr_config_dict.get(
            "n_features_input"
        )

        parsed_attr_config["output_layer"] = attr_config_dict.get(
            "output_layer"
        )
        parsed_attr_config["output_anchor"] = LayerAnchor.__members__.get(
            attr_config_dict.get("output_anchor")
        )
        parsed_attr_config["n_time_step_output"] = attr_config_dict.get(
            "n_time_step_output"
        )
        parsed_attr_config["n_output_neurons"] = attr_config_dict.get(
            "n_output_neurons"
        )

        parsed_attr_config["internal_layer"] = attr_config_dict.get(
            "internal_layer"
        )
        parsed_attr_config["internal_anchor"] = LayerAnchor.__members__.get(
            attr_config_dict.get("internal_anchor")
        )
        parsed_attr_config["n_internal_neurons"] = attr_config_dict.get(
            "n_internal_neurons"
        )
        return RNNAttributionConfiguration(**parsed_attr_config)


@dataclass(eq=True)
class NLPAttributionConfiguration(AttributionConfiguration):
    """
    NLPAttributionConfiguration keeps track of important parameters needed to run attributions on a model.

    Parameters
    =========================
    n_metrics_records (required): int, The number of records to use for metric calculations like accuracies, etc.

    embedding_layer (required): str, The name of the embedding layer to run attributions. 
        Can also be a `truera.client.nn.client_configs.Layer.INPUT`.

    output_layer (required): str, The name of the final layer that is being explained when examining model outputs. 
        Can also be a `truera.client.nn.client_configs.Layer.OUTPUT`.
    n_output_neurons (required): int, The number of neurons in the output layer.


    Optional Parameters
    =========================


    ref_token: str, Used for integrated gradients baseline. Typically a mask or informationless token.
    resolution: int, Used for integrated gradients baseline. The number of interpolation points to use from baseline to value.
    rebatch_size: int, Used for memory constraints with integrated gradients. Resolution will expand the inputsize multiplicatively. 
        If memory issues arise, choose rebatch size to bring the expanded batchsize back down.

    embedding_anchor: client_configs.LayerAnchor, Determines the tensor to run attributions.
        It can be the `in` or `out` tensor of the `embedding_anchor`. Defaults to `out`
    output_anchor: client_configs.LayerAnchor, determines the output tensor to explain.
        It can be the `in` or `out` tensor of the `output_layer`. Defaults to `out`
    
    input_dimension_order: list/tuple[Dimension], The order of which input feature dimensions are expected.
        If not supplied, the input will be expected to be in (batch x n_time_step_input x n_features_input).
        If supplied, the dimensions must be a list of size 3, containing in any order: Dimension.BATCH, Dimension.TIMESTEP, Dimension.FEATURE
    output_dimension_order: list/tuple[Dimension], The order of which input feature dimensions are expected.
        If not supplied, the input will be expected to be in (batch x n_time_step_input x n_output_neurons)
        If supplied, the dimensions must be a list of size 3, containing in any order: Dimension.BATCH, Dimension.TIMESTEP, Dimension.CLASS
    
    shuffle_data: bool, A flag on whether to shuffle the data.
    use_cuda: bool, Whether to use CUDA for accelerated computing. Defaults to True
    use_training_mode: bool, Determines to set the model to training mode which could cause nondeterministic model behavior. Defaults to False
    """
    n_metrics_records: int
    n_output_neurons: int

    input_layer: Optional[Union[str, Layer]
                         ] = None  # Unused. Use embedding_layer instead
    input_anchor: Optional[LayerAnchor] = LayerAnchor.IN

    embedding_layer: Optional[Union[str, Layer]] = None
    embedding_anchor: Optional[LayerAnchor] = LayerAnchor.OUT

    # TODO: R&D work. Need to modify and work towards production
    # qoi_neuron -> Neuron on which QoI is placed when the toCut is in intermediate layer
    # config -> Determines whether we are going "Input -> Intermediate" (coded as 0) or "Intermediate -> Output" (coded as 1)
    partition_at: Optional[ModelPartition] = None
    qoi_neuron: Optional[int] = None

    baseline_type: Optional[str] = "dynamic"
    ref_token: Optional[str] = None
    resolution: Optional[int] = None
    rebatch_size: Optional[int] = None

    output_layer: Optional[Union[str, Layer]] = None
    output_anchor: Optional[LayerAnchor] = None

    attribution_layer: Optional[Union[str, Layer]] = None
    attribution_anchor: Optional[LayerAnchor] = None

    input_dimension_order: Optional[Sequence[Dimension]] = None
    output_dimension_order: Optional[Sequence[Dimension]] = None

    shuffle_data: Optional[bool] = False
    use_cuda: Optional[bool] = True

    # Use training mode is a bug fix configuration in case of this issue: https://discuss.pytorch.org/t/cudnn-rnn-backward-can-only-be-called-in-training-mode/37622
    # If influence generation runs into that error, it will tell you to set this attribute.
    use_training_mode: Optional[bool] = False

    def __post_init__(self):
        super().__post_init__()
        self.embedding_layer = self.embedding_layer or Layer.INPUT
        self.output_layer = self.output_layer or Layer.OUTPUT

    def _to_protobuf(self) -> NLPAttributionConfig():
        return NLPAttributionConfig(
            n_metrics_records=self.n_metrics_records,
            embedding_layer=str(self.embedding_layer),
            embedding_anchor=self.embedding_anchor._to_protobuf()
            if self.embedding_anchor is not None else None,
            output_layer=str(self.output_layer),
            output_anchor=self.output_anchor._to_protobuf()
            if self.output_anchor is not None else None,
            n_output_neurons=self.n_output_neurons,
            ref_token=self.ref_token,
            shuffle_data=self.shuffle_data,
            resolution=self.resolution,
            rebatch_size=self.rebatch_size,
            use_training_mode=self.use_training_mode,
        )

    @staticmethod
    def from_dict(
        attr_config_dict: Dict[str, Union[str, int, float, bool]]
    ) -> NLPAttributionConfiguration:
        parsed_attr_config = {}

        parsed_attr_config["baseline_type"] = attr_config_dict.get(
            "baseline_type"
        )

        parsed_attr_config["n_metrics_records"] = int(
            attr_config_dict.get("n_metrics_records")
        )

        parsed_attr_config["embedding_layer"] = attr_config_dict.get(
            "embedding_layer"
        )

        if (attr_config_dict.get("embedding_anchor") == 'None'):
            parsed_attr_config["embedding_anchor"] = None
        else:
            parsed_attr_config["embedding_anchor"
                              ] = LayerAnchor.__members__.get(
                                  attr_config_dict.get("embedding_anchor")
                              )

        parsed_attr_config["output_layer"] = attr_config_dict.get(
            "output_layer"
        )

        parsed_attr_config["n_output_neurons"] = int(
            attr_config_dict.get("n_output_neurons")
        )

        if (attr_config_dict.get("output_anchor") == "None"):
            parsed_attr_config["output_anchor"] = None
        else:
            parsed_attr_config["output_anchor"] = LayerAnchor.__members__.get(
                attr_config_dict.get("output_anchor")
            )

        parsed_attr_config["shuffle_data"] = bool(
            attr_config_dict.get("shuffle_data")
        )

        if (attr_config_dict.get("rebatch_size") == 'None'):
            parsed_attr_config["rebatch_size"] = None
        else:
            parsed_attr_config["rebatch_size"] = int(
                attr_config_dict.get("rebatch_size")
            )
        parsed_attr_config["ref_token"] = attr_config_dict.get("ref_token")
        if (attr_config_dict.get("resolution") == 'None'):
            parsed_attr_config["resolution"] = None
        else:
            parsed_attr_config["resolution"] = int(
                attr_config_dict.get("resolution")
            )

        return NLPAttributionConfiguration(**parsed_attr_config)


@dataclass(eq=True)
class RNNUserInterfaceConfiguration:
    """
    RNNUserInterfaceConfiguration keeps track of UI preferences.

    Parameters
    =========================
    default_threshold (optional): float, determines the default threshold used in the UI for decision boundaries.
        if not provided, the UI will assume the output is a 0.0 to 1.0 probability, and a 0.5 threshold will be used.
    """
    default_classification_threshold: Optional[float] = None

    def validate(self):
        validate_config(self, self.logger)

    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
        validate_config(self, self.logger)

    def _to_protobuf(self) -> RNNUIConfig:
        return RNNUIConfig(
            default_classification_threshold=self.
            default_classification_threshold
        )
