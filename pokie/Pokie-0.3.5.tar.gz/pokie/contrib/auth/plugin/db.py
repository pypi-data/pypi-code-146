from typing import Optional

from rick.crypto.hasher import HasherInterface
from rick.crypto.hasher.bcrypt import BcryptHasher

from pokie.constants import DI_SERVICES
from pokie.contrib.auth.service.user import AuthUser
from pokie.plugins.auth import AuthPluginInterface
from pokie.contrib.auth.constants import SVC_USER
from pokie.contrib.auth.service import UserService


class DbAuthPlugin(AuthPluginInterface):
    capabilities = [AuthPluginInterface.UPDATE_PASSWORD]

    def autenticate(self, username: str, password: str):
        record = self.svc_user.get_by_username(username)
        if record is None:
            return None

        if not record.active:
            return None

        if self.hasher.is_valid(password, record.password):
            if self.hasher.need_rehash(record.password):
                # update weak password hash
                self.svc_user.update_password(record.id, self.hasher.hash(password))

            # update lastlogin
            self.svc_user.update_lastlogin(record.id)
            return AuthUser(record, self.get_di())

    def load_id(self, id_user) -> Optional[AuthUser]:
        """
        Loads a user record by id
        :param id_user:
        :return:
        """
        record = self.svc_user.get_by_id(id_user)
        if record is None:
            return None

        if not record.active:
            return None

        return AuthUser(record, self.get_di())

    def valid_username(self, username: str) -> bool:
        """
        Checks if the given username is valid (exists and account is enabled)
        :param username:
        :return: True if username exists, false otherwise
        """
        record = self.svc_user.get_by_username(username)
        if record is None:
            return False
        return record.active

    def update_password(self, username: str, password: str) -> bool:
        """
        Updates a user password
        :param username:
        :param password:
        :return:
        """
        if len(password) == 0:
            return False
        record = self.svc_user.get_by_username(username)
        if record is None:
            return False

        self.svc_user.update_password(record.id, self.hasher.hash(password))
        return True

    def is_local(self) -> bool:
        """
        Checks if current backend is local (db/file)
        :return:
        """
        return True

    def has_capability(self, capability: int) -> bool:
        return capability in self.capabilities

    @property
    def svc_user(self) -> UserService:
        return self.get_di().get(DI_SERVICES).get(SVC_USER)

    @property
    def hasher(self) -> HasherInterface:
        return BcryptHasher()
