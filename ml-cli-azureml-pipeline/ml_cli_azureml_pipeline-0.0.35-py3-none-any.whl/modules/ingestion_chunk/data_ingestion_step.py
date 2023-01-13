import json
from pathlib import Path
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.core import PipelineData


def data_ingestion_step(
    compute_target,
    environment,
    datastore,
    datasets:[],
    number_chunk:int,
    chunk_index:int,
    name="Ingest Data",
):
    """
    This step will ingest data from the specified dataset and pass it to
    the next step as a temporary data reference.

    Args:
        compute_target: The compute target to run the step on
        environment: The environment in which to run the script
        datastore: The datastore that will be used
        name: Action name of the node

    Returns:
        The step, the step outputs dictionary
    """

    run_config = RunConfiguration()
    run_config.target = compute_target
    run_config.environment = environment
    print("Run configuration created for the data ingestion step")

    raw_data_dir = PipelineData(
        name="raw_data_dir",
        datastore=datastore,
        is_directory=True,
    )

    outputs = [raw_data_dir]
    outputs_map = {"raw_data_dir": raw_data_dir}

    step = PythonScriptStep(
        script_name="data_ingestion.py",
        name=name,
        arguments=[
            "--datasets_json",
            json.dumps(datasets),
            "--raw_data_dir",
            raw_data_dir,
            "--number_chunk",
            number_chunk,
            "--chunk_index",
            chunk_index
        ],
        outputs=outputs,
        compute_target=compute_target,
        source_directory=Path(__file__).resolve().parent,
        runconfig=run_config,
        allow_reuse=True,
    )

    return step, outputs_map
