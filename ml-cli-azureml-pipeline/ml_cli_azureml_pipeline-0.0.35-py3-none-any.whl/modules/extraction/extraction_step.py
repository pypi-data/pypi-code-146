from pathlib import Path
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration
from azureml.core.runconfig import DockerConfiguration
from azureml.pipeline.core import PipelineData


def extraction_step(
    compute_target,
    environment,
    datastore,
    raw_data_dir,
    chunk_index:int,
    mlcli_template:str,
    name="Extract Features",
):
    """
    This step will use the production algorithm
    to convert pdf,png,jpg,tiff to png

    Args:
        compute_target: The compute target to run the step on
        environment: The environment in which to run the script
        datastore: The datastore that will be used
        raw_data_dir: The reference to the directory containing the data
        name: Action name of the node

    Returns:
        The step, the step outputs dictionary
    """

    run_config = RunConfiguration()
    run_config.target = compute_target
    run_config.environment = environment

    docker_config = DockerConfiguration(use_docker=True)
    run_config.docker = docker_config
    print("Run configuration created for the extraction step")

    data_output_dir = PipelineData(
        name="data_output_dir",
        datastore=datastore,
        is_directory=True,
    )

    outputs_map = {"data_output_dir": data_output_dir}

    step = PythonScriptStep(
        script_name="extraction.py",
        name=name,
        arguments=[
            "--module-name",
            "extraction",
            "--raw-data-dir",
            raw_data_dir,
            "--data-output-dir",
            data_output_dir,
            "--chunk-index",
            chunk_index,
            "--ml_cli_azureml_pipeline-template",
            mlcli_template,
        ],
        inputs=[raw_data_dir],
        outputs=[data_output_dir],
        compute_target=compute_target,
        runconfig=run_config,
        source_directory=Path(__file__).resolve().parent,
        allow_reuse=False,
    )

    return step, outputs_map
