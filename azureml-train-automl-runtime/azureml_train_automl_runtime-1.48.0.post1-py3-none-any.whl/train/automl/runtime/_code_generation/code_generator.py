# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Functions used to generate Python script for customer usage."""
import inspect
import json
import logging
import os
import pickle
import re
import shutil
import tempfile
import mlflow
try:
    import torch
except ImportError:
    # We shouldn't hit this unless the model being inspected isn't DNN, in which case it doesn't matter.
    pass

from typing import Any, Dict, List, Optional, cast, Union

from sklearn.pipeline import Pipeline

from azureml.core import Dataset, Run, Workspace

from azureml.automl.core import _codegen_utilities
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.constants import Sample_Weights_Unsupported
from azureml.automl.runtime import data_cleaning
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.shared.model_wrappers import (
    ForecastingPipelineWrapper,
    PipelineWithYTransformations,
    PreFittedSoftVotingClassifier,
    PreFittedSoftVotingRegressor,
    StackEnsembleBase,
)
from azureml.automl.runtime.shared._cache_constants import Keys
from azureml.data.abstract_dataset import AbstractDataset
from azureml.train.automl import _constants_azureml
from azureml.train.automl.runtime import VERSION
from azureml.training.tabular._constants import TimeSeriesInternal

from . import utilities
from .constants import FunctionNames
from .ensemble_model_template import EnsembleModelTemplate, StackEnsembleModelTemplate
from .featurizer_template import AbstractFeaturizerTemplate
from .function import Function
from .forecast_dnn_model_template import SingleForecastDnnModelTemplate
from .model_template import AbstractModelTemplate, SingleSklearnModelTemplate
from .pipeline_step_template import PipelineStepTemplate
from .template_factory import featurizer_template_factory, preprocessor_template_factory, validation_template_factory
from .validation.validation_task import AbstractTask
from azureml.automl.runtime.featurization import DataTransformer, TimeSeriesTransformer
from azureml.automl.core.inference import inference
from azureml.automl.core.shared.constants import Transformers, OUTPUT_PATH, MODEL_PATH, PT_MODEL_PATH
from .data_featurizer_template import DataFeaturizerTemplate
from .validation.validation_strategy import AbstractValidationStrategy, ForecastingDNNValidationDataStrategy
from .patcher_plugins import patcher
try:
    import azureml.contrib.automl.dnn.forecasting
except:
    pass
logger = logging.getLogger(__name__)


def _get_setup_run(parent_run: Run) -> Run:
    setup_run_list = list(parent_run._client.run.get_runs_by_run_ids(run_ids=[f"{parent_run.id}_setup"]))
    # if this is a local run there will be no setup iteration
    if len(setup_run_list) == 0:
        setup_run = parent_run
    else:
        setup_run = setup_run_list[0]
    return setup_run


def split_dataset(X, y, weights, split_ratio, should_stratify):
    '''
    Splits the dataset into a training and testing set.

    Splits the dataset using the given split ratio. The default ratio given is 0.25 but can be
    changed in the main function. If should_stratify is true the data will be split in a stratified
    way, meaning that each new set will have the same distribution of the target value as the
    original dataset. should_stratify is true for a classification run, false otherwise.
    '''
    from sklearn.model_selection import train_test_split

    random_state = 42
    if should_stratify:
        stratify = y
    else:
        stratify = None

    if weights is not None:
        X_train, X_test, y_train, y_test, weights_train, weights_test = train_test_split(
            X, y, weights, stratify=stratify, test_size=split_ratio, random_state=random_state
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, stratify=stratify, test_size=split_ratio, random_state=random_state
        )
        weights_train, weights_test = None, None

    return (X_train, y_train, weights_train), (X_test, y_test, weights_test)


