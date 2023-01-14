from roboflow2huggingface.hf_utils.instance_segmentation_dataset import (
    export_hf_instance_segmentation_dataset_script,
)
from roboflow2huggingface.hf_utils.object_detection_dataset import (
    export_hf_object_detection_dataset_script,
)
from roboflow2huggingface.hf_utils.image_classification_dataset import (
    export_hf_image_classification_dataset_script,
)


def export_hf_dataset_script(
    hf_dataset_id,
    dataset_labels,
    roboflow_dataset,
    export_dir,
    roboflow_universe_url,
    task="object-detection",
):
    if task == "object-detection":
        export_hf_object_detection_dataset_script(
            hf_dataset_id=hf_dataset_id,
            dataset_labels=dataset_labels,
            roboflow_dataset=roboflow_dataset,
            export_dir=export_dir,
            roboflow_universe_url=roboflow_universe_url,
        )
    elif task == "instance-segmentation":
        export_hf_instance_segmentation_dataset_script(
            hf_dataset_id=hf_dataset_id,
            dataset_labels=dataset_labels,
            roboflow_dataset=roboflow_dataset,
            export_dir=export_dir,
            roboflow_universe_url=roboflow_universe_url,
        )
    elif task == "image-classification":
        export_hf_image_classification_dataset_script(
            hf_dataset_id=hf_dataset_id,
            dataset_labels=dataset_labels,
            roboflow_dataset=roboflow_dataset,
            export_dir=export_dir,
            roboflow_universe_url=roboflow_universe_url,
        )
    else:
        raise ValueError(f"Unknown task: {task}")
