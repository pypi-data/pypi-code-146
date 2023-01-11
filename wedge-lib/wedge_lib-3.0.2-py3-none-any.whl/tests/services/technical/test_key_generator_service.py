from unittest.mock import patch

from w.services.technical.key_generator_service import KeyGeneratorService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestKeyGeneratorService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.left = "left"
        cls.right = "right"
        cls.expected_prefix = "IGmACdiN"
        cls.expected_secret = "LHqgrtu7Q9CnUDNrkCZec8a0A5p57ph5"

    @staticmethod
    def _get_generate_secret_key_mock_config():
        return {
            "service": KeyGeneratorService,
            "method_name": "generate_secret_key",
            "return_value": "IGmACdiN.LHqgrtu7Q9CnUDNrkCZec8a0A5p57ph5",
        }

    """
    _concatenate
    """

    def test__concatenate_with_success_return_str(self):
        """Ensure method returns the concatenation of the two values passed
        in parameter
        """
        assert (
            KeyGeneratorService._concatenate(self.left, self.right)
            == f"{self.left}.{self.right}"
        )

    """
    generate_secret_key
    """

    def test_generate_key_with_success_return_str(self):
        """Ensure method returns random key"""
        with patch(
            "w.services.technical.key_generator_service.get_random_string",
            side_effect=[self.expected_prefix, self.expected_secret],
        ):
            assert (
                KeyGeneratorService.generate_key()
                == f"{self.expected_prefix}.{self.expected_secret}"
            )
