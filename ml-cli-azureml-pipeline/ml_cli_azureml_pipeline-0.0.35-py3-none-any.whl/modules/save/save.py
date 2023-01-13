import argparse
import json
from pathlib import Path
from azureml.core import Run, Dataset
from azureml.core.datastore import Datastore
from azureml.data.datapath import DataPath

# Get parameters
parser = argparse.ArgumentParser()
parser.add_argument(
    '--img_dir', type=str, help='Directory where images to save are stored'
)
parser.add_argument('--save_datastore_name', type=str, help='save datastore name')
parser.add_argument('--save_datastore_path', type=str, help='save datastore path')
parser.add_argument("--save_datasets_json", type=str, help="Dataset json")

parser.add_argument('--chunk_index', type=str, help='index of the current chunk')

# Get arguments from parser
args = parser.parse_args()
img_dir = args.img_dir
# datastore_name = args.datastore_name
chunk_index = args.chunk_index
save_datastore_name = args.save_datastore_name
save_datastore_path = args.save_datastore_path
save_datasets = json.loads(args.save_datasets_json)

# Get the experiment run context
run = Run.get_context()
workspace = run.experiment.workspace

# Load data
print("Loading Data...")
data_output_dir_path = Path(img_dir)

# summary_filename = "summary_chunk" + str(chunk_index) + ".json"
chunk_name = "chunk" + str(chunk_index)
json_chunk_name = "json" + chunk_name
output_jsons = str(data_output_dir_path / json_chunk_name)
# create_summary(output_jsons, str(data_output_dir_path / summary_filename))

datastore = Datastore.get(workspace, save_datastore_name)
dataset = Dataset.File.upload_directory(
    src_dir=str(data_output_dir_path), target=DataPath(datastore, save_datastore_path), pattern="*", show_progress=True,
    overwrite=True
)

output_jsons_path = Path(output_jsons)
if output_jsons_path.is_dir():
    dir_list = [p for p in Path(output_jsons).iterdir() if p.is_dir()]

    for dir_path in dir_list:
        dir_name = dir_path.name
        source = str(output_jsons_path / dir_name)
        dummy_path = str(output_jsons_path / dir_name / 'dummy.json')

        subdir_list = [p for p in Path(source).iterdir() if p.is_dir()]
        subfiles_list = [p for p in Path(source).iterdir() if p.is_file()]
        if len(subfiles_list) <= 0 < len(subdir_list):
            Dataset.File.upload_directory(
                src_dir=source, target=DataPath(datastore, str(Path(save_datastore_path) / dir_name)), pattern="*",
                show_progress=True,
                overwrite=True
            )

        for subdir_path in subdir_list:
            subdirname = subdir_path.name
            destination = str(Path(save_datastore_path) / dir_name / subdirname)
            sub_source = str(Path(subdir_path) / dir_name / subdirname)
            Dataset.File.upload_directory(
                src_dir=sub_source, target=DataPath(datastore, destination), pattern="*",
                show_progress=True,
                overwrite=True
            )

for dataset in save_datasets:
    file_data_set = Dataset.File.from_files(path=(datastore, save_datastore_path + '/' + dataset["pattern"]))
    registered_dataset = file_data_set.register(
        workspace=workspace,
        name=dataset["name"],
        description=dataset["description"],
        tags={},
        create_new_version=True,
    )
    print("Registered dataset: " + registered_dataset.name + ' version: ' + str(registered_dataset.version))

# End the run
run.complete()