def setup_instrumentation(automl_run_id):
    import logging
    import sys

    from azureml.core import Run
    from azureml.telemetry import INSTRUMENTATION_KEY, get_telemetry_log_handler
    from azureml.telemetry._telemetry_formatter import ExceptionFormatter

    logger = logging.getLogger("azureml.training.tabular")

    try:
        logger.setLevel(logging.INFO)

        # Add logging to STDOUT
        stdout_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stdout_handler)

        # Add telemetry logging with formatter to strip identifying info
        telemetry_handler = get_telemetry_log_handler(
            instrumentation_key=INSTRUMENTATION_KEY, component_name="azureml.training.tabular"
        )
        telemetry_handler.setFormatter(ExceptionFormatter())
        logger.addHandler(telemetry_handler)

        # Attach run IDs to logging info for correlation if running inside AzureML
        try:
            run = Run.get_context()
            return logging.LoggerAdapter(logger, extra={
                "properties": {
                    "codegen_run_id": run.id,
                    "automl_run_id": automl_run_id
                }
            })
        except Exception:
            pass
    except Exception:
        pass

    return logger


def generate_autofeaturization_script(parent_run: Run, pipeline: Optional[Any] = None) -> str:
    """
    In autofeaturization, the parent run is passed in to generate the script for featurization
    """
    return generate_full_script(parent_run, pipeline, is_autofeaturization=True)


def generate_verticals_script() -> str:
    stack_list = inspect.stack()
    for fileinfo in stack_list:
        if fileinfo[1].startswith("hd") and fileinfo[1].endswith("driver.py"):
            filename = fileinfo[1]
            break
    filepath = os.path.abspath(filename)
    with open(filepath, "r") as f:
        code = f.read()

    # the script from JOS snapshot has some weird unicode characters that causes parsing to fail. Encode and
    # decode will remove those characters. Also set enable_code_generation=False to prevent re-running codegen
    code = code.encode("ascii", "ignore").decode().replace(
        "'enable_code_generation':True", "'enable_code_generation':False")
    return code


