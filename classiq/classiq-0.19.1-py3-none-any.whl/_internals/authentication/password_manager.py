import abc
import json
import logging
import os
import pathlib
import platform
import stat
from typing import Dict, Optional

import keyring
from keyring.backends import fail

_logger = logging.getLogger(__name__)


class PasswordManager(abc.ABC):
    _SERVICE_NAME: str = "classiqTokenService"
    _ACCESS_TOKEN_KEY: str = "classiqTokenAccount"
    _REFRESH_TOKEN_KEY: str = "classiqRefershTokenAccount"

    @property
    def access_token(self) -> Optional[str]:
        return self._get(key=self._ACCESS_TOKEN_KEY)

    @access_token.setter
    def access_token(self, access_token: Optional[str]) -> None:
        self._set(key=self._ACCESS_TOKEN_KEY, value=access_token)

    @property
    def refresh_token(self) -> Optional[str]:
        return self._get(key=self._REFRESH_TOKEN_KEY)

    @refresh_token.setter
    def refresh_token(self, refresh_token: Optional[str]) -> None:
        self._set(key=self._REFRESH_TOKEN_KEY, value=refresh_token)

    @abc.abstractmethod
    def _get(self, key: str) -> Optional[str]:
        pass

    @abc.abstractmethod
    def _set(self, key: str, value: Optional[str]) -> None:
        pass

    @abc.abstractmethod
    def _clear(self, key: str) -> None:
        pass

    @abc.abstractmethod
    def is_supported(self) -> bool:
        pass


class KeyringPasswordManager(PasswordManager):
    def _get(self, key: str) -> Optional[str]:
        return keyring.get_password(service_name=self._SERVICE_NAME, username=key)

    def _set(self, key: str, value: Optional[str]) -> None:

        if value is None:
            self._clear(key)
            return
        keyring.set_password(
            service_name=self._SERVICE_NAME,
            username=key,
            password=value,
        )

    def _clear(self, key: str) -> None:

        keyring.delete_password(
            service_name=self._SERVICE_NAME,
            username=key,
        )

    def is_supported(self) -> bool:
        return not isinstance(keyring.get_keyring(), fail.Keyring)


class DummyPasswordManager(PasswordManager):
    def _get(self, key: str) -> Optional[str]:
        return None

    def _set(self, key: str, value: Optional[str]) -> None:
        return

    def _clear(self, key: str) -> None:
        return

    def is_supported(self) -> bool:
        return True


class FilePasswordManager(PasswordManager):
    _CLASSIQ_CREDENTIALS_FILE_PATH: str = "{}/.classiq-credentials".format(
        os.getenv("HOME")
    )

    def __init__(self) -> None:
        super().__init__()
        self.credentials_file = pathlib.Path(self._CLASSIQ_CREDENTIALS_FILE_PATH)

    def _update_file(self, token_dict: Dict):
        self.credentials_file.touch()
        self.credentials_file.chmod(stat.S_IRUSR | stat.S_IWUSR)
        self.credentials_file.write_text(json.dumps(token_dict))

    def _get_token_dict(self) -> Dict:
        if self.credentials_file.exists():
            return json.loads(self.credentials_file.read_text())
        return {}

    def _get(self, key: str) -> Optional[str]:
        token_dict = self._get_token_dict()
        if key in token_dict:
            return token_dict[key]
        return None

    def _set(self, key: str, value: Optional[str]) -> None:
        token_dict = self._get_token_dict()
        token_dict[key] = value
        self._update_file(token_dict)

    def _clear(self, key: str) -> None:
        token_dict = self._get_token_dict()
        if key in token_dict:
            token_dict.pop(key)
            self._update_file(token_dict)

    def is_supported(self) -> bool:
        return "windows" not in platform.platform().lower()
