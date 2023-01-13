import os
import pathlib
import tempfile
import zipfile
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import IO, Optional
from uuid import uuid4

from PIL import Image

from baseten.common.api import (create_training_dataset,
                                upload_user_dataset_file, upload_user_file)

DEFAULT_FILE_PATH = "png"


def upload_to_s3(io_stream: IO, file_name: str) -> str:
    """
    Uploads any stream to S3.

    Args:
        io_stream (IO): Any IO byte stream. This could be a bytes buffer, or
        an open binary file.
        file_name (str): The file_name to use when saving the file to S3

    Returns:
        str: A URL to fetch the uploaded S3 object.
    """
    upload_user_file(io_stream, file_name)
    return upload_user_file(io_stream, file_name)


def upload_pil_to_s3(image: Image.Image, file_name: Optional[str] = None) -> str:
    """
    Uploads a PIL image object to S3.

    Args:
        image (PIL.Image): A PIL image object.
        file_name (Optional[str]): The file_name to use when saving the file to S3.
            Must have an image file extension (.jpg, .png, etc.). Can be None.

    Returns:
        str: A URL to fetch the uploaded S3 object.
    """

    # If no file_name is passed, generate a random file path
    if file_name is None:
        file_name = f"{str(uuid4())}.{DEFAULT_FILE_PATH}"

    # Get the file extension from the passed in file name.
    image_format = pathlib.Path(file_name).suffix.strip(".")

    byte_buffer = BytesIO()
    image.save(byte_buffer, format=image_format)

    return upload_to_s3(byte_buffer, file_name)


class TrainingType(Enum):
    DREAMBOOTH = "DREAMBOOTH"
    CLASSIC_STABLE_DIFFUSION = "CLASSIC_STABLE_DIFFUSION"


def upload_dataset(name: str, dir: Path, training_type: TrainingType) -> str:
    # TODO (sid): Validate the dataset

    zipfile_name = f"{name}.zip"
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_file = zipfile.ZipFile(os.path.join(tmpdir, zipfile_name), 'w')

        for file in dir.glob("**/*"):
            zip_file.write(file)
        zip_file.close()
        upload_params = upload_user_dataset_file(os.path.join(tmpdir, zipfile_name), zipfile_name)

        s3_key = upload_params["form_fields"]["key"]
        return create_training_dataset(name, s3_key, training_type.value)
