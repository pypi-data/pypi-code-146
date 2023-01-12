import os
from pathlib import Path
import yaml


def make_dataset_yolov5_trainable(roboflow_dataset_dir: str) -> str:
    """
    Makes a COCO formatted and zipped Roboflow dataset trainable with YOLOv5.

    Args:
        roboflow_dataset_dir (str): The directory of the Roboflow dataset.

    Returns:
        data.yaml path (str)
    """
    train_zip = Path(roboflow_dataset_dir) / "data" / "train.zip"
    val_zip = Path(roboflow_dataset_dir) / "data" / "valid.zip"

    train_dir = Path(roboflow_dataset_dir) / "data" / "train"
    val_dir = Path(roboflow_dataset_dir) / "data" / "valid"

    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)

    import zipfile

    with zipfile.ZipFile(train_zip, "r") as zip_ref:
        zip_ref.extractall(train_dir)

    with zipfile.ZipFile(val_zip, "r") as zip_ref:
        zip_ref.extractall(val_dir)

    train_zip.unlink()
    val_zip.unlink()

    # create data.yaml
    datayaml_path = Path(os.path.abspath(roboflow_dataset_dir)) / "data.yaml"
    train_json_path = Path(train_dir) / "_annotations.coco.json"
    val_json_path = Path(val_dir) / "_annotations.coco.json"

    # create yolov5 data yaml (use replace for windows paths)
    data = {
        "train_image_dir": os.path.abspath(train_dir).replace("\\", "/"),
        "val_image_dir": os.path.abspath(val_dir).replace("\\", "/"),
        "train_json_path": os.path.abspath(train_json_path).replace("\\", "/"),
        "val_json_path": os.path.abspath(val_json_path).replace("\\", "/"),
    }
    with open(datayaml_path, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    return str(datayaml_path).replace("\\", "/")