def generate_full_script(child_run: Run, pipeline: Optional[Any] = None,
                         is_autofeaturization: bool = False) -> str:
    with patcher.patch_with_settings(single_line_output=False, rewrite_namespaces=True):
        # with _codegen_utilities.use_custom_repr(output_single_line=False):
        major_minor_version = re.search(r"^(\d+\.\d+\.\d+)", VERSION)
        if major_minor_version is not None:
            sdk_version = major_minor_version.group(0)
        else:
            sdk_version = VERSION
        output = [
            f"# This file has been autogenerated by version {sdk_version} "
            f"of the Azure Automated Machine Learning SDK.",
            "\n",
            "import numpy",
            "import numpy as np",
            "import pandas as pd",
            "import pickle",
            "import argparse",
            "\n",
            "# For information on AzureML packages: \
https://docs.microsoft.com/en-us/python/api/?view=azure-ml-py",
            "from azureml.training.tabular._diagnostics import logging_utilities",
            "\n",
        ]
        # Add instrumentation code
        output.extend(_codegen_utilities.get_function_source(setup_instrumentation))
        output.append("")
        output.append(f"automl_run_id = '{child_run.id}'")
        output.append(f"logger = setup_instrumentation(automl_run_id)")
        output.append("\n")

        # Add function for splitting dataset
        output.extend(_codegen_utilities.get_function_source(split_dataset))
        output.append("")

        is_forecasttcn = False
        if (is_autofeaturization):
            parent_run = child_run
        elif child_run.properties.get("run_algorithm") == 'TCNForecaster':
            is_forecasttcn = True
            parent_run = child_run.parent.parent
        else:
            parent_run = child_run.parent

        properties = parent_run.properties

        dataset_dict = utilities.get_input_datasets(parent_run)

        settings_json = properties.get(_constants_azureml.Properties.AML_SETTINGS)
        settings_obj = json.loads(settings_json)

        task_type = cast(str, settings_obj.get("task_type"))
        label_column_name = cast(str, settings_obj.get("label_column_name"))
        weight_column_name = cast(Optional[str], settings_obj.get("weight_column_name"))
        metric_name = cast(str, settings_obj.get("primary_metric"))
        test_size = cast(Optional[float], settings_obj.get("test_size"))
        validation_size = cast(Optional[float], settings_obj.get("validation_size"))
        n_cross_validations = cast(Optional[int], settings_obj.get("n_cross_validations"))
        n_step = cast(Optional[int], settings_obj.get("cv_step_size"))
        y_min = cast(Optional[float], settings_obj.get("y_min"))
        y_max = cast(Optional[float], settings_obj.get("y_max"))
        is_timeseries = cast(bool, settings_obj.get("is_timeseries", False))

        validation_dataset_exists = dataset_dict.get('validation_dataset_id') is not None or \
            dataset_dict.get('validation_dataset_uri') is not None
        has_weights = weight_column_name is not None
        contains_mltable = "training_dataset_uri" in dataset_dict

        """
        # TODO: Figure out the best place to save this
        if not has_weights:
            try:
                expr_store = ExperimentStore.get_instance()
                sample_weights = expr_store.data._get_sw_train()
            except Exception:
                pass
        """

        if pipeline is None:
            if is_autofeaturization:
                try:
                    mlflow.set_tracking_uri(parent_run.get_context().experiment.workspace.get_mlflow_tracking_uri())
                    uri = "runs:/" + parent_run.id + "/" + OUTPUT_PATH + "/" + Keys.EXP_TRANSFORMERS_CACHE_DIR
                    transformers = mlflow.sklearn.load_model(uri)
                    pipeline = transformers.get_transformers()[Transformers.X_TRANSFORMER]
                except Exception as e:
                    logger.error("Could not load transformers model via mlflow. ", e)
            else:
                tempdir = None
                try:
                    tempdir = tempfile.mkdtemp()

                    # Retrieve the preprocessor/algorithm sklearn pipeline
                    if is_forecasttcn:
                        child_run.download_file(PT_MODEL_PATH, tempdir)
                        pipeline_path = os.path.join(tempdir,
                                                     os.path.basename(PT_MODEL_PATH))
                        if torch.cuda.is_available():
                            map_location = 'cuda'
                        else:
                            map_location = 'cpu'
                        with open(pipeline_path, "rb") as f:
                            pipeline = torch.load(f, map_location=map_location)
                    else:
                        child_run.download_file(MODEL_PATH, tempdir)
                        pipeline_path = os.path.join(tempdir, os.path.basename(MODEL_PATH))
                        with open(pipeline_path, "rb") as f:
                            pipeline = pickle.load(f)

                finally:
                    if tempdir is not None:
                        shutil.rmtree(tempdir, ignore_errors=True)

        featurizer_template = featurizer_template_factory.select_template(pipeline, task_type)

        validation_task_template = validation_template_factory.select_template(
            task_type, metric_name, validation_dataset_exists, validation_size, n_cross_validations, n_step,
            y_min, y_max, is_timeseries, contains_mltable, is_forecasttcn, pipeline
        )

        output.extend(get_dataset_code(contains_mltable, FunctionNames.GET_TRAIN_DATASET_FUNC_NAME))
        output.append("\n")
        if validation_dataset_exists:
            output.extend(get_dataset_code(contains_mltable, FunctionNames.GET_VALID_DATASET_FUNC_NAME))
            output.append("\n")
        output.extend(
            get_prepare_data_code(validation_task_template, is_timeseries, label_column_name, weight_column_name,
                                  test_size)
        )
        output.append("\n")
        output.append(get_model_code(pipeline, featurizer_template, is_timeseries=is_timeseries))
        output.append("\n")

        if (is_autofeaturization):
            output.extend(get_fit_featurizer_code())
        else:
            if isinstance(pipeline, Pipeline):
                output.extend(get_train_model_code(pipeline, has_weights))
            else:
                is_dnn_train_valid_split = isinstance(
                    validation_task_template.validation_strategy, ForecastingDNNValidationDataStrategy)
                output.extend(get_dnn_train_model_code(pipeline, is_dnn_train_valid_split))
            output.append("\n")
            output.extend(validation_task_template.get_scoring_function().generate_code())
            output.append("\n")
            output.extend(validation_task_template.get_metrics_list_function().generate_code())
            output.append("\n")
            output.extend(validation_task_template.get_metrics_log_methods_function().generate_code())
        output.append("\n")
        output.extend(get_scriptrun_code(validation_dataset_exists, contains_mltable,
                      validation_task_template.validation_strategy, is_autofeaturization, is_forecasttcn))
        output.append("\n")
        output.append("if __name__ == '__main__':")
        output.append(get_dataset_parameter_code(dataset_dict))
        output.append("    try:")
        if validation_dataset_exists:
            if contains_mltable:
                output.append("        main(args.training_dataset_uri, args.validation_dataset_uri)")
            else:
                output.append("        main(args.training_dataset_id, args.validation_dataset_id)")
        else:
            if contains_mltable:
                output.append("        main(args.training_dataset_uri)")
            else:
                output.append("        main(args.training_dataset_id)")
        output.append("    except Exception as e:")
        output.append("        logging_utilities.log_traceback(e, logger)")
        output.append("        raise")

        output_str = "\n".join(output)

        # Experimental auto formatting. We can't rely on this until black has a proper public API
        # See https://github.com/psf/black/issues/779
        # Maybe we can also add some automated cleanup of unused imports?
        # https://stackoverflow.com/questions/54325116/can-i-handle-imports-in-an-abstract-syntax-tree
        try:
            import black

            return black.format_str(output_str, mode=black.Mode())
        except Exception:
            return output_str


