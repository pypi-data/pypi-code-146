from roboflow2huggingface.roboflow_utils import read_roboflow_info
from pathlib import Path


def export_hf_image_classification_dataset_script(
    hf_dataset_id,
    dataset_labels,
    roboflow_dataset,
    export_dir,
    roboflow_universe_url: str = None,
):
    """
    Exports a HuggingFace dataset script for a Roboflow image classification dataset.

    Args:
        hf_dataset_id (str): HuggingFace dataset id
        dataset_labels (list): List of labels as strings
        roboflow_dataset (roboflow.core.version.Version): Roboflow dataset object
        export_dir (str): Directory to export the dataset script to
        roboflow_universe_url (str): Roboflow Universe URL
    """

    license, dataset_url, citation, _ = read_roboflow_info(
        local_data_dir=export_dir, roboflow_universe_url=roboflow_universe_url
    )
    dataset_name = hf_dataset_id.split("/")[-1]
    urls = (
        f"""{{
    "train": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/train.zip",
    "validation": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/valid.zip",
    "test": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/test.zip",
}}
"""
        if "test" in roboflow_dataset.splits.keys()
        else f"""{{
    "train": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/train.zip",
    "validation": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/valid.zip",
}}
"""
    )

    splits = (
        """[
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": dl_manager.iter_files([data_files["train"]]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "files": dl_manager.iter_files([data_files["validation"]]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "files": dl_manager.iter_files([data_files["test"]]),
                },
            ),
]"""
        if "test" in roboflow_dataset.splits.keys()
        else """[
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": dl_manager.iter_files([data_files["train"]]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "files": dl_manager.iter_files([data_files["validation"]]),
                },
            ),
]"""
    )

    classification_dataset_script_template = f'''import os

import datasets
from datasets.tasks import ImageClassification


_HOMEPAGE = "{dataset_url}"
_LICENSE = "{license}"
_CITATION = """\\
{citation}
"""
_URLS = {urls}
_CATEGORIES = {dataset_labels}


class {dataset_name.upper().replace('-', '')}(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features(
                {{
                    "image_file_path": datasets.Value("string"),
                    "image": datasets.Image(),
                    "labels": datasets.features.ClassLabel(names=_CATEGORIES),
                }}
            ),
            supervised_keys=("image", "labels"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            license=_LICENSE,
            task_templates=[ImageClassification(image_column="image", label_column="labels")],
        )

    def _split_generators(self, dl_manager):
        data_files = dl_manager.download_and_extract(_URLS)
        return {splits}

    def _generate_examples(self, files):
        for i, path in enumerate(files):
            file_name = os.path.basename(path)
            if file_name.endswith((".jpg", ".png", ".jpeg", ".bmp", ".tif", ".tiff")):
                yield i, {{
                    "image_file_path": path,
                    "image": path,
                    "labels": os.path.basename(os.path.dirname(path)),
                }}
'''

    with open(Path(export_dir) / f"{dataset_name}.py", "w") as f:
        f.write(classification_dataset_script_template)
