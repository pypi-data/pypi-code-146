from abc import ABC
from abc import abstractmethod
from dataclasses import asdict
from dataclasses import dataclass
import logging
from logging import Logger
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type

import numpy as np
from trulens.utils.typing import TensorLike

from truera.client.nn import NNBackend as NNB
from truera.client.nn import wrappers as base
from truera.client.nn.client_configs import AttributionConfiguration
from truera.client.nn.client_configs import Dimension
from truera.client.nn.client_configs import Layer
from truera.client.nn.client_configs import LayerAnchor


class RequiredFileNotFoundException(Exception):

    def __init__(self, message):
        self.message = message


class ArgValidationException(Exception):

    def __init__(self, message):
        self.message = message


class WrapperOutputValidationException(Exception):

    def __init__(self, message):
        self.message = message


@dataclass(eq=True)
class ParamValidationContainer:
    input_seq_dimension: Dimension
    input_data_dimension: Dimension
    config_input_seq_param: int
    config_input_data_param: int
    config_input_seq_param_str: str
    config_input_data_param_str: str
    input_dimension_order_str: str
    output_dimension_order_str: str
    expected_labels_shape: int
    input_data_key: str
    seq_2_seq: bool


class VerifyHelper(ABC):

    def __init__(
        self,
        model_input_type: Optional[str] = None,
        model_output_type: Optional[str] = None,
        attr_config: Optional[AttributionConfiguration] = None,
        model: Optional[NNB.Model] = None,
        split_load_wrapper: Optional[base.Wrappers.SplitLoadWrapper] = None,
        model_run_wrapper: Optional[base.Wrappers.ModelRunWrapper] = None,
        model_load_wrapper: Optional[base.Wrappers.ModelLoadWrapper] = None,
    ):
        self.set_input_type(model_input_type)
        self.set_output_type(model_output_type)

        self.add_attr_config(attr_config)
        self.add_model(model)

        self.add_split_load_wrapper(split_load_wrapper)
        self.add_model_run_wrapper(model_run_wrapper)
        self.add_model_load_wrapper(model_load_wrapper)

        self.param_validation = self._get_named_parameters()

    def set_output_type(self, model_output_type):
        if model_output_type is not None:
            self.model_output_type = model_output_type

    def set_input_type(self, model_input_type):
        if model_input_type is not None:
            self.model_input_type = model_input_type

    def add_attr_config(self, attr_config: AttributionConfiguration):
        if attr_config is not None:
            self.attr_config = attr_config
            self.attr_config_cls_name = str(type(attr_config))

    def add_model(self, model: NNB.Model):
        if model is not None:
            self.model = model

    def add_split_load_wrapper(
        self, split_load_wrapper: base.Wrappers.SplitLoadWrapper
    ):
        if split_load_wrapper is not None:
            self.split_load_wrapper = split_load_wrapper

    def add_model_run_wrapper(
        self, model_run_wrapper: base.Wrappers.ModelRunWrapper
    ):
        if model_run_wrapper is not None:
            self.model_run_wrapper = model_run_wrapper

    def add_model_load_wrapper(
        self, model_load_wrapper: base.Wrappers.ModelLoadWrapper
    ):
        if model_load_wrapper is not None:
            self.model_load_wrapper = model_load_wrapper

    # Abstract methods - referenced in external files

    @abstractmethod
    def _get_named_parameters(self) -> ParamValidationContainer:
        """Returns an object container that contains many commonly referenced parameters.

        Returns:
            ParamValidationContainer: an object container that contains many commonly referenced parameters.
        """
        ...

    @abstractmethod
    def verify_trubatch_of_databatch(
        self, databatch: base.Types.DataBatch, feature_names: Sequence[str]
    ) -> None:
        """
            Abstract method for validation of ModelRunWrapper.trubatch_of_databatch().
        """
        ...

    @abstractmethod
    def get_cuts_and_expected_shapes(
        self, trubatch: base.Types.TruBatch, outputbatch: base.Types.OutputBatch
    ) -> Tuple[Sequence["Cut"], Sequence[Tuple[Tuple, str]]]:
        """ Abstract method to get the cuts including names and anchors that trulens should test the model architecture against.

        Returns:
            cuts : The list of cuts to check.
            expected_shapes_and_source : A list containing tuples of shapes and a string representing how that shape was gotten.
        """
        ...

    @abstractmethod
    def verify_baseline(
        self, trubatch: base.Types.TruBatch, inputbatch: base.Types.InputBatch
    ) -> None:
        """
            Abstract method for validating baseline construction
        """
        ...

    ### Utility Checks for Data & Batch objects
    def verify_trubatch(
        self,
        trubatch: base.Types.TruBatch,
        truera_keys: Sequence[str],
    ) -> None:
        """A common method among validation types to check trubatch.

        Args:
            trubatch (Base.Types.TruBatch): A TruBatch object of TruEra data.
            truera_keys (Sequence[str]): The expected attributes in trubatch.
        """
        self.verify_type(
            trubatch,
            base.Types.TruBatch,
            origin="ModelRunWrapper.trubatch_of_databatch()"
        )
        tb_dict = asdict(trubatch)
        if not truera_keys.issubset(tb_dict.keys()):
            raise WrapperOutputValidationException(
                f"wrapper method ModelRunWrapper.trubatch_of_databatch keys must contain all of {str(truera_keys)}. Got {str(tb_dict.keys())}"
            )

        batch_size = trubatch.batch_size
        for key in truera_keys:
            if not isinstance(tb_dict[key], np.ndarray):
                raise WrapperOutputValidationException(
                    f"wrapper method ModelRunWrapper.trubatch_of_databatch values should be of type np.ndarray. Instead got {type(tb_dict[key])} for key: '{key}'"
                )
            if not len(tb_dict[key]) == batch_size:
                raise WrapperOutputValidationException(
                    f"wrapper method ModelRunWrapper.trubatch_of_databatch values must match the batch size of \"ids\". "
                    +
                    f"\"ids\" batch size is {batch_size}. \"{key}\" batch size is {len(tb_dict[key])}"
                )

        labels_shape = trubatch.labels.shape

        if not len(labels_shape) == self.param_validation.expected_labels_shape:
            raise WrapperOutputValidationException(
                f"wrapper method trubatch_of_databatch[\"labels\"] must have shape of dimension {self.param_validation.expected_labels_shape} to denote "
                +
                f"{self.param_validation.output_dimension_order_str}. Found {len(labels_shape)} dimensions with shape {str(labels_shape)}"
            )
        if self.model_output_type == "classification":
            assert np.issubdtype(
                trubatch.labels.dtype, np.integer
            ), f"label type was {trubatch.labels.dtype} but {np.integer} expected for classification projects. Labels should be class IDs."
        else:
            assert np.issubdtype(
                trubatch.labels.dtype, np.float_
            ), f"label type was {trubatch.labels.dtype} but {np.float_} expected for {self.model_output_type} projects."

        VerifyHelper.verify_shape(
            trubatch.ids, (batch_size,),
            origin="TruBatch.ids",
            shape_desc="(batch_size,)"
        )

    def verify_inputbatch(
        self,
        inputbatch: base.Types.InputBatch,
        dtype: Type = base.Types.InputBatch
    ):
        self.verify_type(
            inputbatch,
            dtype,
            origin="NLP.TokenizerWrapper.inputbatch_of_textbatch"
        )
        self.verify_type(
            inputbatch.args, List, origin="NLP.Types.InputBatch.args"
        )
        self.verify_type(
            inputbatch.kwargs, Dict, origin="NLP.Types.InputBatch.kwargs"
        )
        # try to run the model
        self.model_run_wrapper.evaluate_model(
            model=self.model, inputs=inputbatch
        )

    ### Top-level Checks (shared by subclasses)

    def verify_evaluate_model(
        self, databatch: base.Types.DataBatch, trubatch: base.Types.TruBatch
    ) -> Tuple[base.Types.OutputBatch, base.Types.InputBatch]:
        """Checks wrapper flow from TruBatch to model output

        Args:
            databatch (Base.Types.DataBatch): Batchable components coming from the SplitLoadWrapper get_ds method.
            trubatch (Base.Types.TruBatch): An object of truera data

        Returns:
            Tuple[Types.OutputBatch, Types.InputBatch]: Returns the output and the input of the model for further verification.

        Raises:
            WrapperOutputValidationException: An exception raised if the method is incorrectly defined.
        """
        inputbatch: base.Types.InputBatch = self.model_run_wrapper.inputbatch_of_databatch(
            databatch, model=self.model
        )

        if not isinstance(inputbatch.args, list):
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.inputbatch_of_databatch first item should return a \"list\". got {str(type(inputbatch.args))}"
            )

        if not isinstance(inputbatch.kwargs, dict):
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.inputbatch_of_databatch second item should return a \"dict\". got {str(type(inputbatch.kwargs))}"
            )
        output = self.model_run_wrapper.evaluate_model(self.model, inputbatch)
        if not output.shape[0] == trubatch.batch_size:
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.evaluate_model batch size should match ModelRunWrapper.trubatch_of_databatch[\"ids\"] batch size. Evaluated batch size is {output.shape[0]}, from shape {str(output.shape)}. \"ids\" batch size is {trubatch.batch_size}"
            )
        print("Passed! ids check input and output batch sizes match")

        if self.param_validation.seq_2_seq:
            if not output.shape[1] == self.attr_config.n_time_step_output:
                raise WrapperOutputValidationException(
                    f"The second dimension in ModelRunWrapper.evaluate_model should be the specified n_time_step_output size. The dimension found is {output.shape[1]} in shape {str(output.shape)}. The n_time_step_output specified in the projects is {self.attr_config.n_time_step_output}."
                )
            print("Passed! check output timestep sizes match")
            class_dimension_idx = 2
        else:
            class_dimension_idx = 1

        if not output.shape[class_dimension_idx
                           ] == self.attr_config.n_output_neurons:
            raise WrapperOutputValidationException(
                f"The dimension index of {class_dimension_idx} in ModelRunWrapper.evaluate_model should be the specified num classes. The dimension found is {output.shape[class_dimension_idx]} in shape {str(output.shape)}. The num classes specified in the projects is {self.attr_config.n_output_neurons}."
            )

        print("Passed! check output num classes match")
        print(
            "Passed! model_run_wrapper.model_input_args_kwargs and model_run_wrapper.evaluate_model"
        )
        return output, inputbatch

    def verify_layers(
        self, *, inputbatch: base.Types.InputBatch,
        trubatch: base.Types.TruBatch, outputbatch: base.Types.OutputBatch,
        logger: logging.Logger
    ) -> None:
        """ Verifies trulens can access the specified layers and they are well formed.

        Args:
            inputbatch (Base.Types.InputBatch): A test batch of inputs that the model can read.
            trubatch (Base.Types.TruBatch): Batched items from wrappers to check against.
            outputbatch (Base.Types.OutputBatch): Batched outputs to check against.

        """
        from trulens.nn.backend import get_backend
        from trulens.nn.models import get_model_wrapper
        from trulens.utils.typing import numpy_of_nested
        tl_model = get_model_wrapper(self.model)

        # TODO: Figure out how we want to standardize model outputs between timeseries and nlp and future.
        if not isinstance(outputbatch, base.Types.OutputBatch):
            outputbatch = base.Types.OutputBatch(
                probits=numpy_of_nested(backend=get_backend(), x=outputbatch)
            )
        cuts, expected_shapes_and_source = self.get_cuts_and_expected_shapes(
            trubatch=trubatch, outputbatch=outputbatch
        )
        for i in range(len(cuts)):
            layer_activations = tl_model.fprop(
                model_args=inputbatch.args,
                model_kwargs=inputbatch.kwargs,
                to_cut=cuts[i]
            )
            if isinstance(layer_activations, tuple):
                logger.warning(
                    f"The `{cuts[i].anchor}` tensor of layer {cuts[i].name} returns a tuple of size {len(layer_activations)}. This can sometimes be intentional, we will check the size of the first element. See logging level INFO for more details."
                )
                logger.info(
                    f"The known times a layer returns a tuple is when pytorch has premade layers like lstm. lstm will return the activations and hidden states as tuple elements."
                )
                layer_activations = layer_activations[0]

            layer_activations = numpy_of_nested(
                backend=get_backend(), x=layer_activations
            )

            # ignore dims of size 1, as they are usually collapsed and we do processing in code for these.
            layer_activations_check_shape = tuple(
                (dim for dim in layer_activations.shape if dim != 1)
            )
            expected_check_shape = tuple(
                (dim for dim in expected_shapes_and_source[i][0] if dim != 1)
            )

            self.verify_shape(
                layer_activations,
                expected_shapes_and_source[i][0],
                origin=expected_shapes_and_source[i][1],
                shape_desc=expected_shapes_and_source[i][1]
            )

            if layer_activations_check_shape != expected_check_shape:
                raise WrapperOutputValidationException(
                    f"The `{cuts[i].anchor}` tensor of layer `{cuts[i].name}` returns a tensor of size {layer_activations.shape}. This should match the {expected_shapes_and_source[i][1]} shape of {expected_shapes_and_source[i][0]}. (Ignoring dimensions of size 1). Check to make sure the right layer and anchor are specified."
                )
            print(
                f"Passed! Checked size of `{cuts[i].anchor}` tensor of layer `{cuts[i].name}`."
            )

    def verify_wrapper_types(
        self,
        *,
        attr_config_type: Any = None,
        model_run_wrapper_type: Any = None,
        split_load_wrapper_type: Any = None,
        model_load_wrapper_type: Any = None
    ) -> None:
        """A common method among validation types to check parameter types.

        Args:
            attr_config_type (Any, optional): _description_. The attr_config (AttributionConfiguration) type based on the input type.
            model_run_wrapper_type (Any, optional): The model_run_wrapper (Parent.ModelRunWrapper) type and parent type based on the input type.
            split_load_wrapper_type (Any, optional): The split_load_wrapper (Parent.SplitLoadWrapper) type and parent type based on the input type.
            model_load_wrapper_type (Any, optional): The model_load_wrapper (Parent.ModelLoadWrapper) type and parent type based on the input type.
        """
        if hasattr(self, "attr_config"):
            VerifyHelper.verify_type(
                self.attr_config,
                attr_config_type,
                origin="AttributionConfiguration"
            )
        else:
            print(
                "Failed to verify attr_config type: Missing attr_config. Add an attr_config with VerifyHelper.add_attr_config()"
            )

        if hasattr(self, "model_run_wrapper"):
            VerifyHelper.verify_type(
                self.model_run_wrapper,
                model_run_wrapper_type,
                origin="ModelRunWrapper"
            )
        else:
            print(
                "Failed to verify model_run_wrapper type: Missing model_run_wrapper. Add a model_run_wrapper with VerifyHelper.add_model_run_wrapper()"
            )

        if self.split_load_wrapper is not None:
            VerifyHelper.verify_type(
                self.split_load_wrapper,
                split_load_wrapper_type,
                origin="SplitLoadWrapper"
            )
        else:
            print(
                "Failed to verify split_load_wrapper type: Missing split_load_wrapper. Add a split_load_wrapper with VerifyHelper.add_split_load_wrapper()"
            )

        if self.model_load_wrapper is not None:
            VerifyHelper.verify_type(
                self.model_load_wrapper,
                model_load_wrapper_type,
                origin="ModelLoadWrapper"
            )
        else:
            print(
                "Failed to verify model_load_wrapper type: Missing model_load_wrapper. Add a model_load_wrapper with VerifyHelper.add_model_load_wrapper()"
            )

    def verify_inputbatch_sizes(
        self,
        inputbatch: base.Types.InputBatch,
        input_dimension_order: Sequence[Dimension] = None,
    ) -> None:
        """A common method among validation types to check input data shapes.

        Args:
            inputbatch (Base.Types.InputBatch): A InputBatch object containing model input arguments.
            input_dimension_order (Sequence[Dimension], optional): The expected input dimension order.

        """
        # TODO: verify shapes?
        args, kwargs = inputbatch.args, inputbatch.kwargs

        if input_dimension_order is not None:
            print(
                "Input dimensions have been customized because input_dimension_order is set."
            )
            n_seq_input_idx = input_dimension_order.index(
                self.param_validation.input_seq_dimension
            )
        else:
            print(
                f"Input dimension defaults are {self.param_validation.input_dimension_order_str}. You can change this with the input_dimension_order in the AttributionConfiguration."
            )
            n_seq_input_idx = 1

        for arg in args + list(kwargs.values()):
            features_shape = arg.shape
            if not features_shape[
                n_seq_input_idx] == self.param_validation.config_input_seq_param:

                raise WrapperOutputValidationException(
                    f"The dimension index {n_seq_input_idx} in ModelRunWrapper.trubatch_of_databatch[\"{self.param_validation.input_data_key}\"] "
                    +
                    f"should be the specified {self.param_validation.input_seq_dimension.name.lower()} dimension size. The dimension found is {features_shape[1]} in shape {str(features_shape)}. "
                    +
                    f"The {self.param_validation.input_seq_dimension.name.lower()} dimension size specified in the projects is {self.param_validation.config_input_seq_param}."
                )

        print(
            f"Passed! input {self.param_validation.input_seq_dimension.name.lower()} dimension size matches model config"
        )

    def verify_attr_config(self):
        if self.attr_config.input_layer is not None:
            VerifyHelper.verify_type(
                self.attr_config.input_layer, (str, Layer),
                origin=f"{self.attr_config_cls_name}.input_layer"
            )
            VerifyHelper.verify_type(
                self.attr_config.input_anchor, (str, LayerAnchor, type(None)),
                origin=f"{self.attr_config_cls_name}.input_anchor"
            )

            if not self.attr_config.input_anchor in [
                "in", "out", LayerAnchor.IN, LayerAnchor.OUT, None
            ]:
                raise ArgValidationException(
                    "input_anchor must be either \"in\" or \"out\". Got %s" %
                    str(self.attr_config.input_anchor)
                )
        elif self.attr_config.input_anchor is not None:
            print(
                "WARNING: input_anchor defined in AttributionConfiguration while input_layer is None. input_anchor will be ignored."
            )

        if self.attr_config.output_layer is not None:
            VerifyHelper.verify_type(
                self.attr_config.output_layer, (str, Layer),
                origin=f"{self.attr_config_cls_name}.output_layer"
            )
            VerifyHelper.verify_type(
                self.attr_config.output_anchor, (str, LayerAnchor, type(None)),
                origin=f"{self.attr_config_cls_name}.output_anchor"
            )
            if not self.attr_config.output_anchor in [
                "in", "out", LayerAnchor.IN, LayerAnchor.OUT, None
            ]:
                raise ArgValidationException(
                    "output_anchor must be either \"in\" or \"out\". Got %s" %
                    str(self.attr_config.output_anchor)
                )
        elif self.attr_config.output_anchor is not None:
            print(
                "WARNING: output_anchor defined in AttributionConfiguration while output_layer is None. output_anchor will be ignored."
            )

    def verify_convert_model_eval_to_binary_classifier(
        self,
        databatch: base.Types.DataBatch,
        model_eval_output: NNB.Outputs,
        logger: Logger,
        labels=False
    ):

        self.verify_type(
            self.model_run_wrapper,
            base.Wrappers.ModelRunWrapper.WithBinaryClassifier,
            origin="ModelRunWrapper"
        )

        binary_output = self.model_run_wrapper.convert_model_eval_to_binary_classifier(
            databatch, model_eval_output, labels=labels
        )

        if hasattr(
            model_eval_output, "probits"
        ):  # temporary for NLP output structures
            model_eval_output = model_eval_output.probits

        logger.info("check binary output shape is batch x 1")
        expected_binary_shape_1 = (model_eval_output.shape[0], 1)
        expected_binary_shape_2 = (model_eval_output.shape[0],)
        if not (
            binary_output.shape == expected_binary_shape_1 or
            binary_output.shape == expected_binary_shape_2
        ):
            raise WrapperOutputValidationException(
                "ModelRunWrapper.convert_model_eval_to_binary_classifier should have batch size matching ModelRunWrapper.evaluate_model, each with one value. expected size %s or %s, but got %s."
                % (
                    expected_binary_shape_1, expected_binary_shape_2,
                    binary_output.shape
                )
            )

        if max(binary_output) > 1 or min(binary_output) < 0:
            raise WrapperOutputValidationException(
                "The values of ModelRunWrapper.convert_model_eval_to_binary_classifier should be between 0 and 1. min found: %d, max found %d. labels param is %s"
                % (min(binary_output), max(binary_output), str(labels))
            )

        print(
            "Passed! model_run_wrapper.convert_model_eval_to_binary_classifier"
        )

    ### Utility methods used in other checks

    @staticmethod
    def verify_shape(
        array: TensorLike,
        expected_shape: Sequence[int],
        *,
        origin: str,
        shape_desc: str,
        additional_logger_info: str = ""
    ) -> None:
        if expected_shape is None:
            # Unknown shape to check
            return

        if not hasattr(array, "shape"):
            raise ArgValidationException(
                f"{origin} should be an array of size {shape_desc} but got type {type(origin)} instead."
            )

        array_shape = tuple((dim for dim in array.shape if dim != 1))
        expected_shape = tuple((dim for dim in expected_shape if dim != 1))

        invalid_shape_exception = WrapperOutputValidationException(
            f"{origin} should be an array of size {shape_desc}. Expecting {expected_shape} but received {array_shape}.{additional_logger_info}"
        )

        if None in expected_shape:
            for a_s, e_s in zip(array_shape, expected_shape):
                if e_s is not None and a_s != e_s:
                    raise invalid_shape_exception
        elif array_shape != expected_shape:
            raise invalid_shape_exception
        print(f"Passed! {origin} size check.")

    @staticmethod
    def verify_type(arg: Any, arg_type: Any, *, origin: str) -> None:
        """Checks if arguments are the right type.

        Args:
            arg (Any): the argument.
            arg_type (Any): the type the argument should be.
            origin (str): The source that the argument comes from. Usually from the configs

        Raises:
            ArgValidationException: If the argument is the wrong type, raise this exception.
        """
        if not isinstance(arg, arg_type):
            raise ArgValidationException(
                f"{origin} must be of type {arg_type}. Instead got {str(type(arg))}:{str(arg)}"
            )

    @staticmethod
    def verify_dimension_ordering(
        config_value: Sequence[Dimension], trubatch: base.Types.TruBatch,
        trubatch_attr: str, expected_dimensions: Sequence[Dimension],
        expected_dimensions_config_values: Sequence[int],
        expected_dimensions_strs: Sequence[str]
    ) -> None:
        """
        validates the dimension orderings
        Parameters
        ===============
        config_value: one of input_dimension_order, output_dimension_order, internal_dimension_order
        trubatch: Object containing TruEra data
        trubatch_attr: the key of the data to check in trubatch
        expected_dimensions: the dimensions expected in the config value
        expected_dimensions_config_values: the config value numbers associated with the expected dimensions. Should be indexed the same as expected_dimensions
        expected_dimensions_strs: the string values associated with the expected dimension. Should be indexed the same as expected_dimensions
        """
        assert len(config_value) == 3
        # Check that the config values contain expected dimensions
        for dimension in expected_dimensions:
            assert dimension in config_value
        expected_shape = []
        expected_shape_str_components = []
        # In the order of the config value dimensions, construct the expected shapes and logging errors if not matching
        for dimension in config_value:
            for i in range(len(expected_dimensions)):
                if dimension == expected_dimensions[i]:
                    expected_shape.append(expected_dimensions_config_values[i])
                    expected_shape_str_components.append(
                        expected_dimensions_strs[i]
                    )
        VerifyHelper.verify_shape(
            getattr(trubatch, trubatch_attr),
            expected_shape=tuple(expected_shape),
            origin=f"TruBatch.{trubatch_attr}",
            shape_desc="%s x %s x %s" % tuple(expected_shape_str_components)
        )
