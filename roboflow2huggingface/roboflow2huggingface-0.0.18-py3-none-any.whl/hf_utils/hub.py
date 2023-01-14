import logging
from pathlib import Path

from PIL import Image
from roboflow2huggingface.other_utils import add_text_to_image

LOGGER = logging.getLogger(__name__)


def upload_dataset_to_hfhub(dataset_dir, repo_id, token, private=False):
    """
    Uploads a dataset to the Hugging Face Hub.

    Args:
        dataset_dir (str): Path to the dataset directory.
        repo_id (str): The name of the repository to upload to.
        token (str): The token to use to authenticate to the Hugging Face Hub.
        private (bool, optional): Whether the repository should be private. Defaults to False.
    """
    from huggingface_hub import upload_folder, create_repo

    LOGGER.info(f"Uploading dataset to hf.co/{repo_id}...")

    create_repo(
        repo_id=repo_id,
        token=token,
        private=private,
        exist_ok=True,
        repo_type="dataset",
    )
    upload_folder(
        folder_path=dataset_dir,
        repo_id=repo_id,
        token=token,
        repo_type="dataset",
        commit_message="dataset uploaded by roboflow2huggingface package",
    )

    LOGGER.info(f"Dataset uploaded to hf.co/{repo_id}!")


def generate_thumbnail(image_path, repo_id) -> Path:
    """
    Generate thumbnail for the model card

    USERNAME/garbage-object-detection > Garbage Object Detection
    """
    thumbnail_text = repo_id.split("/")[-1]
    texts = thumbnail_text.split("-")
    for ind, text in enumerate(texts):
        if "yolo" not in text.lower():
            texts[ind] = text.title()

    thumbnail_text = " ".join(texts)

    image = add_text_to_image(
        text=thumbnail_text,
        pil_image=Image.open(image_path),
        brightness=0.60,
        text_font=50,
        crop_margin=150,
    )

    folder_path = Path(image_path).parent
    thumbnail_path = folder_path / "thumbnail.jpg"
    image.save(str(thumbnail_path), quality=100)

    return thumbnail_path
