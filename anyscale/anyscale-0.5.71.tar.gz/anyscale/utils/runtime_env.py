# pylint:disable=private-import
import hashlib
import logging
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING
from urllib.parse import urlparse
import uuid

import click

from anyscale.util import is_anyscale_workspace
from anyscale.utils.ray_utils import zip_directory  # type: ignore


if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def _upload_file_to_google_cloud_storage(file: str, bucket: str, object_name: str):
    try:
        from google.cloud import storage

    except Exception:
        raise click.ClickException(
            "Could not upload file to Google Storage. Could not import the Google Storage Python API via `from google.cloud import storage`.  Please check your installation or try running `pip install --upgrade google-cloud-storage`."
        )
    try:
        storage_client = storage.Client()
        bucket_obj = storage_client.bucket(bucket)
        blob = bucket_obj.blob(object_name)
        blob.upload_from_filename(file)
    except Exception as e:
        raise click.ClickException(
            f"Could not upload file to Google Cloud Storage. Please check your credentials and ensure that the bucket exists. {e}"
        )


def _upload_file_to_s3(file: str, bucket: str, object_key: str):
    try:
        import boto3
    except Exception:
        raise click.ClickException(
            "Could not upload file to S3: Could not import the Amazon S3 Python API via `import boto3`.  Please check your installation or try running `pip install boto3`."
        )
    try:
        s3_client = boto3.client("s3")
        s3_client.upload_file(file, bucket, object_key)
    except Exception as e:
        raise click.ClickException(
            f"Could not upload file to S3. Check your credentials and that the bucket exists. Original error: {e}"
        )


def _get_remote_storage_object_name(upload_path, upload_filename):
    # Strip leading slash, otherwise bucket will create a new directory called "/".
    object_name = os.path.join(urlparse(upload_path).path, upload_filename).lstrip("/")
    return object_name


def _upload_file_to_remote_storage(
    source_file: str, upload_path: str, upload_filename: str
):
    parsed_upload_path = urlparse(upload_path)
    service = parsed_upload_path.scheme
    bucket = parsed_upload_path.netloc
    object_name = _get_remote_storage_object_name(upload_path, upload_filename)
    if service == "s3":
        _upload_file_to_s3(source_file, bucket, object_key=object_name)
    if service == "gs":
        _upload_file_to_google_cloud_storage(
            source_file, bucket, object_name=object_name
        )

    final_uploaded_filepath = os.path.join(upload_path, upload_filename)
    try:
        from smart_open import open

        open(final_uploaded_filepath)
    except Exception as e:
        raise click.ClickException(
            f"Could not open uploaded file, maybe something went wrong while uploading: {e}."
        )

    return final_uploaded_filepath


def upload_and_rewrite_working_dir(
    runtime_env_json: Dict[str, Any],
    upload_file_to_remote_storage_fn: Callable[
        [str, str, str], str
    ] = _upload_file_to_remote_storage,
) -> Dict[str, Any]:
    """Upload a local working_dir and rewrite the working_dir field with the destination remote URI.

    After uploading, deletes the "upload_path" field because it is no longer used and is not a valid
    OSS runtime env field.
    """
    if "working_dir" not in runtime_env_json:
        return runtime_env_json

    working_dir = runtime_env_json["working_dir"]
    parsed = urlparse(working_dir)
    if parsed.scheme:
        # The working dir is a remote URI already
        return runtime_env_json

    upload_path = runtime_env_json["upload_path"]
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip_file_path = os.path.join(
            temp_dir, "anyscale_generated_working_dir.zip"
        )
        zip_directory(
            working_dir,
            excludes=runtime_env_json.get("excludes", []),
            output_path=temp_zip_file_path,
            # Ray requires remote Zip URIs to consist of a single top-level directory when unzipped.
            include_parent_dir=True,
        )

        hash_val = hashlib.md5(Path(temp_zip_file_path).read_bytes()).hexdigest()
        uploaded_zip_file_name = f"_anyscale_pkg_{hash_val}.zip"
        final_uploaded_filepath = upload_file_to_remote_storage_fn(
            temp_zip_file_path, upload_path, uploaded_zip_file_name,
        )

    final_runtime_env = runtime_env_json.copy()
    final_runtime_env["working_dir"] = final_uploaded_filepath
    del final_runtime_env["upload_path"]
    return final_runtime_env


def override_runtime_env_for_local_working_dir(
    runtime_env: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    If runtime_env contains a "upload_path" field, we need to upload it first
    before backing it up inside EFS (if in workspaces).
    """
    if runtime_env:
        runtime_env = upload_and_rewrite_working_dir(runtime_env)

    if is_anyscale_workspace():
        import anyscale

        runtime_env = anyscale.snapshot_util.env_hook(runtime_env)
        # Snapshot the working directory to EFS so the job we submit can read it from there
        parsed_working_dir = urlparse(runtime_env["working_dir"])
        # We add prefix "file://" only if the working dir is local dir
        if not parsed_working_dir.scheme:
            runtime_env["working_dir"] = "file://" + runtime_env["working_dir"]
        fake_job_id = uuid.uuid4().hex
        runtime_env = anyscale.snapshot_util.checkpoint_job(fake_job_id, runtime_env)
        runtime_env["working_dir"] = "file://" + runtime_env["working_dir"]

    return runtime_env
