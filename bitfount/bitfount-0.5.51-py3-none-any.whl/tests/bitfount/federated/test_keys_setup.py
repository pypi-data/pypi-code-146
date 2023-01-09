"""Tests for encryption key setup functions."""
from pathlib import Path

from _pytest.logging import LogCaptureFixture
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.federated.encryption import _RSAEncryption
from bitfount.federated.exceptions import RSAKeyError
from bitfount.federated.keys_setup import (
    _MODELLER_PRIVATE_KEY_FILE,
    _MODELLER_PUBLIC_KEY_FILE,
    _POD_PRIVATE_KEY_FILE,
    _POD_PUBLIC_KEY_FILE,
    RSAKeyPair,
    _generate_key_pair,
    _get_key_pair,
    _get_modeller_keys,
    _get_pod_keys,
    _load_key_pair,
)
from tests.utils.helper import get_warning_logs, unit_test


@unit_test
class TestKeysSetups:
    """Tests for keys_setup.py functions."""

    @fixture
    def tmp_key_directory(self, tmp_path: Path) -> Path:
        """Temporary per-function directory for storing keys."""
        tmp_key_directory = tmp_path / "key_storage"
        tmp_key_directory.mkdir(parents=True, exist_ok=True)
        return tmp_key_directory

    @fixture
    def private_key_path(self, tmp_key_directory: Path) -> Path:
        """Temporary per-function file for storing private key."""
        return tmp_key_directory / "key"

    @fixture
    def public_key_path(self, tmp_key_directory: Path) -> Path:
        """Temporary per-function file for storing public key."""
        return tmp_key_directory / "key.pub"

    @fixture(scope="class")
    def key_pair(self) -> RSAKeyPair:
        """A pair of RSA keys to persist for all tests."""
        private_key, public_key = _RSAEncryption.generate_key_pair()
        return RSAKeyPair(public_key, private_key)

    @fixture(scope="class")
    def private_key(self, key_pair: RSAKeyPair) -> RSAPrivateKey:
        """Persistent RSA private key."""
        return key_pair.private

    @fixture(scope="class")
    def public_key(self, key_pair: RSAKeyPair) -> RSAPublicKey:
        """Persistent RSA public key."""
        return key_pair.public

    @fixture
    def pre_store_keys(
        self,
        private_key: RSAPrivateKey,
        private_key_path: Path,
        public_key: RSAPublicKey,
        public_key_path: Path,
    ) -> None:
        """Write keys to files before tests."""
        private_key_path.write_bytes(
            _RSAEncryption.serialize_private_key(private_key, form="SSH")
        )
        public_key_path.write_bytes(
            _RSAEncryption.serialize_public_key(public_key, form="SSH")
        )

    def test__generate_key_pair(
        self, private_key_path: Path, public_key_path: Path
    ) -> None:
        """Tests _generate_key_pair creates and saves keys."""
        key_pair = _generate_key_pair(private_key_path, public_key_path)

        # Check keys generated
        assert isinstance(key_pair.private, RSAPrivateKey)
        assert isinstance(key_pair.public, RSAPublicKey)

        # Check keys serialized
        assert private_key_path.exists()
        assert public_key_path.exists()

        # Check serialized keys match returned keys
        assert _RSAEncryption.private_keys_equal(
            key_pair.private, _RSAEncryption.load_private_key(private_key_path)
        )
        assert _RSAEncryption.public_keys_equal(
            key_pair.public, _RSAEncryption.load_public_key(public_key_path)
        )

    def test__load_key_pair(
        self,
        pre_store_keys: None,
        private_key: RSAPrivateKey,
        private_key_path: Path,
        public_key: RSAPublicKey,
        public_key_path: Path,
    ) -> None:
        """Tests _load_key_pair loads keys from file."""
        loaded_keys = _load_key_pair(private_key_path, public_key_path)

        # Check loaded keys match unserialized keys
        assert _RSAEncryption.private_keys_equal(loaded_keys.private, private_key)
        assert _RSAEncryption.public_keys_equal(loaded_keys.public, public_key)

    def test__load_key_pair_handles_public_key_mismatch(
        self,
        pre_store_keys: None,
        private_key: RSAPrivateKey,
        private_key_path: Path,
        public_key_path: Path,
    ) -> None:
        """Tests _load_key_pair raises exception if public-private key mismatch."""
        # Store replacement public key at key path
        _, replacement_public_key = _RSAEncryption.generate_key_pair()
        public_key_path.write_bytes(
            _RSAEncryption.serialize_public_key(replacement_public_key, form="SSH")
        )

        with pytest.raises(RSAKeyError):
            _load_key_pair(private_key_path, public_key_path)

    @pytest.mark.parametrize(
        "private_key_present", [True, False], ids=lambda x: f"private_key_present={x}"
    )
    @pytest.mark.parametrize(
        "public_key_present", [True, False], ids=lambda x: f"public_key_present={x}"
    )
    def test__get_key_pair(
        self,
        caplog: LogCaptureFixture,
        key_pair: RSAKeyPair,
        mocker: MockerFixture,
        private_key_path: Path,
        private_key_present: bool,
        public_key_path: Path,
        public_key_present: bool,
    ) -> None:
        """Test various paths of _get_key_pair."""
        # Mock out loading/generating
        mock__load_key_pair = mocker.patch(
            "bitfount.federated.keys_setup._load_key_pair",
            autospec=True,
            return_value=key_pair,
        )
        mock__generate_key_pair = mocker.patch(
            "bitfount.federated.keys_setup._generate_key_pair", autospec=True
        )
        mock_rsa_priv_key_loading = mocker.patch.object(
            _RSAEncryption,
            "load_private_key",
            autospec=True,
            return_value=key_pair.private,
        )

        # "Create" files if requested
        if private_key_present:
            private_key_path.touch()
        if public_key_present:
            public_key_path.touch()

        if public_key_present and not private_key_present:
            with pytest.raises(
                RSAKeyError,
                match="Could not find private key corresponding to public key",
            ):
                _get_key_pair(private_key_path, public_key_path)
        else:
            returned_key_pair = _get_key_pair(private_key_path, public_key_path)

            # If both key files present, files should be loaded
            if public_key_present and private_key_present:
                mock__load_key_pair.assert_called_once_with(
                    private_key_path, public_key_path
                )
                assert returned_key_pair == key_pair

            # If only private key is present, public key should be extracted and saved
            elif private_key_present:
                mock_rsa_priv_key_loading.assert_called_once_with(private_key_path)
                # Check saved key
                assert public_key_path.exists()
                assert _RSAEncryption.public_keys_equal(
                    key_pair.public, _RSAEncryption.load_public_key(public_key_path)
                )
                # Check returned key
                assert _RSAEncryption.public_keys_equal(
                    returned_key_pair.public, key_pair.public
                )
                assert _RSAEncryption.private_keys_equal(
                    returned_key_pair.private, key_pair.private
                )
                # Check situation was logged
                assert (
                    "Extracting public key from private key and saving"
                    in get_warning_logs(caplog)
                )

            # Otherwise, they should be generated
            else:
                mock__generate_key_pair.assert_called_once_with(
                    private_key_path, public_key_path
                )
                assert returned_key_pair == mock__generate_key_pair.return_value

    def test__get_pod_keys(
        self, key_pair: RSAKeyPair, mocker: MockerFixture, tmp_key_directory: Path
    ) -> None:
        """Test getting of pod keys."""
        mock__get_key_pair = mocker.patch(
            "bitfount.federated.keys_setup._get_key_pair",
            autospec=True,
            return_value=key_pair,
        )

        returned_key_pair = _get_pod_keys(tmp_key_directory)

        assert returned_key_pair == key_pair
        mock__get_key_pair.assert_called_once_with(
            tmp_key_directory / _POD_PRIVATE_KEY_FILE,
            tmp_key_directory / _POD_PUBLIC_KEY_FILE,
        )

    def test__get_modeller_keys(
        self, key_pair: RSAKeyPair, mocker: MockerFixture, tmp_key_directory: Path
    ) -> None:
        """Test getting of modeller keys."""
        mock__get_key_pair = mocker.patch(
            "bitfount.federated.keys_setup._get_key_pair",
            autospec=True,
            return_value=key_pair,
        )

        returned_key_pair = _get_modeller_keys(tmp_key_directory)

        assert returned_key_pair == key_pair
        mock__get_key_pair.assert_called_once_with(
            tmp_key_directory / _MODELLER_PRIVATE_KEY_FILE,
            tmp_key_directory / _MODELLER_PUBLIC_KEY_FILE,
        )
