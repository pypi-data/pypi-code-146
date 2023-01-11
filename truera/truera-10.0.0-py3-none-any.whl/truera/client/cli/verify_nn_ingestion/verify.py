from logging import Logger
from pathlib import Path
import types
from typing import Iterable, Optional

from truera.client.cli.verify_nn_ingestion import ArgValidationException
from truera.client.cli.verify_nn_ingestion import VerifyHelper
from truera.client.cli.verify_nn_ingestion import \
    WrapperOutputValidationException
from truera.client.cli.verify_nn_ingestion.timeseries import \
    TimeseriesVerifyHelper
from truera.client.nn import NNBackend as NNB
from truera.client.nn import wrappers as base
from truera.client.nn.client_configs import AttributionConfiguration
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.wrappers import nlp
from truera.client.nn.wrappers.datasets import convert_to_truera_iterable
from truera.client.nn.wrappers.timeseries import Wrappers as Timeseries


def get_helper(
    *,
    model_input_type: str,
    model_output_type: str,
    attr_config: AttributionConfiguration,
    model: NNB.Model,
    split_load_wrapper: base.Wrappers.SplitLoadWrapper,
    model_run_wrapper: base.Wrappers.ModelRunWrapper,
    model_load_wrapper: Optional[base.Wrappers.ModelLoadWrapper] = None,
    tokenizer_wrapper: Optional[nlp.Wrappers.TokenizerWrapper] = None
) -> VerifyHelper:
    """Returns an appropriate VerifyHelper implementation to help validate different modelling types.

    Args:
        model_input_type (str): datatype of model input. Currently allows 'time_series_tabular' and 'text'.
        model_input_type (str): datatype of model output. Currently allows 'classification' and 'regression'.
        attr_config (AttributionConfiguration): The run configuration. At this point it will be based on the input type.
        model (NNB.Model): The model object.
        split_load_wrapper (base.Wrappers.SplitLoadWrapper): The SplitLoadWrapper where the parent Base class should match the project_input_type.
        model_run_wrapper (base.Wrappers.ModelRunWrapper): The ModelRunWrapper where the parent Base class should match the project_input_type.
        model_load_wrapper (Optional[base.Wrappers.ModelLoadWrapper], optional): The SplitLoadWrapper where the parent Base class should match the project_input_type.
        tokenizer_wrapper (Optional[nlp.Wrappers.TokenizerWrapper], optional): The TokenizerWrapper implementation. Only needed when input_type is 'text'.

    Returns:
        VerifyHelper: Subclass of VerifyHelper for particular domain
    """
    if isinstance(attr_config, NLPAttributionConfiguration):
        from truera.client.cli.verify_nn_ingestion.nlp import NLPVerifyHelper
        return NLPVerifyHelper(
            model_input_type=model_input_type,
            model_output_type=model_output_type,
            attr_config=attr_config,
            model=model,
            split_load_wrapper=split_load_wrapper,
            model_run_wrapper=model_run_wrapper,
            model_load_wrapper=model_load_wrapper,
            tokenizer_wrapper=tokenizer_wrapper
        )
    elif isinstance(attr_config, RNNAttributionConfiguration):
        return TimeseriesVerifyHelper(
            model_input_type=model_input_type,
            model_output_type=model_output_type,
            attr_config=attr_config,
            model=model,
            split_load_wrapper=split_load_wrapper,
            model_run_wrapper=model_run_wrapper,
            model_load_wrapper=model_load_wrapper
        )
    else:
        raise ArgValidationException(
            f"attr_config must be one of RNNAttributionConfiguration, NLPAttributionConfiguration. Instead got {type(attr_config)}"
        )


def verify_split(
    verify_helper: VerifyHelper, logger: Optional[Logger] = None
) -> None:
    """Verifies all the SplitLoadWrapper methods are well formed.

    Args:
        verify_helper (VerifyHelper): The VerifyHelper container with wrapper and model objects
        logger (Logger, optional): The Logger.
    """
    split_load_wrapper = verify_helper.split_load_wrapper
    split_path = split_load_wrapper.get_data_path()
    if isinstance(split_load_wrapper.get_ds, types.FunctionType):
        # This is for legacy support on ingestion_wrappers.py
        dataset = convert_to_truera_iterable(
            split_load_wrapper.get_ds(split_path)
        )
    elif isinstance(split_load_wrapper, base.Wrappers.SplitLoadWrapper):
        dataset = convert_to_truera_iterable(split_load_wrapper.get_ds())
    else:
        raise ArgValidationException(
            f"Argument split_load_wrapper is not instance of {str(base.Wrappers.SplitLoadWrapper)}."
        )

    if not isinstance(dataset, Iterable):
        raise WrapperOutputValidationException(
            "SplitLoadWrapper.get_ds did not return an iterable object."
        )
    print("Passed! SplitLoadWrapper.get_ds")

    dataset_single_batch = None
    dataset_single_batch = next(iter(dataset))
    feature_names = None

    if isinstance(split_load_wrapper, Timeseries.SplitLoadWrapper):
        feature_names = TimeseriesVerifyHelper.verify_get_feature_names(
            split_load_wrapper, split_path
        )
        TimeseriesVerifyHelper.verify_get_short_feature_descriptions(
            feature_names, split_load_wrapper, split_path
        )
        TimeseriesVerifyHelper.verify_get_missing_values(
            feature_names, split_load_wrapper, split_path
        )
    if isinstance(
        split_load_wrapper, base.Wrappers.SplitLoadWrapper.WithStandardization
    ):
        dataset_single_batch = split_load_wrapper.standardize_databatch(
            dataset_single_batch
        )
    return dataset_single_batch, feature_names


