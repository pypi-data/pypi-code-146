import logging
import random
import shutil
import json
from typing import List
import requests
import urllib
from bs4 import BeautifulSoup
import urllib
import roboflow

from pathlib import Path

ROBOFLOW_DATASETTXT_FILENAME = "README.dataset.txt"
ROBOFLOW_ROBOFLOWTXT_FILENAME = "README.roboflow.txt"
ROBOFLOW_UNIVERSE_BASE_URL = "https://universe.roboflow.com"
ROBOFLOW_ROBOFLOWTXT_CONTENT_START = "This dataset was exported via roboflow"

LOGGER = logging.getLogger(__name__)


def parse_citation(universe_url) -> str:
    """
    Parses the citation from a Roboflow Universe URL.

    Args:
        universe_url (str): Roboflow Universe URL
            example: https://universe.roboflow.com/boxer5/123-qq5ea/dataset/6
            example: https://universe.roboflow.com/boxer5/123-qq5ea/

    Returns:
        citation (str): Citation for the dataset
    """

    url = urllib.parse.urlparse(universe_url)
    base_url = url[0] + "://" + url[1]
    if base_url != ROBOFLOW_UNIVERSE_BASE_URL:
        raise ValueError(f"Not a valid Roboflow Universe URL: {universe_url}")

    if "/dataset/" in universe_url:
        project_url = universe_url.split("/dataset")[0] + "/"
    else:
        project_url = universe_url
    request = requests.get(project_url)
    soup = BeautifulSoup(request.text, "html.parser")
    citation_div = soup.find_all("div", {"class": "section citation"})[0]
    citation = citation_div.find("code").get_text(strip=True)
    citation = citation.replace("\\", "\\\\")
    return citation


def download_roboflow_dataset(
    universe_url, api_key, location="roboflow_dataset"
) -> tuple:
    """
    Downloads a Roboflow dataset to a local directory.

    Args:
        universe_url (str): Roboflow Universe URL
            example: https://universe.roboflow.com/boxer5/123-qq5ea/dataset/6
        api_key (str): Roboflow API key
        location (str): Directory to download the dataset to

    Returns:
        project (roboflow.core.project.Project): Roboflow project object
        dataset (roboflow.core.version.Version): Roboflow dataset object
        task (str): Huggingface dataset task type. Supported types: ('image-classification', 'object-detection')
    """

    url = urllib.parse.urlparse(universe_url)
    base_url = url[0] + "://" + url[1]
    if base_url != ROBOFLOW_UNIVERSE_BASE_URL:
        raise ValueError(f"Not a valid Roboflow Universe URL: {universe_url}")
    _, workspace, project, _, version = url[2].split("/")

    rf = roboflow.Roboflow(api_key=api_key)
    project = rf.workspace(workspace).project(project)
    dataset = project.version(version)
    dataset_type = dataset.type
    if dataset_type == "classification":
        task = "image-classification"
        dataset.download("folder", location=location)
    elif dataset_type == "object-detection":
        task = "object-detection"
        dataset.download("coco", location=location)
    else:
        raise ValueError(
            "Roboflow dataset type not supported {dataset_type}. Supported types: ('classification', 'object-detection')"
        )

    return project, dataset, task


def zip_roboflow_dataset(roboflow_dir, roboflow_dataset):
    """
    Zips the Roboflow dataset splits.

    Args:
        roboflow_dir (str): Path to the Roboflow dataset directory.
        roboflow_dataset (roboflow.core.version.Version): The Roboflow dataset object.
    """
    from pathlib import Path

    LOGGER.info("Zipping Roboflow dataset splits...")

    split_names = list(roboflow_dataset.splits.keys()) + ["valid-mini"]

    for split in split_names:
        source = Path(roboflow_dir) / split
        shutil.make_archive(
            Path(roboflow_dir) / "data" / split, format="zip", root_dir=source
        )
        shutil.rmtree(source)

    LOGGER.info("Roboflow dataset splits zipped!")


