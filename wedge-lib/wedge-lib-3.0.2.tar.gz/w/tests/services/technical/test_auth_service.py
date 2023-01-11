from unittest.mock import patch, Mock

from w.services.technical.auth_service import AuthService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestAuthService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.text = "mon text à signer"
        cls.signed_text = (
            "mon text à signer:HkmUAVUQI6KNcQjbQX1ZZGfJWMlp5NCRNqOXwwQTaUs"
        )
        cls.salt = "mon sel"
        cls.hash = "HkmUAVUQI6KNcQjbQX1ZZGfJWMlp5NCRNqOXwwQTaUs"

    """
    generate_random_pwd
    """

    def test_generate_random_pwd_with_success_return_str(self):
        """Ensure method return random password"""
        with patch("uuid.uuid4") as uuid4:
            uuid4.return_value = Mock(hex="uuid-token")
            assert AuthService.generate_random_pwd() == "uuid-token"

    """
    get_crypto_hash
    """

    def test_get_crypto_hash_with_success_return_str(self):
        """Ensure method succeeds"""
        actual = AuthService.get_crypto_hash(self.text, salt=self.salt)
        assert actual == self.hash

    """
    is_crypto_hash_valid
    """

    def test_is_crypto_hash_valid_with_wrong_hash_return_false(self):
        """Ensure method raise return false with wrong hash"""
        actual = AuthService.is_crypto_hash_valid(
            self.text, "mauvaishash", salt=self.salt
        )
        assert actual is False

    def test_is_crypto_hash_valid_with_wrong_salt_return_false(self):
        """Ensure method raise return false with wrong salt"""
        actual = AuthService.is_crypto_hash_valid(
            self.text, self.hash, salt="mauvais sel"
        )
        assert actual is False

    def test_is_crypto_hash_valid_with_success_return_true(self):
        """Ensure method succeed"""
        actual = AuthService.is_crypto_hash_valid(self.text, self.hash, self.salt)
        assert actual is True
