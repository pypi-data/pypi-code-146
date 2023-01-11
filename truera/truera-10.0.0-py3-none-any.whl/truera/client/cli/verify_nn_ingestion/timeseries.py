from logging import Logger
from pathlib import Path
import types
from typing import Sequence, Tuple

import numpy as np

from truera.client.cli.verify_nn_ingestion import ArgValidationException
from truera.client.cli.verify_nn_ingestion import ParamValidationContainer
from truera.client.cli.verify_nn_ingestion import VerifyHelper
from truera.client.cli.verify_nn_ingestion import \
    WrapperOutputValidationException
from truera.client.nn.client_configs import Dimension
from truera.client.nn.client_configs import Layer
from truera.client.nn.client_configs import LayerAnchor
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.wrappers.datasets import convert_to_truera_iterable
from truera.client.nn.wrappers.timeseries import Types
from truera.client.nn.wrappers.timeseries import Wrappers
from truera.rnn.general.model_runner_proxy.baseline_utils import \
    BaselineConstructor
from truera.rnn.general.model_runner_proxy.sampling_utils import \
    prepare_datasplit


class TimeseriesVerifyHelper(VerifyHelper):

    def get_cuts_and_expected_shapes(
        self, trubatch: Types.TruBatch, outputbatch: Types.OutputBatch
    ) -> Tuple[Sequence["Cut"], Sequence[Tuple[Tuple, str]]]:
        """ Gets the trulens cuts to check.

        Returns:
            cuts : The list of cuts to check.
            expected_shapes_and_source : A list containing tuples of shapes and a string representing how that shape was gotten.
        """
        from trulens.nn.slices import Cut
        from trulens.nn.slices import InputCut
        from trulens.nn.slices import OutputCut
        attr_config = self.attr_config
        expected_shapes_and_source = []

        if attr_config.input_layer == Layer.INPUT:
            cuts = [InputCut()]
        else:
            cuts = [
                Cut(
                    attr_config.input_layer,
                    anchor=str(attr_config.input_anchor)
                )
            ]
        expected_shapes_and_source.append(
            (trubatch.features.shape, "trubatch `features`")
        )

        if attr_config.output_layer == Layer.OUTPUT:
            cuts.append(OutputCut())
        else:
            cuts.append(
                Cut(
                    attr_config.output_layer,
                    anchor=str(attr_config.output_anchor)
                )
            )
        expected_shapes_and_source.append(
            (outputbatch.probits.shape, "model output")
        )

        return cuts, expected_shapes_and_source

    def verify_wrapper_types(self) -> None:
        """The Timeseries Specific validation for verify_wrapper_types. See the VerifyHelper for more details.
        """
        super().verify_wrapper_types(
            attr_config_type=RNNAttributionConfiguration,
            model_run_wrapper_type=Wrappers.ModelRunWrapper,
            split_load_wrapper_type=Wrappers.SplitLoadWrapper,
            model_load_wrapper_type=Wrappers.ModelLoadWrapper
        )

    def verify_attr_config(self):
        """The Timeseries Specific validation for verify_attr_config. See the VerifyHelper for more details.
        """
        super().verify_attr_config()
        if self.attr_config.internal_layer is not None:
            VerifyHelper.verify_type(
                self.attr_config.internal_layer,
                str,
                origin="RNNAttributionConfiguration.internal_layer"
            )
            VerifyHelper.verify_type(
                self.attr_config.internal_anchor, (str, LayerAnchor),
                origin="RNNAttributionConfiguration.internal_anchor"
            )
            if not self.attr_config.internal_anchor in [
                "in", "out", LayerAnchor.IN, LayerAnchor.OUT
            ]:
                raise ArgValidationException(
                    "internal_anchor must be either \"in\" or \"out\". Got %s" %
                    str(self.attr_config.internal_anchor)
                )

            VerifyHelper.verify_type(
                self.attr_config.n_internal_neurons,
                int,
                origin="RNNAttributionConfiguration.n_internal_neurons"
            )
            if not self.attr_config.n_internal_neurons > 2:
                raise ArgValidationException(
                    "n_internal_neurons must be greater than 2. Got %s" %
                    str(self.attr_config.n_internal_neurons)
                )

        VerifyHelper.verify_type(
            self.attr_config.n_time_step_input,
            int,
            origin="RNNAttributionConfiguration.n_time_step_input"
        )
        VerifyHelper.verify_type(
            self.attr_config.n_time_step_output,
            int,
            origin="RNNAttributionConfiguration.n_time_step_output"
        )
        VerifyHelper.verify_type(
            self.attr_config.n_features_input,
            int,
            origin="RNNAttributionConfiguration.n_features_input"
        )

    def verify_lengths_trubatch(
        self, n_time_step_input: int, trubatch: Types.TruBatch, batch_size: int,
        logger: Logger
    ):
        """Validate the 'lengths' data.

        Args:
            n_time_step_input (int): The number of input timesteps
            trubatch (Types.TruBatch): Object of truera properties.
            batch_size (int): the number of items in a batch.
            logger (Logger): The logger object
        """
        VerifyHelper.verify_shape(
            trubatch.lengths, (batch_size,),
            origin="TruBatch.lengths",
            shape_desc="(batch_size,)"
        )

        lengths_data = trubatch.lengths
        min_val = np.min(lengths_data)
        max_val = np.max(lengths_data)
        if min_val < 1:
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.trubatch_of_databatch[\"lengths\"] has minimum value of {min_val}. Length values must be between 1 and AttributionConfiguration.n_time_step_input:{n_time_step_input}"
            )
        if max_val > n_time_step_input:
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.trubatch_of_databatch[\"lengths\"] has maximum value of {max_val}. Length values must be between 1 and AttributionConfiguration.n_time_step_input:{n_time_step_input}"
            )
        if min_val == max_val and max_val != n_time_step_input:
            logger.warning(
                f"ModelRunWrapper.trubatch_of_databatch[\"lengths\"] are all the same length of {max_val}, even though the AttributionConfiguration.n_time_step_input is {n_time_step_input}. You may want to double check that this is intentional."
            )

    def verify_trubatch_of_databatch(
        self,
        databatch: Types.DataBatch,
        feature_names: Sequence[str],
        logger: Logger = None
    ) -> None:
        """The Timeseries Specific validation for verify_trubatch_of_databatch. See the VerifyHelper for more details.
        """
        trubatch: Types.TruBatch = self.model_run_wrapper.trubatch_of_databatch(
            databatch, model=self.model
        )
        truera_keys = set(["ids", "features", "lengths", "labels"])
        self.verify_trubatch(trubatch=trubatch, truera_keys=truera_keys)
        batch_size = trubatch.batch_size

        self.verify_lengths_trubatch(
            self.attr_config.n_time_step_input, trubatch, batch_size, logger
        )

        if isinstance(
            self.model_run_wrapper, Wrappers.ModelRunWrapper.WithOneHot
        ):
            if not self.attr_config.input_dimension_order:
                self.verify_feature_names_match_sizes(
                    trubatch, feature_names, self.model_run_wrapper, logger
                )
            else:
                self.verify_feature_names_match_sizes(
                    trubatch,
                    feature_names,
                    self.model_run_wrapper,
                    logger,
                    feature_dimension=self.attr_config.input_dimension_order.
                    index(Dimension.FEATURE)
                )
        if not self.attr_config.input_dimension_order:
            VerifyHelper.verify_shape(
                getattr(trubatch, self.param_validation.input_data_key), (
                    batch_size, self.param_validation.config_input_seq_param,
                    self.param_validation.config_input_data_param
                ),
                origin=f"TruBatch.{self.param_validation.input_data_key}",
                shape_desc=self.param_validation.input_dimension_order_str,
                additional_logger_info=
                " Or you may need to supply 'input_dimension_order' in your AttributionConfig."
            )
        else:
            VerifyHelper.verify_dimension_ordering(
                config_value=self.attr_config.input_dimension_order,
                trubatch=trubatch,
                trubatch_attr=self.param_validation.input_data_key,
                expected_dimensions=[
                    Dimension.BATCH, self.param_validation.input_seq_dimension,
                    self.param_validation.input_data_dimension
                ],
                expected_dimensions_config_values=[
                    batch_size, self.param_validation.config_input_seq_param,
                    self.param_validation.config_input_data_param
                ],
                expected_dimensions_strs=[
                    "batch", self.param_validation.config_input_seq_param_str,
                    self.param_validation.config_input_data_param_str
                ],
            )

        # Todo: generalize this if we ever get to nlp seq2seq
        if not self.attr_config.output_dimension_order:
            VerifyHelper.verify_shape(
                trubatch.labels, (
                    batch_size, self.attr_config.n_time_step_output,
                    self.attr_config.n_output_neurons
                ),
                origin="TruBatch.labels",
                shape_desc="batch x n_time_step_output x n_output_neurons",
                additional_logger_info=
                " Or you may need to supply 'output_dimension_order' in your RNNAttributionConfig."
            )
        else:
            VerifyHelper.verify_dimension_ordering(
                config_value=self.attr_config.output_dimension_order,
                trubatch=trubatch,
                trubatch_attr="labels",
                expected_dimensions=[
                    Dimension.BATCH, Dimension.TIMESTEP, Dimension.CLASS
                ],
                expected_dimensions_config_values=[
                    batch_size, self.attr_config.n_time_step_output,
                    self.attr_config.n_output_neurons
                ],
                expected_dimensions_strs=[
                    "batch", "n_time_step_output", "n_output_neurons"
                ],
            )

        if self.attr_config.input_dimension_order is not None:
            n_data_input_idx = self.attr_config.input_dimension_order.index(
                self.param_validation.input_data_dimension
            )
        else:
            n_data_input_idx = 2

        pp_features = trubatch.preprocessed_features
        features_shape = getattr(
            trubatch, self.param_validation.input_data_key
        ).shape
        if pp_features is not None:
            pp_features_shape = pp_features.shape
            if not pp_features_shape[
                n_data_input_idx
            ] == self.param_validation.config_input_data_param:
                raise WrapperOutputValidationException(
                    f"The dimension index {n_data_input_idx} in ModelRunWrapper.trubatch_of_databatch[\"preprocessed_features\"] should be the specified feature size. The dimension found is {pp_features_shape[n_data_input_idx]} in shape {str(pp_features_shape)}. The feature size specified in the projects is {self.param_validation.config_input_data_param}."
                )

        else:
            if not features_shape[
                n_data_input_idx
            ] == self.param_validation.config_input_data_param:
                raise WrapperOutputValidationException(
                    f"The dimension index {n_data_input_idx} in ModelRunWrapper.trubatch_of_databatch[\"{self.param_validation.input_data_key}\"] should be the specified feature size. The dimension found is {features_shape[n_data_input_idx]} in shape {str(features_shape)}. The feature size specified in the projects is {self.param_validation.config_input_data_param}."
                )

        print("Passed! input features match model config")

        print("Passed! ModelRunWrapper.verify_trubatch_of_databatch")
        return trubatch

    @staticmethod
    def verify_get_missing_values(
        feature_names: Sequence[str],
        split_load_wrapper: Wrappers.SplitLoadWrapper, split_path: Path
    ):
        if isinstance(
            split_load_wrapper.get_missing_values, types.FunctionType
        ):
            missing_vals = split_load_wrapper.get_missing_values(split_path)
        else:
            missing_vals = split_load_wrapper.get_missing_values()
        if not (
            missing_vals is None or isinstance(missing_vals, dict) or
            isinstance(missing_vals, list)
        ):
            raise WrapperOutputValidationException(
                "SplitLoadWrapper.missing_vals needs to return dict, list, or None"
            )
        if missing_vals is None:
            print("Passed! SplitLoadWrapper.missing_vals is not implemented")
        else:
            if not len(missing_vals) > 0:
                raise WrapperOutputValidationException(
                    "SplitLoadWrapper.missing_vals cannot be empty. If there are no missing values, return None."
                )

        def _verify_missing_vals_subset(names):
            if not set(names).issubset(set(feature_names)):
                raise WrapperOutputValidationException(
                    "SplitLoadWrapper.missing_vals must be a subset of the features: %s"
                    % str(feature_names)
                )

        if isinstance(missing_vals, dict):
            _verify_missing_vals_subset(missing_vals.keys())
            print(
                "Passed! SplitLoadWrapper.missing_vals is a dictionary of values"
            )
        elif isinstance(missing_vals, list):
            _verify_missing_vals_subset(missing_vals)
            print("Passed! SplitLoadWrapper.missing_vals is a list of values")

    @staticmethod
    def verify_get_short_feature_descriptions(
        feature_names: Sequence[str],
        split_load_wrapper: Wrappers.SplitLoadWrapper, split_path: Path
    ):
        if isinstance(
            split_load_wrapper.get_short_feature_descriptions,
            types.FunctionType
        ):
            short_feature_descriptions = split_load_wrapper.get_short_feature_descriptions(
                split_path
            )
        else:
            short_feature_descriptions = split_load_wrapper.get_short_feature_descriptions(
            )
        if not isinstance(short_feature_descriptions, dict):
            raise WrapperOutputValidationException(
                "SplitLoadWrapper.get_short_feature_descriptions should be of type \"dict\". Got %s"
                % str(type(short_feature_descriptions))
            )

        if not set(feature_names) == short_feature_descriptions.keys():
            raise WrapperOutputValidationException(
                "SplitLoadWrapper.get_short_feature_descriptions keys must match SplitLoadWrapper.get_features. features:%s\n\ndescription keys:%s"
                % (str(feature_names), str(short_feature_descriptions.keys()))
            )

        for feature in feature_names:
            if not isinstance(feature, str):
                raise WrapperOutputValidationException(
                    "SplitLoadWrapper.get_features contents should be of type \"str\". Got %s:%s"
                    % (str(type(feature)), str(feature))
                )

        print("Passed! SplitLoadWrapper.get_short_feature_descriptions")

    @staticmethod
    def verify_get_feature_names(
        split_load_wrapper: Wrappers.SplitLoadWrapper, split_path: Path
    ) -> Sequence[str]:
        if isinstance(split_load_wrapper.get_feature_names, types.FunctionType):
            feature_names = split_load_wrapper.get_feature_names(split_path)
        else:
            feature_names = split_load_wrapper.get_feature_names()
        if not isinstance(feature_names, list):
            raise WrapperOutputValidationException(
                "SplitLoadWrapper.get_feature_names must be a list. instead got %s"
                % str(type(feature_names))
            )

        for feature in feature_names:
            if not isinstance(feature, str):
                raise WrapperOutputValidationException(
                    "SplitLoadWrapper.get_feature_names must be a list of \"str\". instead got %s:%s"
                    % (str(type(feature)), feature)
                )

        print("Passed! SplitLoadWrapper.get_feature_names")
        return feature_names

    @staticmethod
    def verify_feature_names_match_sizes(
        trubatch: Types.TruBatch,
        feature_names: Sequence[str],
        model_run_wrapper: Wrappers.ModelRunWrapper,
        logger: Logger,
        feature_dimension: int = 2
    ) -> None:
        features_shape = trubatch.features.shape
        num_features = features_shape[feature_dimension]
        one_hot_sizes = model_run_wrapper.get_one_hot_sizes()
        if trubatch.preprocessed_features is not None:
            logger.info("starting preprocessed feature validation")
            remaining_features_with_one_hot = num_features
            pp_f_shape = trubatch.preprocessed_features.shape
            if not len(feature_names) == pp_f_shape[feature_dimension]:
                raise WrapperOutputValidationException(
                    f"Number of features in SplitLoadWrapper.get_features should match the third dimension in ModelRunWrapper.trubatch_of_databatch[\"preprocessed_features\"]. Number of features in get_features is {len(feature_names)}, and third dimension of trubatch_of_databatch[\"preprocessed_features\"] is {pp_f_shape[feature_dimension]}, with total shape {str(pp_f_shape)}."
                )

            remaining_features = len(feature_names)
            for oh_feature in one_hot_sizes:
                if (oh_feature in feature_names):
                    remaining_features_with_one_hot -= one_hot_sizes[oh_feature]
                    remaining_features -= 1
            remaining_features_without_one_hot = remaining_features_with_one_hot
            if not remaining_features == remaining_features_without_one_hot:
                raise WrapperOutputValidationException(
                    f"ModelRunWrapper.trubatch_of_databatch[\"features\"]\"s third dimension should add to all onehot sizes plus non onehot features. The shape of trubatch_of_databatch[\"features\"] is {features_shape}, third dimension is {num_features}, and total features calculated is { num_features - remaining_features_with_one_hot + remaining_features}. debug info -- features:{str(feature_names)}\n\nModelRunWrapper.get_one_hot_sizes:{str(one_hot_sizes)}"
                )
            print("Passed! SplitLoadWrapper.get_one_hot_sizes")
        else:
            if not len(feature_names) == num_features:
                raise WrapperOutputValidationException(
                    f"Number of features in SplitLoadWrapper.get_features should match the third dimension in ModelRunWrapper.trubatch_of_databatch[\"features\"]. Number of features in get_features is {len(feature_names)}, and third dimension of trubatch_of_databatch[\"features\"] is {num_features}, with total shape {features_shape}."
                )

            if not len(one_hot_sizes) == 0:
                raise WrapperOutputValidationException(
                    f"ModelRunWrapper.get_one_hot_sizes cannot be 0. If there are no one hot encodings, return None. got {str(one_hot_sizes)}"
                )

        print("Passed! feature name and size validation.")
        return feature_names

    def verify_baseline(
        self, trubatch: Types.TruBatch, inputbatch: Types.InputBatch
    ) -> None:
        """
            Method for validating baseline construction
        """
        from trulens.nn.models import get_backend

        baseline_ds, batch_size, is_unknown_ds_type = prepare_datasplit(
            convert_to_truera_iterable(self.split_load_wrapper.get_ds()),
            backend=get_backend(),
            batch_size=2,
            model=self.model,
            model_wrapper=self.model_run_wrapper,
            num_take_records=2,
            shuffle=False
        )

        baseline_constructor = BaselineConstructor(
            baseline_ds, self.split_load_wrapper.get_data_path(), self.model,
            self.split_load_wrapper, self.model_run_wrapper, self.attr_config,
            batch_size
        )  # this fn needs model_name and n_time_step from attr_config
        batched_baseline = baseline_constructor.construct_avg_baseline()
        self.verify_shape(
            batched_baseline, (
                None, self.attr_config.n_time_step_input,
                self.attr_config.n_features_input
            ),
            origin="Baseline",
            shape_desc=
            "Batch size x attr_config.n_time_step_input x attr_config.n_features_input"
        )
        print("Passed! Baseline checks")

    def _get_named_parameters(self) -> ParamValidationContainer:
        """Returns an object container that contains many commonly referenced parameters.

        Returns:
            ParamValidationContainer: an object container that contains many commonly referenced parameters.
        """
        if not hasattr(self, "attr_config") or self.attr_config is None:
            return None
        return ParamValidationContainer(
            input_seq_dimension=Dimension.TIMESTEP,
            input_data_dimension=Dimension.FEATURE,
            config_input_seq_param=self.attr_config.n_time_step_input,
            config_input_data_param=self.attr_config.n_features_input,
            config_input_seq_param_str="n_time_step_input",
            config_input_data_param_str="n_features_input",
            input_dimension_order_str=
            "(batch x n_time_step_input x n_features_input)",
            output_dimension_order_str=
            "(batchsize x num_timesteps x num_classes)",
            expected_labels_shape=3,
            input_data_key="features",
            seq_2_seq=True
        )
