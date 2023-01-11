from typing import Iterable

from fastapi import Request


class NoPermissionError(Exception):
    pass


class UserGroups:
    ADMIN = "Администратор"
    STAFF = "staff"
    READER = "reader"


class PermissionChecker:
    def __init__(self, permissions: Iterable[str]):
        self.permissions = set(permissions)

    def __call__(self, request: Request = None):
        if not set(request.user.permissions) & set(self.permissions):
            raise NoPermissionError()


__all__ = ['NoPermissionError', 'UserGroups', 'PermissionChecker']