def get_dataset_parameter_code(dataset_dict: Dict[str, str]) -> str:
    if 'training_dataset_id' in dataset_dict:
        output = [
            "    parser = argparse.ArgumentParser()",
            f"parser.add_argument('--training_dataset_id', type=str, default='{dataset_dict['training_dataset_id']}', \
    help='Default training dataset id is populated from the parent run')",
        ]

        if 'validation_dataset_id' in dataset_dict:
            output.append(
                f"parser.add_argument('--validation_dataset_id',  type=str, default='{dataset_dict['validation_dataset_id']}', \
    help='Default validation dataset id is populated from the parent run')")
    else:
        output = [
            "    parser = argparse.ArgumentParser()",
            f"parser.add_argument('--training_dataset_uri', type=str, default='{dataset_dict['training_dataset_uri']}', \
    help='Default training dataset uri is populated from the parent run')", ]

        if 'validation_dataset_uri' in dataset_dict:
            output.append(
                f"parser.add_argument('--validation_dataset_uri',  type=str, default='{dataset_dict['validation_dataset_uri']}', \
    help='Default validation dataset uri is populated from the parent run')")

    output.append("args = parser.parse_args()")
    output.append("")

    code_body = "\n".join(output)
    return _codegen_utilities.indent_multiline_string(code_body)


def get_dataset_code(contains_mltable: bool, dataset_func_name: str) -> List[str]:
    if contains_mltable:
        return get_dataset_code_from_uri(dataset_func_name)
    else:
        return get_dataset_code_from_id(dataset_func_name)


def get_dataset_code_from_id(dataset_func_name: str) -> List[str]:
    function = Function(dataset_func_name, "dataset_id")
    function.add_doc_string([
        "\'\'\'",
        "Loads the previously used dataset.",
        "",
        "It assumes that the script is run in an AzureML command job under the same workspace as the \
original experiment.",
        "\'\'\'",
    ])
    function.add_imports(Dataset, Run)
    function += [
        f'logger.info("Running {dataset_func_name}")',
        "ws = Run.get_context().experiment.workspace",
        "dataset = Dataset.get_by_id(workspace=ws, id=dataset_id)",
        "return dataset.to_pandas_dataframe()",
    ]

    return function.generate_code()


def get_dataset_code_from_uri(dataset_func_name: str) -> List[str]:
    function = Function(dataset_func_name, "dataset_uri")
    function.add_imports(AbstractDataset, Run)
    function += [
        f'logger.info("Running {dataset_func_name}")',
        "ws = Run.get_context().experiment.workspace",
        "dataset = AbstractDataset._load(dataset_uri, ws)",
        "return dataset.to_pandas_dataframe()",
    ]

    return function.generate_code()


