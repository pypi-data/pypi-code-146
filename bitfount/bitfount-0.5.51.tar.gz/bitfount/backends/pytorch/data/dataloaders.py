"""PyTorch-specific DataLoader implementations."""
import math
import random
import secrets
from typing import Any, Iterator, List, Union, cast

import torch
from torch.utils.data import DataLoader as PyTorchDataLoader

from bitfount.backends.pytorch.data.datasets import (
    _PyTorchDataset,
    _PyTorchIterableDataset,
)
from bitfount.backends.pytorch.data.utils import _convert_batch_to_tensor
from bitfount.data.dataloaders import BitfountDataLoader
from bitfount.data.types import _DataBatch, _SingleOrMulti
from bitfount.utils import delegates

#: The default buffer size for shuffling Iterable Datasets.
DEFAULT_BUFFER_SIZE: int = 1000


class _BasePyTorchBitfountDataLoader(BitfountDataLoader):
    """Base class for PyTorch-specific Bitfount DataLoaders.

    Args:
       dataset: An pytorch compatible dataset.
       batch_size: The batch size for the dataloader.
           Defaults to 1.
       shuffle: A boolean value indicating whether the values
           in the dataset should be shuffled. Defaults to False.

    Attributes:
       dataset: An pytorch compatible dataset.
       batch_size: The batch size for the dataloader.
           Defaults to 1.
       shuffle: A boolean value indicating whether the values
           in the dataset should be shuffled. Defaults to False.
    """

    def __init__(
        self,
        dataset: Union[_PyTorchDataset, _PyTorchIterableDataset],
        batch_size: int = 1,
        shuffle: bool = False,
    ):
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle


@delegates()
class PyTorchBitfountDataLoader(_BasePyTorchBitfountDataLoader):
    """Wraps a PyTorch DataLoader with bitfount functions.

    Args:
       dataset: An pytorch compatible dataset.
    """

    def __init__(self, dataset: _PyTorchDataset, **kwargs: Any):
        super().__init__(dataset=dataset, **kwargs)
        self.dataloader = self.get_pytorch_dataloader()

    def get_pytorch_dataloader(self, **kwargs: Any) -> PyTorchDataLoader:
        """Return a PyTorch DataLoader for `self.dataset`.

        Keyword arguments are passed to PyTorch's DataLoader constructor and take
        precedence over the values set in the constructor.
        """
        return PyTorchDataLoader(
            dataset=kwargs.pop("dataset", self.dataset),
            batch_size=kwargs.pop("batch_size", self.batch_size),
            shuffle=kwargs.pop("shuffle", self.shuffle),
            **kwargs,
        )

    def __len__(self) -> int:
        """Number of batches or number of elements if batch size is None."""
        return len(self.dataloader)

    def __iter__(self) -> Iterator[List[_SingleOrMulti[torch.Tensor]]]:
        """Wrapper around the default PyTorch DataLoader iterator.

        The only difference is that the elements of each batch are wrapped in a list.
        """
        for batch in self.dataloader:
            yield [x for x in batch]


@delegates()
class PyTorchIterableBitfountDataLoader(_BasePyTorchBitfountDataLoader):
    """Wraps a PyTorch DataLoader with bitfount functions.

    Args:
        dataset: An iterable dataset.
        secure_rng: A boolean value indicating whether to use a secure
            random number generator. Defaults to False.

    Attributes:
         secure_rng: A boolean value indicating whether to use a secure
            random number generator. Defaults to False.
    """

    def __init__(
        self, dataset: _PyTorchIterableDataset, secure_rng: bool = False, **kwargs: Any
    ):
        super().__init__(dataset=dataset, **kwargs)
        self.secure_rng = secure_rng

    @property
    def buffer_size(self) -> int:
        """Number of elements to buffer.

        The size of the buffer is the greater of the batch size and default buffer size
        unless the dataset is smaller than the default buffer in which case the dataset
        size is used. PyTorch already ensures that the batch size is not greater than
        the dataset size under the hood.
        """
        # Batch size is optional in the core hierarchy but in pytorch we ensure it is
        # set to 1 if not provided. Re-assuring mypy of this.
        assert self.batch_size is not None  # nosec[assert_used]
        return max(min(len(self.dataset), DEFAULT_BUFFER_SIZE), self.batch_size)

    def __len__(self) -> int:
        """Number of batches in the dataset."""
        assert self.batch_size is not None  # nosec[assert_used]
        return math.ceil(len(self.dataset) / self.batch_size)

    def __iter__(self) -> Iterator[List[_SingleOrMulti[torch.Tensor]]]:
        """Yields a batch of data when iterated.

        We use a custom iterator with different behaviour depending on whether the
        dataset should be shuffled or not. Each batch is explicitly converted to torch
        tensors prior to yielding as this is not done automatically by pytorch.
        """
        batch: _DataBatch = []

        if self.shuffle:
            # If the dataset should be shuffled, we use a reservoir sampling method
            # to sample from a buffer of elements from the dataset.
            buffer_: _DataBatch = []
            for sample in cast(_PyTorchIterableDataset, self.dataset):
                if len(batch) == self.batch_size:
                    yield _convert_batch_to_tensor(batch)
                    batch = []

                if len(buffer_) == self.buffer_size:
                    if self.secure_rng:
                        idx = secrets.randbelow(self.buffer_size)
                    else:
                        # Ignoring security warning here because RNG does not need
                        # to be cryptographically secure if it is turned off by
                        # the user.
                        idx = random.randint(0, self.buffer_size - 1)  # nosec
                    batch.append(buffer_[idx])
                    buffer_[idx] = sample
                else:
                    buffer_.append(sample)

            # This is only reached once the dataset iterator has been exhausted. The
            # remainder of the buffer is shuffled and yielded until empty.
            random.shuffle(buffer_)
            while buffer_:
                if len(batch) == self.batch_size:
                    yield _convert_batch_to_tensor(batch)
                    batch = []

                batch.append(buffer_.pop())

        else:
            # If the dataset should not be shuffled, we simply iterate over the dataset
            for sample in cast(_PyTorchIterableDataset, self.dataset):
                if len(batch) == self.batch_size:
                    yield _convert_batch_to_tensor(batch)
                    batch = []

                batch.append(sample)

        # If there are any elements left in the batch after the dataset/buffer are
        # empty, yield an incomplete batch.
        if batch:
            yield _convert_batch_to_tensor(batch)
