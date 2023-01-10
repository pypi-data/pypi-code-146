class InvalidUuidException(Exception):
    # message, uuid
    def __init__(self, uuid: str):
        super().__init__()
        self.uuid = uuid

    def __str__(self):
        return f"Invalid UUID Exception: the given value is not a valid uuid. {self.uuid}"