def get_prepare_data_code(
    validation_task_template: AbstractTask,
    is_timeseries: bool,
    label_column_name: str,
    weight_column_name: Optional[str] = None,
    test_size: Optional[float] = None,
) -> List[str]:
    # TODO: make stuff from data_transformation.py publicly visible here
    #  such as label encoding, dropping NaN, etc
    function = Function(FunctionNames.PREPARE_DATA_FUNC_NAME, "dataframe")
    function.add_doc_string([
        "\'\'\'",
        "Prepares data for training.",
        "",
        "Cleans the data, splits out the feature and sample weight columns and prepares the data for use in training.",
        "This function can vary depending on the type of dataset and the experiment task type: classification,",
        "regression, or time-series forecasting.",
        "\'\'\'",
    ])
    function.add_imports(data_cleaning)
    function += [
        f'logger.info("Running {FunctionNames.PREPARE_DATA_FUNC_NAME}")',
        f"label_column_name = '{label_column_name}'",
        "",
        "# extract the features, target and sample weight arrays",
        "y = dataframe[label_column_name].values",
    ]

    if weight_column_name:
        function += [
            f"class_weights_column_name = '{weight_column_name}'",
            "X = dataframe.drop([label_column_name, class_weights_column_name], axis=1)",
            "sample_weights = dataframe[class_weights_column_name].values",
        ]
    else:
        function += ["X = dataframe.drop([label_column_name], axis=1)", "sample_weights = None"]

    # Remove the test set if needed
    if test_size is not None and test_size > 0.0 and validation_task_template.data_splitting_strategy is not None:
        function += [
            "",
            "# Split training data into train/test datasets and take only the train dataset",
            *validation_task_template.data_splitting_strategy.get_test_data_split_code(test_size),
        ]

    # TODO: Make this API public (#1277252)
    function += [
        "X, y, sample_weights = data_cleaning._remove_nan_rows_in_X_y(X, y, sample_weights,",
        f" is_timeseries={is_timeseries}, target_column=label_column_name)",
        "",
        "return X, y, sample_weights",
    ]

    return function.generate_code()


def get_model_code(
    model_object: Any,
    featurizer_template: AbstractFeaturizerTemplate,
    is_timeseries: bool,
) -> str:
    pipeline_step_templates = []            # type: List[PipelineStepTemplate]
    output = featurizer_template.generate_featurizer_code()
    if isinstance(model_object, (Pipeline, DataTransformer)):
        model = model_object if isinstance(model_object, DataTransformer) else model_object.steps[-1][1]
        is_autofeaturization = False
        if isinstance(model, (DataTransformer, TimeSeriesTransformer)):
            pipeline_step_templates = [featurizer_template]
            is_autofeaturization = True
        elif isinstance(model, (PreFittedSoftVotingRegressor, PreFittedSoftVotingClassifier)):
            model_template = EnsembleModelTemplate(model)  # type: AbstractModelTemplate
            output += model_template.generate_model_code()
            pipeline_step_templates = [featurizer_template, model_template]
        elif isinstance(model, StackEnsembleBase):
            model_template = StackEnsembleModelTemplate(model)
            output += model_template.generate_model_code()
            pipeline_step_templates = [featurizer_template, model_template]
        else:
            preproc_template = preprocessor_template_factory.select_template(model_object)
            model_template = SingleSklearnModelTemplate(model)
            output += preproc_template.generate_preprocessor_code()
            output += model_template.generate_model_code()
            pipeline_step_templates = [featurizer_template, preproc_template, model_template]

        has_y_transformer = False
        if isinstance(model_object, PipelineWithYTransformations):
            output.extend(get_y_transformer_code(model_object))
            has_y_transformer = True
        if is_timeseries:
            Contract.assert_type(model_object, "sklearn_pipeline", expected_types=ForecastingPipelineWrapper)
            model_object = cast(ForecastingPipelineWrapper, model_object)
            if isinstance(model_object.pipeline, PipelineWithYTransformations):
                output.extend(get_y_transformer_code(model_object.pipeline))
                has_y_transformer = True
            timeseries_stddev = cast(float, model_object.stddev)
            output.append(get_build_timeseries_model_pipeline_code(
                timeseries_stddev, featurizer_template, has_y_transformer))
        else:
            output.append(get_build_model_pipeline_code_from_templates(
                pipeline_step_templates, has_y_transformer, is_autofeaturization))
    else:
        # DNN models aren't wrapped in Pipelines but handle a bunch of stuff internally.
        model_template = SingleForecastDnnModelTemplate(model_object)
        output.extend(model_template.generate_model_code())

    return "\n".join(output)


