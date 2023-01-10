import abc
from typing import Optional

from flask_login import UserMixin
from rick.mixin import Injectable


class AuthPluginInterface(Injectable, abc.ABC):
    UPDATE_PASSWORD = 1

    @abc.abstractmethod
    def autenticate(self, username: str, password: str) -> Optional[UserMixin]:
        pass

    @abc.abstractmethod
    def valid_username(self, username: str) -> bool:
        pass

    @abc.abstractmethod
    def update_password(self, username: str, password: str) -> bool:
        pass

    @abc.abstractmethod
    def is_local(self) -> bool:
        pass

    @abc.abstractmethod
    def has_capability(self, capability: int) -> bool:
        pass

    @abc.abstractmethod
    def load_id(self, id_user):
        pass
