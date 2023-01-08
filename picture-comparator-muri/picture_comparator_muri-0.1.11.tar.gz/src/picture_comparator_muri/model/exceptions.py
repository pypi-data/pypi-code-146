
class ImageTooBigException(Exception):
    def __init__(self, path: str):
        self.path = path
        super().__init__(f'"{path}": image is too big and cannot be loaded.')