def get_y_transformer_code(pipeline: Pipeline) -> List[str]:
    y_transformer = pipeline.y_transformer

    function = Function(FunctionNames.Y_TRANSFORMER_FUNC_NAME, "pipeline")
    function.add_imports(y_transformer.__class__, PipelineWithYTransformations)
    function += [
        f'transformer = {y_transformer}',
        f'transformer_name = "{y_transformer.__class__.__name__}"',
        "return PipelineWithYTransformations(pipeline, transformer_name, transformer)",
        ""
    ]

    return function.generate_code()


def get_build_model_pipeline_code_from_templates(
        pipeline_step_templates: List[PipelineStepTemplate],
        has_y_transformer: bool, is_autofeaturization: bool = False) -> str:
    func_name = FunctionNames.BUILD_MODEL_FUNC_NAME

    if (is_autofeaturization):
        func_name = FunctionNames.BUILD_FEATURIZER_FUNC_NAME

    output = [f"def {func_name}():"]

    output.extend([
        "\'\'\'",
        "Defines the scikit-learn pipeline steps.",
        "\'\'\'",
    ])
    imports = [_codegen_utilities.get_import(Pipeline)]
    output.extend(_codegen_utilities.generate_import_statements(imports))
    output.append("")

    output.append(f'logger.info("Running {func_name}")')
    output.append("pipeline = Pipeline(")
    output.append("    steps=[")

    for template in pipeline_step_templates:
        output.extend(_codegen_utilities.indent_lines(template.generate_pipeline_step(), 8))

    output.append("    ]")
    output.append(")")
    output.append("")

    if has_y_transformer:
        output.append(f"return {FunctionNames.Y_TRANSFORMER_FUNC_NAME}(pipeline)")
    else:
        output.append("return pipeline")

    code_body = "\n".join(output)
    return _codegen_utilities.indent_multiline_string(code_body)


def get_build_timeseries_model_pipeline_code(
    stddev: Optional[float], featurizer_template: AbstractFeaturizerTemplate, has_y_transformer: bool
) -> str:
    output = [f"def {FunctionNames.BUILD_MODEL_FUNC_NAME}():"]

    output.extend([
        "\'\'\'",
        "Defines the scikit-learn pipeline steps.",
        "",
        "For time-series forecasting models, the scikit-learn pipeline is wrapped in a ForecastingPipelineWrapper,",
        "which has some additional logic needed to properly handle time-series data depending on the applied \
algorithm.",
        "\'\'\'",
    ])

    imports = [
        _codegen_utilities.get_import(Pipeline),
        _codegen_utilities.get_import(ForecastingPipelineWrapper),
    ]
    output.extend(_codegen_utilities.generate_import_statements(imports))
    output.append("")

    output.append(f'logger.info("Running {FunctionNames.BUILD_MODEL_FUNC_NAME}")')
    output.append("pipeline = Pipeline(")
    output.append("    steps=[")
    output.extend(_codegen_utilities.indent_lines(featurizer_template.generate_pipeline_step(), 8))
    output.append(f"        ('model', {FunctionNames.MODEL_FUNC_NAME}())")
    output.append("    ]")
    output.append(")")
    var_name = "pipeline"
    if has_y_transformer:
        var_name = "y_transformer_pipeline"
        output.append(f"{var_name} = {FunctionNames.Y_TRANSFORMER_FUNC_NAME}(pipeline)")
    output.append(f"forecast_pipeline_wrapper = ForecastingPipelineWrapper({var_name}, stddev={stddev})")
    output.append("")
    output.append("return forecast_pipeline_wrapper")

    code_body = "\n".join(output)
    return _codegen_utilities.indent_multiline_string(code_body)