def read_roboflow_info(local_data_dir: str, roboflow_universe_url: str = None):
    """
    Reads the Roboflow dataset info from the README.dataset.txt and README.roboflow.txt files.

    Args:
        local_data_dir (str): Path to the Roboflow dataset directory.
        roboflow_universe_url (str): Roboflow Universe URL of the dataset.

    Returns:
        license (str): License of the dataset.
        dataset_url (str): Roboflow Universe URL of the dataset.
        citation (str): Citation of the dataset.
        roboflow_dataset_summary (str): Summary of the dataset.
    """
    dataset_txt_path = Path(local_data_dir) / ROBOFLOW_DATASETTXT_FILENAME

    # read value of License: from README.dataset.txt
    with open(dataset_txt_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("License:"):
                license = line.split(":")[1].strip()
                break

    if roboflow_universe_url is None:
        # read dataset url from README.dataset.txt
        with open(dataset_txt_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(ROBOFLOW_UNIVERSE_BASE_URL):
                    dataset_url = line.strip()
                    break
    else:
        dataset_url = roboflow_universe_url

    # parse citation info from dataset_url
    citation = parse_citation(dataset_url)

    roboflow_txt_path = Path(local_data_dir) / ROBOFLOW_ROBOFLOWTXT_FILENAME

    # combine all lines starting from expression expression This dataset was exported via roboflow.com from README.roboflow.txt
    with open(roboflow_txt_path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith(ROBOFLOW_ROBOFLOWTXT_CONTENT_START):
                start = i
                break
        roboflow_dataset_summary = "".join(lines[start:])

    return license, dataset_url, citation, roboflow_dataset_summary


def fix_annotation_file(source_path: str):
    """
    Fixes the coco annotation json file by removing first category if its supercategory is 'none'.
    Also updates remaining category ids as 0 to N.
    Then, updates all category ids in annotations.
    Lastly, removes images and annotations that contain null bbox.

    Args:
        source_path (str): Path to the annotation file.
    """
    with open(source_path, "r") as f:
        data = json.load(f)

    # remove first category if its supercategory is 'none'
    if data["categories"][0]["supercategory"] == "none":
        data["categories"].pop(0)

        # update category ids
        for i, category in enumerate(data["categories"]):
            category["id"] = i

        # update annotation category ids
        for annotation in data["annotations"]:
            annotation["category_id"] = annotation["category_id"] - 1

    images = data["images"]
    annotations = data["annotations"]

    # remove images and annotations that contain null bbox
    new_images = []
    new_annotations = []

    invalid_image_ids = set()
    for annotation in annotations:
        if len(annotation["bbox"]) != 4:
            invalid_image_ids.add(annotation["image_id"])
        else:
            new_annotations.append(annotation)

    for image in images:
        if image["id"] not in invalid_image_ids:
            new_images.append(image)

    data["images"] = new_images
    data["annotations"] = new_annotations

    with open(source_path, "w") as f:
        json.dump(data, f)


def fix_annotations_files(local_data_dir: str):
    """
    Fixes the coco annotation json files by removing first category if its supercategory is 'none'.
    Also updates remaining category ids as 0 to N.
    Lastly, updates all category ids in annotations.

    Args:
        local_data_dir (str): Path to the Roboflow dataset directory.
    """

    for split in ["train", "valid", "test"]:
        source_path = Path(local_data_dir) / split / "_annotations.coco.json"
        if source_path.exists():
            fix_annotation_file(source_path)


def normalize_dataset_labels(local_data_dir: str) -> None:
    """
    Normalizes the dataset labels by converting them to lowercase.

    Args:
        local_data_dir (str): Path to the Roboflow dataset directory.
    """
    for split in ["train", "valid", "test"]:
        source_path = Path(local_data_dir) / split / "_annotations.coco.json"
        if source_path.exists():
            with open(source_path, "r") as f:
                data = json.load(f)
                for coco_category in data["categories"]:
                    coco_category["name"] = coco_category["name"].lower()

            with open(source_path, "w") as f:
                json.dump(data, f)


def read_dataset_labels(local_data_dir: str) -> List[str]:
    """
    Reads the dataset labels from the coco annotation json file.

    Args:
        local_data_dir (str): Path to the Roboflow dataset directory.

    Returns:
        dataset_labels (List[str]): List of dataset labels.
    """
    train_coco_json_path = Path(local_data_dir) / "train" / "_annotations.coco.json"
    with open(train_coco_json_path, "r") as f:
        data = json.load(f)
    dataset_labels = [coco_category["name"] for coco_category in data["categories"]]

    return dataset_labels


def create_mini_valid_split(local_data_dir, num_samples: int = 3):
    """
    Creates a mini valid split in coco format by copying random samples from valid split.

    Args:
        local_data_dir (str): Path to the Roboflow dataset directory.
        num_samples (int): Number of samples to copy from valid split.
    """

    valid_coco_json_path = Path(local_data_dir) / "valid" / "_annotations.coco.json"
    with open(valid_coco_json_path, "r") as f:
        data = json.load(f)

    images = data["images"]
    annotations = data["annotations"]

    # get random samples from valid split
    random.shuffle(images)

    mini_valid_images = images[:num_samples]

    # gen mini valid annotations
    mini_valid_annotations = []
    for annotation in annotations:
        if annotation["image_id"] in [image["id"] for image in mini_valid_images]:
            mini_valid_annotations.append(annotation)

    # create mini valid split
    mini_valid_split_dir = Path(local_data_dir) / "valid-mini"
    mini_valid_split_dir.mkdir(exist_ok=True)

    # copy images
    for image in mini_valid_images:
        image_path = Path(local_data_dir) / "valid" / image["file_name"]
        shutil.copy(image_path, mini_valid_split_dir)

    # copy annotations
    data["images"] = mini_valid_images
    data["annotations"] = mini_valid_annotations

    with open(mini_valid_split_dir / "_annotations.coco.json", "w") as f:
        json.dump(data, f)
