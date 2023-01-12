# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods for AutoML remote runs."""
import numpy as np
import logging
import mlflow

from datetime import datetime
from typing import Any, List, Optional

from azureml._tracing import get_tracer
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.telemetry_activity_logger import TelemetryActivityLogger
from azureml.automl.runtime import cpu_utilities
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.onnx_convert.onnx_converter import OnnxConverter
from azureml.automl.runtime.shared.limit_function_call_spawn import EnforceLimits
from azureml.core import Run
from azureml.core.workspace import Workspace
from azureml.train.automl import _logging   # type: ignore
from azureml.train.automl._constants_azureml import CodePaths
from azureml.train.automl.runtime._automl_job_phases import BatchTrainingPhase
from azureml.train.automl.runtime._entrypoints import entrypoint_util, training_entrypoint_util

logger = logging.getLogger(__name__)
activity_logger = TelemetryActivityLogger()
tracer = get_tracer(__name__)


def execute(
        script_directory: str,
        automl_settings: str,
        dataprep_json: str,
        child_run_ids: List[str],
        **kwargs: Any
) -> None:
    """
    Driver script that runs given child runs that contain pipelines
    """
    batch_job_run = Run.get_context()  # current batch job context

    try:
        print("{} - INFO - Beginning batch driver wrapper.".format(datetime.now().__format__('%Y-%m-%d %H:%M:%S,%f')))
        logger.info('Beginning AutoML remote batch driver for {}.'.format(batch_job_run.id))

        parent_run, automl_settings_obj, cache_store = entrypoint_util.init_wrapper(
            batch_job_run, automl_settings, script_directory, code_path=CodePaths.BATCH_REMOTE, **kwargs)

        if automl_settings_obj.enable_streaming:
            entrypoint_util.modify_settings_for_streaming(automl_settings_obj, dataprep_json)

        expr_store = ExperimentStore(cache_store, read_only=True)
        expr_store.load()
        onnx_cvt = training_entrypoint_util.load_onnx_converter(
            automl_settings_obj, cache_store, parent_run.id)  # type: Optional[OnnxConverter]

        num_procs = automl_settings_obj.num_procs
        max_available_cores = cpu_utilities.get_cpu_core_count() - 1
        if not num_procs or num_procs > max_available_cores:
            num_procs = max_available_cores
            logger.info("Changing num_procs to be {}, which is one less than this machine's number of cores".format(
                num_procs))

        # For one or two core machines, we do not parallelize child runs
        if not automl_settings_obj.enable_parallel_run or num_procs <= 1:
            BatchTrainingPhase.run(
                automl_parent_run=parent_run,
                child_run_ids=child_run_ids,
                automl_settings=automl_settings_obj,
                onnx_cvt=onnx_cvt,
            )

        else:
            run_parallel(
                script_directory=script_directory,
                automl_settings=automl_settings,
                dataprep_json=dataprep_json,
                child_run_ids=child_run_ids,
                num_procs=num_procs,
                mem_in_mb=automl_settings_obj.mem_in_mb,
                **kwargs
            )

        _logging.set_run_custom_dimensions(
            automl_settings=automl_settings_obj,
            parent_run_id=parent_run.id,
            child_run_id=batch_job_run.id,
            code_path=CodePaths.BATCH_REMOTE
        )

        logger.info("No more training iteration task in the queue, ending the script run for {}"
                    .format(batch_job_run.id))
        run_lifecycle_utilities.complete_run(batch_job_run)

    except Exception as e:
        logger.error("AutoML batch_driver_wrapper script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(batch_job_run, e)
        raise
    finally:
        # Reset the singleton for subsequent usage.
        ExperimentStore.reset()


def run_parallel(
        script_directory: str,
        automl_settings: str,
        dataprep_json: str,
        child_run_ids: List[str],
        num_procs: int,
        mem_in_mb: Optional[int],
        **kwargs: Any
) -> None:
    """
    Run training iterations in parallel for given child run ids

    :param script_directory: The current working directory
    :param automl_settings:  AutoMl settings for current run
    :param dataprep_json: Settings for UI
    :param child_run_ids:  List of child run ids to train
    :param num_procs: The amount of processes that can be used to execute the child jobs
    :param mem_in_mb: The amount of memory each iteration is limited to
    :return:
    """
    grouped_child_run_ids = _divide_child_jobs(child_run_ids, num_procs)
    if mem_in_mb:
        # Increase mem_in_mb to be the max number of child runs in a group since
        # mem_in_mb is the amount of memory for a single iteration
        mem_in_mb *= max([len(group) for group in grouped_child_run_ids])

    functions, args, _kwargs = [], [], []
    for group in grouped_child_run_ids:
        functions.append(_run)
        args.append((script_directory, automl_settings, dataprep_json, group))
        _kwargs.append(kwargs)

    process = EnforceLimits(mem_in_mb=mem_in_mb)
    _, error, _ = process.execute_multiple(working_dir=script_directory,
                                           functions=functions, args=args, kwargs=_kwargs)

    if error:
        logger.error("One or more processes finished with an error. The last error captured was {}".format(
            error.__class__.__name__))
        logging_utilities.log_traceback(error, logger)
    else:
        logger.info("Batched jobs ran in parallel successfully")


def _run(
    script_directory: str,
    automl_settings: str,
    dataprep_json: str,
    child_run_ids: List[str],
    **kwargs: Any
) -> None:
    """
    Run training iterations for given child run ids

    :param script_directory: The current working directory
    :param automl_settings: AutoMl settings for current run
    :param dataprep_json: Settings for UI
    :param child_run_ids: List of child run ids to train
    :return:
    """
    batch_job_run = Run.get_context()  # current batch job context

    try:
        automl_parent_run, automl_settings_obj, cache_store = entrypoint_util.init_wrapper(
            batch_job_run, automl_settings, script_directory, code_path=CodePaths.BATCH_REMOTE, **kwargs)

        if automl_settings_obj.enable_streaming:
            entrypoint_util.modify_settings_for_streaming(automl_settings_obj, dataprep_json)

        expr_store = ExperimentStore(cache_store, read_only=True)
        expr_store.load()
        onnx_cvt = training_entrypoint_util.load_onnx_converter(
            automl_settings_obj, cache_store, automl_parent_run.id)  # type: Optional[OnnxConverter]

        # tracking uri gets lost while inside subprocess. Need to reset it here so that mlflow works
        workspace = automl_parent_run.experiment.workspace  # type: Workspace
        mlflow.set_tracking_uri(workspace.get_mlflow_tracking_uri())

        BatchTrainingPhase.run(
            automl_parent_run=automl_parent_run,
            child_run_ids=child_run_ids,
            automl_settings=automl_settings_obj,
            onnx_cvt=onnx_cvt,
        )

    finally:
        ExperimentStore.reset()


def _divide_child_jobs(child_run_ids: List[str], num_procs: int) -> List[List[str]]:
    """
    :param child_run_ids: List of child run ids to train
    :param num_procs: The number of processes to use to run the jobs in child_run_ids
    :return: A list containing lists of child run ids that processes should execute
    """
    grouped = np.array_split(child_run_ids, num_procs)
    grouped_child_run_ids = []
    for group in grouped:
        if group.size:
            grouped_child_run_ids.append(list(group))
    return grouped_child_run_ids
