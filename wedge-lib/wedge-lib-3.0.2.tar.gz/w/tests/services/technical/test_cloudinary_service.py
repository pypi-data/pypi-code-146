from io import BytesIO

import pytest
from cloudinary import CloudinaryImage

from w.services.technical.cloudinary_service import CloudinaryService
from w.tests.helpers import service_test_helper
from w.tests.helpers.cloudinary_test_helper import (
    mock_cloudinary_upload,
    mock_cloudinary_delete,
)
from w.tests.mixins.testcase_mixin import TestCaseMixin
from w.tests.helpers.cloudinary_test_helper import _get_dataset


class TestCloudinaryService(TestCaseMixin):
    service = CloudinaryService

    @classmethod
    def setup_class(cls):
        cls.service.init(cloud_name="TEST", api_key="TEST", api_secret="TEST")

    @classmethod
    def teardown_class(cls):
        cls.service.clear()

    """
    upload
    """

    def test_upload_with_success_return_none(self):
        with mock_cloudinary_upload() as mock:
            self.service.upload("random/file/path")

        assert mock.call_count == 1

    """
    delete
    """

    def test_delete_with_success_return_none(self):
        with mock_cloudinary_delete() as mock:
            self.service.delete("some_public_id1", "some_public_id2")

        assert mock.call_count == 1

    def test_delete_with_no_public_id_return_none(self):
        with mock_cloudinary_delete() as mock:
            self.service.delete()

        assert mock.call_count == 0

    """
    upload_temporary_file
    """

    def test_upload_temporary_file_with_success_return_cloudinary_image(self):
        some_file_bytes = BytesIO()
        some_folder = "cloudinary_folder"
        with mock_cloudinary_upload() as upload_mock:
            with mock_cloudinary_delete() as delete_mock:
                with self.service.upload_temporary_file(
                    some_file_bytes,
                    folder=some_folder,
                ) as image:
                    assert isinstance(image, CloudinaryImage)
                    assert some_folder in str(image)

        assert upload_mock.call_count == delete_mock.call_count == 1

    """
    search
    """

    def test_search_with_service_not_initialized_raise_runtime_error(self):
        """Ensure method raises RuntimeError if service is not initialized"""
        CloudinaryService.clear()
        match = "Service CloudinaryService must be initialized first"
        with pytest.raises(RuntimeError, match=match):
            CloudinaryService.search("seat")

    def test_search_with_success_return_response(self):
        """Ensure method succeeds"""
        mock_response = _get_dataset("cloudinary/search_make_with_success.json")
        with service_test_helper.mock_service(
            CloudinaryService, "search", mock_response
        ):
            response = CloudinaryService.search("seat")
        self.assert_equals_resultset(response)
