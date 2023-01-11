import os

from w.services.technical.file_service import FileService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestFileService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.encryption_key = "en2yvL6HrcWM8u8JZFq9vWGQ7Gp_eOBqbvkbz0z-7tQ="

    """
    save_encrypted_file
    """

    def test_save_encrypted_file(self):
        self.clean_sandbox()
        filename = self.get_sandbox_dir("writing_success.txt")
        secret = b"Hello World!"
        FileService.save_encrypted_file(filename, secret, self.encryption_key)
        assert os.path.exists(filename)
        with open(filename):
            assert (
                FileService.load_encrypted_file(filename, self.encryption_key) == secret
            )
