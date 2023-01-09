"""Tests datafactory.py."""
from unittest.mock import create_autospec

from bitfount.backends.pytorch.data.datafactory import _PyTorchDataFactory
from bitfount.backends.pytorch.data.dataloaders import PyTorchIterableBitfountDataLoader
from bitfount.backends.pytorch.data.datasets import _PyTorchIterableDataset
from tests.utils.helper import backend_test, unit_test


@backend_test
@unit_test
def test_datafactory_iterable_dataset() -> None:
    """Tests create_dataloader returns iterable loader."""
    datafactory = _PyTorchDataFactory()
    dataset = create_autospec(_PyTorchIterableDataset)
    dataloader = datafactory.create_dataloader(dataset)
    assert isinstance(dataloader, PyTorchIterableBitfountDataLoader)
