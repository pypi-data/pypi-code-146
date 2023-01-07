from click import ClickException


class PVECLIError(ClickException):
    pass


class InvalidConfigError(PVECLIError):
    pass
