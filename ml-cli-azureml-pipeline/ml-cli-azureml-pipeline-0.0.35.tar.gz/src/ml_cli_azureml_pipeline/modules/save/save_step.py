import json
from pathlib import Path
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration

def save_step(
    compute_target,
    environment,
    img_dir,
    save_datastore_name,
    path_on_datastore,
    chunk_index,
    save_datasets,
    name="Save"
):

    run_config = RunConfiguration()
    run_config.target = compute_target
    run_config.environment = environment
    print("Run configuration created for the data saving step")

    step = PythonScriptStep(
        script_name="save.py",
        name=name,
        arguments=[
            "--img_dir",
            img_dir,
            "--chunk_index",
            chunk_index,
            "--save_datastore_name",
            save_datastore_name,
            "--save_datastore_path",
            path_on_datastore,
            "--save_datasets_json",
            json.dumps(save_datasets),
        ],
        inputs=[img_dir],
        compute_target=compute_target,
        runconfig=run_config,
        source_directory=Path(__file__).resolve().parent,
        allow_reuse=False,
    )

    return step
