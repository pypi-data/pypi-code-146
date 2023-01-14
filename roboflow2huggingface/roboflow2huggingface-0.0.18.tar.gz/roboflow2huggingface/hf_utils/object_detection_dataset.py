from roboflow2huggingface.roboflow_utils import read_roboflow_info


def export_hf_object_detection_dataset_script(
    hf_dataset_id,
    dataset_labels,
    roboflow_dataset,
    export_dir,
    roboflow_universe_url=None,
):
    """
    Exports a HuggingFace dataset script for a Roboflow object detection dataset.

    Args:
        hf_dataset_id (str): HuggingFace dataset id
        dataset_labels (list): List of labels as strings
        roboflow_dataset (roboflow.core.version.Version): Roboflow dataset object
        export_dir (str): Directory to export the dataset script to
    """
    from pathlib import Path

    license, dataset_url, citation, _ = read_roboflow_info(
        local_data_dir=export_dir, roboflow_universe_url=roboflow_universe_url
    )
    dataset_name = hf_dataset_id.split("/")[-1]

    urls = (
        f"""{{
                "train": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/train.zip",
                "validation": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/valid.zip",
                "test": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/test.zip",
            }}"""
        if "test" in roboflow_dataset.splits.keys()
        else f"""{{
                "train": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/train.zip",
                "validation": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/valid.zip",
            }}"""
    )

    mini_urls = (
        f"""{{
                "train": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/valid-mini.zip",
                "validation": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/valid-mini.zip",
                "test": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/valid-mini.zip",
            }}"""
        if "test" in roboflow_dataset.splits.keys()
        else f"""{{
                "train": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/valid-mini.zip",
                "validation": "https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/data/valid-mini.zip",
            }}"""
    )

    splits = (
        """[
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "folder_dir": data_files["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "folder_dir": data_files["validation"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "folder_dir": data_files["test"],
                },
            ),
]"""
        if "test" in roboflow_dataset.splits.keys()
        else """[
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "folder_dir": data_files["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "folder_dir": data_files["validation"],
                },
            ),
]"""
    )

    detection_dataset_script_template = f'''import collections
import json
import os

import datasets


_HOMEPAGE = "{dataset_url}"
_LICENSE = "{license}"
_CITATION = """\\
{citation}
"""
_CATEGORIES = {dataset_labels}
_ANNOTATION_FILENAME = "_annotations.coco.json"

class {dataset_name.upper().replace('-', '')}Config(datasets.BuilderConfig):
    """Builder Config for {dataset_name}"""

    def __init__(self, data_urls, **kwargs):
        """
        BuilderConfig for {dataset_name}.

        Args:
          data_urls: `dict`, name to url to download the zip file from.
          **kwargs: keyword arguments forwarded to super.
        """
        super({dataset_name.upper().replace('-', '')}Config, self).__init__(version=datasets.Version("1.0.0"), **kwargs)
        self.data_urls = data_urls


class {dataset_name.upper().replace('-', '')}(datasets.GeneratorBasedBuilder):
    """{dataset_name} object detection dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        {dataset_name.upper().replace('-', '')}Config(
            name="full",
            description="Full version of {dataset_name} dataset.",
            data_urls={urls},
        ),
        {dataset_name.upper().replace('-', '')}Config(
            name="mini",
            description="Mini version of {dataset_name} dataset.",
            data_urls={mini_urls},
        )
    ]

    def _info(self):
        features = datasets.Features(
            {{
                "image_id": datasets.Value("int64"),
                "image": datasets.Image(),
                "width": datasets.Value("int32"),
                "height": datasets.Value("int32"),
                "objects": datasets.Sequence(
                    {{
                        "id": datasets.Value("int64"),
                        "area": datasets.Value("int64"),
                        "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                        "category": datasets.ClassLabel(names=_CATEGORIES),
                    }}
                ),
            }}
        )
        return datasets.DatasetInfo(
            features=features,
            homepage=_HOMEPAGE,
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        data_files = dl_manager.download_and_extract(self.config.data_urls)
        return {splits}

    def _generate_examples(self, folder_dir):
        def process_annot(annot, category_id_to_category):
            return {{
                "id": annot["id"],
                "area": annot["area"],
                "bbox": annot["bbox"],
                "category": category_id_to_category[annot["category_id"]],
            }}

        image_id_to_image = {{}}
        idx = 0

        annotation_filepath = os.path.join(folder_dir, _ANNOTATION_FILENAME)
        with open(annotation_filepath, "r") as f:
            annotations = json.load(f)
        category_id_to_category = {{category["id"]: category["name"] for category in annotations["categories"]}}
        image_id_to_annotations = collections.defaultdict(list)
        for annot in annotations["annotations"]:
            image_id_to_annotations[annot["image_id"]].append(annot)
        image_id_to_image = {{annot["file_name"]: annot for annot in annotations["images"]}}

        for filename in os.listdir(folder_dir):
            filepath = os.path.join(folder_dir, filename)
            if filename in image_id_to_image:
                image = image_id_to_image[filename]
                objects = [
                    process_annot(annot, category_id_to_category) for annot in image_id_to_annotations[image["id"]]
                ]
                with open(filepath, "rb") as f:
                    image_bytes = f.read()
                yield idx, {{
                    "image_id": image["id"],
                    "image": {{"path": filepath, "bytes": image_bytes}},
                    "width": image["width"],
                    "height": image["height"],
                    "objects": objects,
                }}
                idx += 1
'''

    with open(Path(export_dir) / f"{dataset_name}.py", "w") as f:
        f.write(detection_dataset_script_template)
