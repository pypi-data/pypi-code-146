from assimilator.core.database.exceptions import NotFoundError


class AlreadyDeletedError(NotFoundError):
    pass


class InvalidSearchData(Exception):
    def __init__(self, name: str, description: str):
        self.errors = [{"name": name, "description": description}]


__all__ = ['AlreadyDeletedError', 'InvalidSearchData']
