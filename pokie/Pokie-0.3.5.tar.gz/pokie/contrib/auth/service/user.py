from typing import Optional, List

from flask_login import UserMixin
from rick.base import Di
from rick.mixin import Injectable

from pokie.contrib.auth.constants import SVC_ACL
from pokie.contrib.auth.repository.user import UserRepository
from pokie.constants import DI_SERVICES, DI_DB
from rick.util.datetime import iso8601_now
from pokie.contrib.auth.dto import UserRecord


class AuthUser(UserMixin):
    record = None  # type: UserRecord
    resources = None  # type: List
    roles = None  # type: List
    id = -1

    def __init__(self, usr: UserRecord, _di: Di):
        self.record = usr
        self.id = usr.id
        svc_acl = _di.get(DI_SERVICES).get(SVC_ACL)
        self.resources = svc_acl.list_user_resource_id(usr.id)
        self.roles = svc_acl.list_user_role_id(usr.id)

    def can_access(self, id_resource: str) -> bool:
        return id_resource in self.resources

    def has_role(self, id_role: int):
        return id_role in self.roles

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.record.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class UserService(Injectable):
    def get_by_id(self, id_user: int) -> Optional[UserRecord]:
        """
        Find user by id
        :param id_user:
        :return:
        """
        return self.user_repository.fetch_pk(id_user)

    def get_by_username(self, username: str) -> Optional[UserRecord]:
        """
        Find user by username
        :param username:
        :return:
        """
        return self.user_repository.find_by_username(username)

    def update_lastlogin(self, id_user: int):
        """
        Update user last login timestamp
        :param id_user:
        :return:
        """
        self.user_repository.update(UserRecord(id=id_user, last_login=iso8601_now()))

    def update_password(self, id_user: int, password_hash: str):
        """
        Update user password
        :param id_user:
        :param password_hash:
        :return:
        """
        self.user_repository.update(UserRecord(id=id_user, password=password_hash))

    def add_user(self, record: UserRecord) -> int:
        """
        Creates a new user
        :param record:
        :return:
        """
        return self.user_repository.insert_pk(record)

    def list_users(self, offset, limit, sort_field=None, sort_order=None) -> tuple:
        """
        Returns a tuple with a list of users

        :param offset:
        :param limit:
        :param sort_field:
        :param sort_order:
        :return: (total user count, [records])
        """
        return self.user_repository.list_users(offset, limit, sort_field, sort_order)

    def update_user(self, record: UserRecord):
        return self.user_repository.update(record)

    @property
    def user_repository(self) -> UserRepository:
        return UserRepository(self._di.get(DI_DB))
