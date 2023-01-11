
class VelaitError(Exception):
    def __init__(self, name: str = None, description: str = None, *args):
        super(VelaitError, self).__init__(*args)
        self.name = name
        self.description = description


class AlreadyDeletedError(VelaitError):
    pass


__all__ = ['AlreadyDeletedError', 'VelaitError']