def verify_data_consistency(
    verify_helper: VerifyHelper, logger: Optional[Logger] = None
) -> None:
    """Verifies that the data from TruBatch is consistent with all data inputs.

    Args:
        verify_helper (VerifyHelper): The VerifyHelper container with wrapper and model objects
        logger (Logger): The Logger.

    Raises:
        WrapperOutputValidationException: _description_

    Returns:
        _type_: _description_
    """

    databatch, feature_names = verify_split(verify_helper)
    print("Checking data consistency...")
    databatch_dup, _ = verify_split(verify_helper)

    trubatch: base.Types.TruBatch = verify_helper.verify_trubatch_of_databatch(
        databatch=databatch, feature_names=feature_names
    )

    trubatch_dup: base.Types.TruBatch = verify_helper.verify_trubatch_of_databatch(
        databatch=databatch_dup, feature_names=feature_names
    )

    if False in (trubatch.ids == trubatch_dup.ids):
        raise WrapperOutputValidationException(
            "Dataset loads a different set of records on each load."
        )

    print("Passed! Dataset returns same ordering on each run")
    return databatch, trubatch


def verify_model(
    verify_helper: VerifyHelper, model_path: Optional[Path] = None
):
    verify_helper.verify_attr_config()
    if isinstance(
        verify_helper.model_load_wrapper.get_model, types.FunctionType
    ):
        model = verify_helper.model_load_wrapper.get_model(model_path)
    else:
        model = verify_helper.model_load_wrapper.get_model()
    return model, verify_helper.model_load_wrapper


def verify_model_eval(
    verify_helper: VerifyHelper, dataset_single_batch: base.Types.DataBatch,
    trubatch: base.Types.TruBatch, *, logger: Logger
) -> None:
    """Verifies the ModelRunWrapper evaluate_model method is well formed.

    Args:
        verify_helper (VerifyHelper): The VerifyHelper container with wrapper and model objects
        dataset_single_batch (Base.Types.DataBatch): A batchable input coming from SplitLoadWrapper get_ds method.
        trubatch (Base.Types.TruBatch): An object of truera data
        logger (Logger): The Logger.

    """
    model_eval_output, inputbatch = verify_helper.verify_evaluate_model(
        databatch=dataset_single_batch, trubatch=trubatch
    )
    try:
        if not isinstance(
            verify_helper.model_run_wrapper,
            Timeseries.ModelRunWrapper.WithBinaryClassifier
        ):
            raise NotImplementedError

        verify_helper.verify_convert_model_eval_to_binary_classifier(
            dataset_single_batch, model_eval_output, logger, labels=False
        )
        verify_helper.verify_convert_model_eval_to_binary_classifier(
            dataset_single_batch, trubatch.labels, logger, labels=True
        )
    except NotImplementedError:
        logger.warning(
            "ModelRunWrapper does not implement WithBinaryClassifier. Confusion Matrix sampling feature will not be available."
        )

    return model_eval_output, inputbatch


def verify_run(verify_helper: VerifyHelper, logger: Optional[Logger] = None):
    """Verifies that all components needed for running attributions is well defined.

    Args:
        verify_helper (VerifyHelper): The VerifyHelper container with wrapper and model objects
        logger (Logger): The Logger.
    """

    # Check Data loading
    dataset_single_batch, trubatch = verify_data_consistency(
        verify_helper, logger=logger
    )

    # Check model running flow
    outputbatch, inputbatch = verify_model_eval(
        verify_helper,
        dataset_single_batch=dataset_single_batch,
        trubatch=trubatch,
        logger=logger
    )

    verify_helper.verify_baseline(trubatch=trubatch, inputbatch=inputbatch)

    # Check trulens layer access and shapes
    verify_helper.verify_layers(
        inputbatch=inputbatch,
        trubatch=trubatch,
        outputbatch=outputbatch,
        logger=logger
    )
