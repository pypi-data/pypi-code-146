from abc import ABC, abstractmethod
from typing import Callable, List, Literal, Optional, Sequence, Tuple, TypeVar, Union

import numpy as np
from torch import Tensor, tensor
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import Lambda

from classiq.exceptions import ClassiqIndexError, ClassiqValueError

Transform = Callable[[Tensor], Tensor]
T = TypeVar("T")
DataAndLabel = Tuple[List[int], List[int]]


#
# Utils for `DatasetNot`
#
def all_bits_to_one(n: int) -> int:
    """
    Return an integer of length `n` bits, where all the bits are `1`
    """
    return (2**n) - 1


def all_bits_to_zero(n: int) -> int:
    """
    Return an integer of length `n` bits, where all the bits are `0`
    """
    return 0


#
# Transformers for `DatasetNot`
#
def state_to_weights(pure_state: Tensor) -> Tensor:
    """
    input: a `Tensor` of binary numbers (0 or 1)
    output: the required angle of rotation for `Rx`
    (in other words, |0> translates to no rotation, and |1> translates to `pi`)
    """
    # |0> requires a rotation by 0
    # |1> requires a rotation by pi
    return pure_state.bool().int() * np.pi


def state_to_label(pure_state: Tensor) -> Tensor:
    """
    input: a `Tensor` of binary numbers (0 or 1) - the return value of a measurement
    output: probability (from that measurement) of measuring 0
    (in other words,
        |0> translates to 100% chance for measuring |0> ==> return value is 1.0
        |1> translates to   0% chance for measuring |0> ==> return value is 0.0
    )
    """
    # |0> means 100% chance to get |0> ==> 100% == 1.0
    # |1> means   0% chance to get |0> ==>   0% == 0.0

    # This line basically does `1 - bool(pure_state)`
    return 1 - pure_state.bool().int()


class MyDataset(Dataset, ABC):
    def __init__(
        self,
        n: int = 2,
        transform: Optional[Transform] = None,
        target_transform: Optional[Transform] = None,
    ):
        self._n = n
        self.transform = transform
        self.target_transform = target_transform

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def _get_data_and_label(self, index: int) -> DataAndLabel:
        pass

    def __getitem__(self, index: int) -> Tuple[Tensor, Tensor]:
        if index < 0 or index >= len(self):
            raise ClassiqIndexError(f"{self.__class__.__name__} out of range")

        the_data, the_label = self._get_data_and_label(index)

        data = tensor(the_data)
        if self.transform:
            data = self.transform(data)

        label = tensor(the_label)
        if self.target_transform:
            label = self.target_transform(label)

        return data.float(), label.float()

    def _get_bin_str(self, num: int) -> str:
        return bin(num)[2:].zfill(self._n)[::-1]


class MySubsetDataset(MyDataset, ABC):
    def __init__(
        self,
        n: int = 2,
        subset: Union[List[int], Literal["all"]] = "all",
        transform: Optional[Transform] = None,
        target_transform: Optional[Transform] = None,
    ):
        super().__init__(n, transform, target_transform)

        self._subset: Sequence[int]
        if isinstance(subset, list):
            if not all(0 <= i < n for i in subset):
                raise ClassiqValueError(
                    "Invalid subset indices. Make sure each index is between [0, n)"
                )
            self._subset = subset
        elif subset == "all":
            self._subset = range(n)
        else:
            raise ClassiqValueError(
                'Invalid subset - please enter a `list` of `int`, or the string "all"'
            )

    def _get_subset(self, coll: Sequence[T]) -> List[T]:
        return [coll[i] for i in self._subset]


class DatasetNot(MyDataset):
    def __len__(self) -> int:
        return 2

    def _get_data_and_label(self, index: int) -> DataAndLabel:
        if index == 0:
            data = all_bits_to_zero(self._n)
            label = all_bits_to_one(self._n)
        elif index == 1:
            data = all_bits_to_one(self._n)
            label = all_bits_to_zero(self._n)
        else:
            raise ClassiqIndexError(f"{self.__class__.__name__} out of range")

        return [data], [label]


class DatasetXor(MyDataset):
    def __len__(self) -> int:
        return 2**self._n

    def _get_data_and_label(self, index: int) -> DataAndLabel:
        bin_str = self._get_bin_str(index)
        data_value = map(int, bin_str)

        label_value = bin_str.count("1") % 2

        return list(data_value), [int(label_value)]


class DatasetSubsetParity(MySubsetDataset):
    def __init__(
        self,
        n: int = 2,
        subset: Union[List[int], Literal["all"]] = "all",
        add_readout_qubit: bool = True,
        transform: Optional[Transform] = None,
        target_transform: Optional[Transform] = None,
    ):
        super().__init__(n, subset, transform, target_transform)

        self._add_readout_qubit = add_readout_qubit

    def __len__(self) -> int:
        return 2**self._n

    def _get_data_and_label(self, index: int) -> DataAndLabel:
        bin_str = self._get_bin_str(index)

        data = list(map(int, bin_str)) + [0] * self._add_readout_qubit

        label_value = self._get_subset(bin_str).count("1") % 2

        return data, [int(label_value)]


class DatasetParity(DatasetSubsetParity):
    def __init__(
        self,
        n: int = 2,
        add_readout_qubit: bool = True,
        transform: Optional[Transform] = None,
        target_transform: Optional[Transform] = None,
    ):
        super().__init__(n, "all", add_readout_qubit, transform, target_transform)


DATASET_NOT = DatasetNot(
    1, transform=Lambda(state_to_weights), target_transform=Lambda(state_to_label)
)
DATALOADER_NOT = DataLoader(DATASET_NOT, batch_size=2, shuffle=True)

DATASET_XOR = DatasetXor()
DATALOADER_XOR = DataLoader(DATASET_XOR, batch_size=4, shuffle=True)

DATASET_SUBSET_PARITY = DatasetSubsetParity(
    3,
    [0, 2],
    transform=Lambda(state_to_weights),
    target_transform=Lambda(state_to_label),
)
DATALOADER_SUBSET_PARITY = DataLoader(DATASET_SUBSET_PARITY, batch_size=8, shuffle=True)
