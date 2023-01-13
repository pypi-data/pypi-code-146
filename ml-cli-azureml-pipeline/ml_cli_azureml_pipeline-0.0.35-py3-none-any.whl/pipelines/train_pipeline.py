from datetime import datetime

from azureml.pipeline.core import Pipeline

from ..modules.ingestion_chunk.data_ingestion_step import data_ingestion_step
from ..modules.extraction.extraction_step import extraction_step
from ..modules.save.save_step import save_step


def train_pipeline(workspace, datastore, clusters, environments, dataset_dict, mlcli_template:str):

    number_chunk = dataset_dict["inputs"]["number_chunk"]
    start_at_chunk_index = dataset_dict["inputs"]["start_at_chunk_index"]

    steps = []
    previous_data_extraction_step = None
    previous_previous_data_extraction_step = None
    previous_data_injection_step = None
    for chunk_index in range(number_chunk):
        if start_at_chunk_index > chunk_index:
            continue
        # Data ingestion
        data_ingestion, data_ingestion_outputs = data_ingestion_step(
            clusters[0],
            environments[0],
            datastore,
            dataset_dict["inputs"]["datasets"],
            name="Data Ingestion",
            number_chunk=number_chunk,
            chunk_index=chunk_index
        )
        steps.append(data_ingestion)

        if previous_data_injection_step is not None:
            data_ingestion.run_after(previous_data_injection_step)

        if previous_previous_data_extraction_step is not None:
            data_ingestion.run_after(previous_previous_data_extraction_step)
        previous_data_injection_step = data_ingestion

        # Data extraction
        data_extraction, data_extraction_outputs = extraction_step(
            clusters[0],
            environments[1],
            datastore,
            data_ingestion_outputs["raw_data_dir"],
            chunk_index,
            mlcli_template,
            name="Data Extraction"
        )
        steps.append(data_extraction)

        if previous_data_extraction_step is not None:
            data_extraction.run_after(previous_data_extraction_step)
        previous_previous_data_extraction_step = previous_data_extraction_step
        previous_data_extraction_step = data_extraction


        path_on_datastore = dataset_dict["outputs"]["path_on_datastore"]
        date_folder_name = datetime.now().strftime("%d-%m-%Y_%Hh%M")
        updated_path_on_datastore = path_on_datastore.replace("{date}", date_folder_name)
        save = save_step(
            clusters[0],
            environments[0],
            data_extraction_outputs["data_output_dir"],
            dataset_dict["outputs"]["datastore_name"],
            updated_path_on_datastore,
            chunk_index,
            dataset_dict["outputs"]["datasets"],
            name="Save",
        )

        steps.append(save)
        save.run_after(data_extraction)

    pipeline = Pipeline(
        workspace=workspace,
        steps=steps,
    )

    print("Pipeline is built.")
    return pipeline
