class FilesSynchronizationError(Exception):
    def __init__(self, message="Something is going wrong"):
        self.message = message
        super().__init__(self.message)
