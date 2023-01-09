import os
import unittest

from pycollimator import Api
from pycollimator.error import CollimatorApiError
from tests import setup_auth_token, ENV


class TestUploadFile(unittest.TestCase):
    def setUp(self) -> None:
        self.token = setup_auth_token()
        self.fixtures_root = os.environ.get("FIXTURES_ROOT", "")
        return super().setUp()

    def test_upload_file(self):
        response = Api.upload_file(f"{self.fixtures_root}tests/fixtures/stop.png", overwrite=True)

        self.assertEquals("image/png", response["summary"]["content_type"])
        self.assertEquals("stop.png", response["summary"]["name"])
        self.assertEquals(356793, response["summary"]["size_in_bytes"])
        self.assertEquals("upload_completed", response["summary"]["status"])

    def test_upload_file_fails(self):
        if ENV == "local":
            return

        with self.assertRaises(CollimatorApiError) as context:
            Api.upload_file(f"{self.fixtures_root}tests/fixtures/stop.png", overwrite=False)

        self.assertTrue("File with this name already exists: stop.png" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