def get_fit_featurizer_code() -> List[str]:
    function = Function(FunctionNames.FIT_FEATURIZER_FUNC_NAME, "X", "y")
    function += [
        f'logger.info("Running {FunctionNames.FIT_FEATURIZER_FUNC_NAME}")',
        f"featurizer_pipeline = {FunctionNames.BUILD_FEATURIZER_FUNC_NAME}()",
        "",
    ]

    function += "featurizer = featurizer_pipeline.fit(X, y)"
    function += "return featurizer"

    return function.generate_code()


def get_train_model_code(pipeline: Pipeline, use_weights: bool) -> List[str]:
    function = Function(FunctionNames.TRAIN_MODEL_FUNC_NAME, "X", "y", "sample_weights=None", "transformer=None")

    function.add_doc_string([
        "\'\'\'",
        "Calls the fit() method to train the model.",
        "",
        "The return value is the model fitted/trained on the input data.",
        "\'\'\'",
    ])
    function += [
        f'logger.info("Running {FunctionNames.TRAIN_MODEL_FUNC_NAME}")',
        f"model_pipeline = {FunctionNames.BUILD_MODEL_FUNC_NAME}()",
        "",
    ]
    """
    # Taken from _ml_engine/training/train.py
    # Add sample weights if model supports it
    # TODO: This doesn't work all the time. Re-enable when it does
    classifier_name = pipeline.steps[-1][0]
    if use_weights and classifier_name not in Sample_Weights_Unsupported:
        # pipeline expects kwargs to be formatted as stepname__arg.
        # The arg is then passed to fit of stepname
        function += f"model = model_pipeline.fit(" \
                    f"X, y, **{{f'{{model_pipeline.steps[-1][0]}}__sample_weight': sample_weights}})"
    else:
    """
    function += "model = model_pipeline.fit(X, y)"
    function += "return model"

    return function.generate_code()


def get_dnn_train_model_code(pipeline: Any, is_train_valid_split: bool) -> List[str]:
    if is_train_valid_split:
        function = Function(FunctionNames.TRAIN_MODEL_FUNC_NAME, "X", "y", "X_valid", "y_valid", "transformer")
    else:
        function = Function(FunctionNames.TRAIN_MODEL_FUNC_NAME, "X", "y", "transformer=None")
    function += [
        f'logger.info("Running {FunctionNames.TRAIN_MODEL_FUNC_NAME}")',
        "",
    ]
    n_epochs = pipeline.params.get_value("num_epochs")
    function += [
        "df = transformer.transform(X, y).sort_index()",
        f"y = df[['{TimeSeriesInternal.DUMMY_TARGET_COLUMN}']]",
        f"X = df.drop(columns=['{TimeSeriesInternal.DUMMY_TARGET_COLUMN}'])",
    ]
    if is_train_valid_split:
        function += [
            "valid_df = transformer.transform(X_valid, y_valid).sort_index()",
            f"y_valid = valid_df[['{TimeSeriesInternal.DUMMY_TARGET_COLUMN}']]",
            f"X_valid = valid_df.drop(columns=['{TimeSeriesInternal.DUMMY_TARGET_COLUMN}'])",
        ]
    function += [
        f"model = {FunctionNames.MODEL_FUNC_NAME}()",
    ]

    if is_train_valid_split:
        function += [
            f"model.train(n_epochs={n_epochs}, X_train=X, y_train=y, X_valid=X_valid, y_valid=y_valid, \
                featurizer=transformer)",
        ]
    else:
        function += [
            f"model.train(n_epochs={n_epochs}, X_train=X, y_train=y, featurizer=transformer)",
        ]
    function += "return model"

    return function.generate_code()


