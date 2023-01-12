import logging

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
