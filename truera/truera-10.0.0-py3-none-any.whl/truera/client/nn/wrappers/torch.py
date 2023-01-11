from collections.abc import Collection
from collections.abc import Sequence
from collections.abc import Sized
from math import ceil
from typing import Iterable

from truera.client.nn import get_torch
from truera.client.nn import NNBackend as NNB
from truera.client.nn.wrappers import Types
from truera.client.util.iter_utils import LenIterable
from truera.client.util.iter_utils import LenIterator


def import_torch():
    """
    Import torch module. Raises exception if torch not found.
    """
    torch = get_torch()
    if not torch:
        raise RuntimeError(
            "Could not load torch; if you are wrapping a torch model, make sure pytorch is installed."
        )
    return torch


torch = import_torch()
data = torch.utils.data


class Backend(NNB[torch.Tensor, torch.nn.Module]):
    # TODO(piotrm): see if we can reuse trulens NNBackend

    # backend-specific model representations for pytorch are torch.nn.Module
    Model = torch.nn.Module

    class Tensor(torch.Tensor):
        """
        Pytorch tensors annotated with Truera-related indicators such as Input
        vs. Output, Batchable vs. Non-Batchable.
        """

        torch = __import__('torch')
        # TODO(piotrm): figure out how not have to import here too

        @classmethod
        def __torch_function__(cls, func, types, args=(), kwargs=None):
            """Undo our custom tensor types once any torch method is called
            on them."""
            return super().__torch_function__(
                func, map(lambda t: cls.torch.Tensor, types),
                map(
                    lambda arg: arg.as_subclass(cls.torch.Tensor)
                    if isinstance(arg, cls.torch.Tensor) else arg, args
                ), kwargs
            )

        @staticmethod
        def __new__(cls, tensor):
            return tensor.as_subclass(cls)

    class Inputs(Tensor):
        """
        Input tensors.
        """

    class Batchable(Inputs):
        """
        Batchable input tensors.
        """

    class Parameter(Inputs):
        """
        Non-batchable input tensors.
        """

    class Embeddings(Batchable):
        """
        Embeddings tensors.
        """

    class Masks(Batchable):
        """
        Attention masks tensors.
        """

    class Words(Batchable):
        """
        Words tensors (i.e. not embeddings).
        """

    class Outputs(Tensor):
        """
        Model output tensors.
        """

    class Logits(Outputs):
        """
        Logit outputs.
        """

    class Probits(Outputs):
        """
        Probit outputs.
        """


class Torch:
    """Pytorch-specific methods and wrapper requirements."""

    class Dataset(data.Dataset, Sequence, Collection):
        """
        A basic implementation of pytorch's Dataset. Checks to make sure instances are indexable.
        """

        def __init__(self, instances: Iterable):
            self._instances = instances
            assert hasattr(
                self._instances, "__getitem__"
            ), "instances is not indexable"

        def __len__(self):
            return len(self._instances)

        def __getitem__(self, i):
            return self._instances[i]

    class IterableDataset(data.IterableDataset, Sized):
        """
        A basic implementation of pytorch's IterableDataset. Constructed with an
        iterable of instances and iterates them when called upon. Can store a length.
        """

        def __init__(self, instances: Iterable, len: int = None):
            self._instances = instances
            self._len = len

        def __len__(self):
            if self._len is not None:
                return self._len
            else:
                raise ValueError("Do not know how many instances I have.")

        def __map__(self, func):
            return LenIterable(self._instances).map(func)

        def __iter__(self):
            return LenIterator(self._instances, len=self._len)

    class DataLoader(data.DataLoader, Sized):
        """
        A variant of pytorch's DataLoader that can collate dataclasses like
        DataBatch. Can also store a length.
        """

        def __init__(self, dataset, batch_size: int, *args, **kwargs):
            super().__init__(
                collate_fn=Types.DataBatch.collate,
                *args,
                dataset=dataset,
                batch_size=batch_size,
                **kwargs
            )

            self._len = None

            try:
                total_items = len(dataset)
                self._len = ceil(total_items / batch_size)
            except:
                pass

        def __len__(self):
            return self._len

        def __map__(self, func):
            return LenIterable((func(batch) for batch in self), len=self._len)

        def __iter__(self):
            return LenIterator(data.DataLoader.__iter__(self), len=self._len)

    @staticmethod
    def get_device() -> torch.device:
        # TODO: might need to generalize or configure this method. However, it
        # should probably not be a user provided method.
        use_cuda = torch.cuda.is_available()

        if use_cuda:
            return torch.device("cuda", torch.cuda.current_device())
        else:
            return torch.device("cpu", 0)