def get_scriptrun_code(
        validation_dataset_exists: bool,
        contains_mltable: bool,
        validation_strategy: AbstractValidationStrategy,
        is_autofeaturization: bool = False,
        is_forecasttcn: bool = False
) -> List[str]:
    if validation_dataset_exists:
        if contains_mltable:
            function = Function("main", "training_dataset_uri=None", "validation_dataset_uri=None")
        else:
            function = Function("main", "training_dataset_id=None", "validation_dataset_id=None")
    else:
        if contains_mltable:
            function = Function("main", "training_dataset_uri=None")
        else:
            function = Function("main", "training_dataset_id=None")

    function.add_doc_string([
        "\'\'\'",
        "Runs all functions defined above.",
        "\'\'\'",
    ])
    function.add_imports(Run)

    if is_autofeaturization:
        function += [
            "import scipy",
            "",
        ]
    else:
        function.add_imports(inference)
        function += [
            "import mlflow",
            "",
        ]

    if contains_mltable:
        assign_train_df = f"df = {FunctionNames.GET_TRAIN_DATASET_FUNC_NAME}(training_dataset_uri)"
    else:
        assign_train_df = f"df = {FunctionNames.GET_TRAIN_DATASET_FUNC_NAME}(training_dataset_id)"

    function += [
        "# The following code is for when running this code as part of an AzureML script run.",
        "run = Run.get_context()",
        "",
        assign_train_df,
        f"X, y, sample_weights = {FunctionNames.PREPARE_DATA_FUNC_NAME}(df)",
    ]
    if (is_autofeaturization):
        function += [
            f"featurizer = {FunctionNames.FIT_FEATURIZER_FUNC_NAME}(X, y)",
            "",
            "featurized_train_data = featurizer.transform(X)",
            "",
        ]
    else:
        scoring_import_tuples, code_body = validation_strategy.get_scoring_code()
        function.add_import_tuples(scoring_import_tuples)
        function += code_body
        function += [
            f"metrics_log_methods = {FunctionNames.GET_METRICS_LOG_METHODS}()",
            "print(metrics)",
            "for metric in metrics:",
            "    if metrics_log_methods[metric] == 'None':",
            "        logger.warning(\"Unsupported non-scalar metric {}. Will not log.\".format(metric))",
            "    elif metrics_log_methods[metric] == 'Skip':",
            "        pass # Forecasting non-scalar metrics and unsupported classification metrics are not logged",
            "    else:",
            "        getattr(run, metrics_log_methods[metric])(metric, metrics[metric])",
        ]

    if(is_autofeaturization):
        file_name = 'full_training_dataset.parquet'
        function += [
            f"file_name = '{file_name}'",
            "",
            "if scipy.sparse.issparse(featurized_train_data):",
            "    featurized_train_data = featurized_train_data.todense()",
            "",
            "col = list(range(featurized_train_data.shape[1]))",
            "",
            "featurized_train_data_df = pd.DataFrame(data = featurized_train_data, columns = col)",
            "featurized_train_data_df.columns = [str(c) for c in featurized_train_data_df.columns]",
            "featurized_train_data_df.to_parquet(file_name, compression=\"gzip\")",
            "",
            f"run.upload_file('outputs/featurization/data/{file_name}', '{file_name}')",
        ]
    else:
        function += get_save_mlflow_model_code('model', 'outputs/', 'outputs/', is_forecasttcn)

    return function.generate_code()


def get_save_mlflow_model_code(
        model_name: str, output_dir: str, artifacts_path: str, is_forecasttcn: bool = False
) -> List[str]:
    if is_forecasttcn:
        return [
            "cd = inference.get_conda_deps_as_dict(True)",
            "",
            f"# Saving ML model to {output_dir}.",
            "signature = mlflow.models.signature.infer_signature(X, y)",
            "mlflow.pytorch.log_model(",
            f"    pytorch_model={model_name},",
            f"    artifact_path='{output_dir}',",
            "    conda_env=cd,",
            "    signature=signature,",
            "    pickle_module=pickle)",
            "",
            f"run.upload_folder('{output_dir}', '{artifacts_path}')"]
    else:
        return [
            "cd = inference.get_conda_deps_as_dict(True)",
            "",
            f"# Saving ML model to {output_dir}.",
            "signature = mlflow.models.signature.infer_signature(X, y)",
            "mlflow.sklearn.log_model(",
            f"    sk_model={model_name},",
            f"    artifact_path='{output_dir}',",
            "    conda_env=cd,",
            "    signature=signature,",
            "    serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_PICKLE)",
            "",
            f"run.upload_folder('{output_dir}', '{artifacts_path}')"]
