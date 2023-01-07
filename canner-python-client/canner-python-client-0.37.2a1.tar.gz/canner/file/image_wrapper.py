import numpy as np
from io import BytesIO
from PIL import Image

__all__ = ["ImageWrapper"]


class ImageWrapper(object):
    def __init__(self, content):
        self.content = content

    def to_pil(self):
        return Image.open(BytesIO(self.content))

    def to_np(self, *args, **kwargs):
        return np.asarray(self.to_pil())