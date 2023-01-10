class ProxmoxError(Exception):
    pass


class ProxmoxConnectionError(ProxmoxError):
    pass


class ProxmoxVMNotFoundError(ProxmoxError):
    pass


class ProxmoxMissingPermissionError(ProxmoxError):
    def __init__(self, path: str, permission: str):
        super().__init__(f'Missing permission for "{path}": {permission}')
        self.path = path
        self.permission = permission
