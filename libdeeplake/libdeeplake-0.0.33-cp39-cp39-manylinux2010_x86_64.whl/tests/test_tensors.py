from indra import api
from .constants import (
    MNIST_DS_NAME,
)

def test_indra():
    ds = api.dataset(MNIST_DS_NAME)
    tensors = ds.tensors
    assert isinstance(tensors, list)
