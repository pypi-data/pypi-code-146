import io
import numpy
import PIL.Image
import torch


class Utf8:
    @staticmethod
    def encode(x):
        return bytes(x)

    @staticmethod
    def decode(x):
        return x.decode('utf-8')


class PILImage:
    @staticmethod
    def encode(x):
        buffer = io.BytesIO()
        x.save(buffer, format='png')
        return buffer.getvalue()

    @staticmethod
    def decode(bytes_):
        return PIL.Image.open(io.BytesIO(bytes_))


class FloatTensor:
    @staticmethod
    def encode(x):
        x = x.numpy()
        assert x.dtype == numpy.float32
        return memoryview(x).tobytes()

    @staticmethod
    def decode(bytes_):
        array = numpy.frombuffer(bytes_, dtype=numpy.float32)
        return torch.from_numpy(array).type(torch.float)
