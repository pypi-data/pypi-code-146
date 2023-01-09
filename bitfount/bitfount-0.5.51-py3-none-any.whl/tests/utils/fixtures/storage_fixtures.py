"""Fixtures related to uploading/downloading from S3."""
from datetime import datetime

from pytest import fixture

from bitfount.types import _S3PresignedPOSTFields, _S3PresignedPOSTURL, _S3PresignedURL


@fixture
def s3_netloc_subdomain() -> str:
    """A mock subdomain of the style of our message service S3 buckets."""
    time_segment = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"-message-service-external{time_segment}.s3.eu-west-2.amazonaws.com"


@fixture
def s3_upload_url(s3_netloc_subdomain: str) -> _S3PresignedPOSTURL:
    """A faked upload URL for S3 POST."""
    return _S3PresignedPOSTURL(
        f"https://an-s3-upload-url{s3_netloc_subdomain}.s3.com/some-resource/path?hello=upload_world"  # noqa: B950  # better to keep the URL whole
    )


@fixture
def s3_upload_fields() -> _S3PresignedPOSTFields:
    """Faked upload fields for S3 POST."""
    return _S3PresignedPOSTFields({"some": "upload", "fields": "to_test_with"})


@fixture
def s3_download_url(s3_netloc_subdomain: str) -> _S3PresignedURL:
    """Fake download URL for S3 GET."""
    return _S3PresignedURL(
        f"https://an-s3-download-url{s3_netloc_subdomain}.s3.com/some-resource/path?hello=download_world"  # noqa: B950  # better to keep the URL whole
    )
