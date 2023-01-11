from __future__ import annotations

import dataclasses
from dataclasses import asdict
from dataclasses import astuple
from dataclasses import dataclass
from dataclasses import fields
from enum import Enum
import logging
from math import ceil
import os
from typing import Any, Dict, Generic, Iterable, List, Type, TypeVar
import warnings

from truera.client.util.iter_utils import it_peek
from truera.client.util.iter_utils import LenIterable

logger = logging.getLogger(__name__)

# NN product version
__version__ = "0.0.1"

# Backend-specific models:
BaseModel = TypeVar("BaseModel")

# Backend-specific tensors:
BaseTensor = TypeVar("BaseTensor")

# from trulens.utils.typing import BaselineLike
BaselineLike = Any
# Any is actually BaselineLike from trulens but don't want to import trulens
# here. This file is imported by truera.client.truera_workspace which is common
# across diagnostic and nn products.


def get_tf(version=None):
    # Method is here so that we can test for tf before importing
    # truera.client.nn.tf* which raise an exception if appropriate tf is not
    # found.
    """
    Get the tensorflow module. Returns false if it cannot be imported.
    """
    try:
        tf = __import__('tensorflow')

        if version is not None:
            if not tf.__version__.startswith(str(version)):
                logger.warning(
                    f"Requested tf version {version} but loaded {tf.__version__}."
                )
                return None

        return tf

    except:
        return False


def get_torch():
    # Method is here so that we can test for torch before importing
    # truera.client.nn.torch which raises an exception if torch is not found.
    """
    Get the torch module. Returns false if it cannot be imported.
    """
    try:
        torch = __import__('torch')
        return torch

    except:
        return False


class CUDA:

    @staticmethod
    def get_cuda():
        try:
            pynvml = __import__("pynvml")
            pynvml.nvmlInit()
            return pynvml
        except:
            raise RuntimeError(
                "pynvml not installed, cannot load CUDA utilities"
            )

    @staticmethod
    def select(min_ram: int = 0) -> None:
        """
        Find a device with the required amount of ram and then configure all
        available backends to use that device.
        """

        device = CUDA.find(min_ram)
        index = device['index']

        tf = get_tf(2)

        if tf:
            tf_devices = tf.config.list_physical_devices('GPU')
            if index >= len(tf_devices):
                warnings.warn(
                    "Tensorflow does not see the selected CUDA device; you will not be able to use tensorflow with CUDA support."
                )
            else:

                tf_device = tf_devices[index]

                # set default device for tensorflow
                tf.config.experimental.set_memory_growth(tf_device, True)
                tf.config.experimental.set_visible_devices([tf_device], 'GPU')

                logger.info(f"Set tf2 device to {tf_device}.")

        torch = get_torch()
        if torch:
            cuda = torch.cuda
            pytorch_device = torch.device("cuda", index)
            from truera.client.nn.wrappers.torch import Torch

            # set default device for pytorch:
            cuda.set_device(pytorch_device)

            logger.info(
                f"Set torch device to {pytorch_device.type}:{pytorch_device.index}."
            )

            logger.info(f"Torch.get_device() = {Torch.get_device()}")

    @staticmethod
    def find(min_ram: int = 0) -> Dict[str, Any]:
        """
        Find a CUDA device with at least `min_ram` memory available. Raises
        RuntimeException if no device with that requirement is available. This
        should be ran before any CUDA ram is allocated. This method will fail if
        the current process is already allocated on some CUDA device.
        """

        from humanize import naturalsize

        pynvml = CUDA.get_cuda()

        num_devices = pynvml.nvmlDeviceGetCount()
        logger.info(f"Have {num_devices} CUDA device(s).")

        # get current process id
        mypid = os.getpid()

        devices = []

        # Print out devices along with processes using them.
        for device in range(num_devices):
            handle = pynvml.nvmlDeviceGetHandleByIndex(device)

            # readable brand/model name
            name = pynvml.nvmlDeviceGetName(handle).decode('utf-8')

            # PCI bus location, may not be necessary if we just want any device
            # but I read indexes (`device`) can change which physical device
            # they refer to between reboots. PCI bus location may be needed to
            # disambiguate them.
            pci = pynvml.nvmlDeviceGetPciInfo(handle).busId.decode('utf-8')

            logger.info(f"  Device {device} @ {pci} ({name})")

            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)

            logger.info(
                f"    Memory available: {naturalsize(mem.free)} of {naturalsize(mem.total)}"
            )

            procs = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
            for proc in procs:
                logger.info(
                    f"    Proc: {proc.pid}, memory used: {naturalsize(proc.usedGpuMemory if proc.usedGpuMemory is not None else 0)}"
                )

                if proc.pid == mypid:
                    raise RuntimeError(
                        f"This notebook already allocated memory on device {device}; "
                        "Restart this notebook to (re)select a gpu."
                    )

            if mem.free < min_ram:
                logger.warning(
                    f"    Need at least {naturalsize(min_ram)} CUDA RAM, ignoring this device."
                )
            else:
                devices.append(
                    dict(
                        index=device,
                        pci=pci,
                        name=name,
                        procs=procs,
                        mem=dict(free=mem.free, total=mem.total, used=mem.used)
                    )
                )

        if len(devices) == 0:
            raise RuntimeError("Could not find any GPU's with enough space.")

        # sort devices by number of processes on them
        devices.sort(key=lambda d: len(d['procs']))

        device = devices[0]

        logger.info(f"  Picked device {device}")

        if len(device['procs']) > 0:
            logger.warning(
                "  There are processes already on the selected device. "
                "Someone else might be using it."
            )

        # get the device id of the selected device
        return device


class BaselineType(str, Enum):
    """Baselines for integrated gradients.

    - FIXED -- A baseline that does not depend on input instance, is the same
      regardless of instance. E.g. all zeros.
    - DYNAMIC -- A baseline that is a function of the input instance. E.g. word
      embeddings replaced by zeros, control token embeddings kept as is.
    - DYNAMIC_INDEP: a baseline that is a function of more than just the input
      instance. Not presently supported. E.g. baseline that is another instance
      in a dataset.
    - CLS_PAD: TODO: Documentation
    """

    FIXED = 'fixed'
    DYNAMIC = 'dynamic'
    DYNAMIC_INDEP = 'dynamic_indep'
    CLS_PAD = 'cls_pad'

    @staticmethod
    def from_str(label):
        if label == 'fixed':
            return BaselineType.FIXED
        elif label == 'dynamic':
            return BaselineType.DYNAMIC
        elif label == 'dynamic_indep':
            return BaselineType.DYNAMIC_INDEP
        elif label == 'cls_pad':
            return BaselineType.CLS_PAD
        raise NotImplementedError(f'BaselineType {label} not supported')


class NNBackend(Generic[BaseTensor, BaseModel]):
    """
    Various decorators over the base tensor type to indicate their function in a
    model or ML pipeline. Included here are Model and Tensor which are meant to
    extend BaseModel and BaseTensor respectively. The goal of these is to be
    able to distinguish objects which are wrapped for us or by us from ones
    which are not. Base versions may not be ready for us, while the ones in this
    backend are created or wrapped by us. They can further indicate some
    information like whether a tensor represents an input or output or something
    else.

    The tensor types form a hierarchy:

        Tensor
            Inputs
                Batchable
                    Embeddings
                    Masks
                    Words
                Parameter
            Outputs
                Logits
                Probits

    """

    # TODO: reuse or merge with trulens backends
    class Model(object):  # WANT: subclass BaseModel
        """
        Backend's representation of a model. A user model should contain this
        somewhere inside of it (or be it). This should subclass BaseModel
        but cannot specify that in python right now.
        """
        ...

    class Tensor(object):  # WANT: subclass BaseTensor
        """
        Framework-specific tensors annotated with Truera-related indicators such
        as Input vs. Output, Batchable vs. Non-Batchable.
        """
        ...

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


@dataclass
class Batch:
    # TODO: allow for non-batchable fields using NNBackend or similar.
    # TODO: allow for dicts and use for InputBatch as well.
    # TODO: some system for determining the number of batches
    """
    Project-specific data batch based on dataclasses. This class must be
    extended for a project. Fields can be customized but each must have values
    that are iterable (i.e. list) with the same number of items or None. Each
    field must be defined using the `field` method giving it a constructor.
    Common constructors are

    - tuple constructs tuple
    - list constructs list
    - torch.tensor constructs torch.Tensor
    - numpy.array constructs numpy.ndarray
    - TODO tensorflow something
    """

    def __len__(self):
        return len(getattr(self, fields(self)[0].name))

    def unit(self):
        return f"{self.__class__.__name__} of {len(self)} instances"

    @property
    def batch_fields(self):
        return (getattr(self, field.name) for field in fields(self))

    def __getitem__(self, slice):
        """
        Want `take` below but providing getitem for prefixes for compatility
        with other structures not implementing take.
        """

        if isinstance(slice, int):
            start = slice
            stop = slice
            step = 1
        else:
            start, stop, step = slice.start, slice.stop, slice.step

        if stop is None:
            stop = len(self)

        if step is None:
            step = 1

        assert start == 0 and step == 1, "only prefix is subscriptable"

        return self.take(slice.stop)

    def take(self, n: int):
        """
        Create a batch that contains only the first n instances in this batch.
        """

        tup_batch = tuple([] for _ in range(len(fields(self.__class__))))

        tup = astuple(self)

        for num_instances, item in enumerate(zip(*tup)):
            if num_instances >= n:
                break

            for i, iv in enumerate(item):
                tup_batch[i].append(iv)

        storage_classes = list(map(Batch._get_factory, fields(self.__class__)))

        tup_batch = tuple(
            map(
                lambda storage_class_v: storage_class_v[0](storage_class_v[1]),
                zip(storage_classes, tup_batch)
            )
        )

        return self.__class__(*tup_batch)

    @staticmethod
    def field(factory, *args, **kwargs):
        """
        Create a dataclass field with metadata including a reference to the
        given factory.
        """
        return dataclasses.field(
            metadata=dict(factory=factory), *args, **kwargs
        )

    @staticmethod
    def _get_factory(field):
        if "factory" not in field.metadata:
            raise ValueError(
                f"Field {field.name} does not have a factory. "
                "Make sure you define your fields with DataBatch.field ."
            )
        return field.metadata['factory']

    @staticmethod
    def flatten_batches(batches: Iterable[Batch]) -> Iterable[Batch]:
        """
        Given batches of some number of instances, return batches containing
        only one instance each.
        """
        for batch in batches:
            tup = astuple(batch)
            for vals in zip(
                *tup
            ):  # requires each value in tup is iterable, and has same number of items
                yield batch.__class__(*[[v] for v in vals])

    @staticmethod
    def asdict(batch: Batch) -> Dict[str, Any]:
        """
        Return the batch as a dictionary. Does not reccur like
        dataclasses.asdict does.
        """

        return {
            field.name: getattr(batch, field.name) for field in fields(batch)
        }

    @staticmethod
    def collate(items: Iterable[Batch]) -> Batch:
        """
        Given a collection of batches, produce one batch that contains all of
        the same items.
        """

        try:
            databatch, it = it_peek(iter(items))
        except StopIteration:
            raise RuntimeError("no databatches given to collate")

        data_fields = fields(databatch.__class__)

        # Will accumulate values from all items here.
        accumulators: Dict[str,
                           List] = {field.name: [] for field in data_fields}

        # Factories for each field.
        classes: Dict[str, Type] = {
            field.name: Batch._get_factory(field) for field in data_fields
        }

        # Loop through every batch in items.
        for databatch in it:

            # Get the fields as a dictionary.
            databatch_dict = Batch.asdict(databatch)

            # For every field,
            for field_name, field_value in databatch_dict.items():
                if field_value is not None:
                    # Append its value to appropriate accumulator if it is not
                    # None. Allowing none for optional fields.
                    accumulators[field_name].extend(field_value)

        # Stack/combine the accumulated values with the appropriate container
        # classes.
        for field_name, field_values in accumulators.items():
            storage_class = classes[field_name]

            if len(field_values) > 0:
                # Except for fields which accumulated Nothing.

                accumulators[field_name] = storage_class(field_values)
            else:
                # Keep the ones with None fields as None (i.e. don't use empty
                # list that we initialized the accumulators with).

                accumulators[field_name] = None

        # Reconstruct the dataclass using the accumulated/stacked values.
        return databatch.__class__(**accumulators)

    def batch(self, batch_size: int) -> LenIterable[Batch]:
        """
        Batch the contents of this batch into (presumably) smaller batches.
        """
        assert batch_size > 0, f"batch_size={batch_size} must be positive"

        return self.rebatch(batches=self.single(), batch_size=batch_size)

    def single(self) -> LenIterable[Batch]:
        return LenIterable([self], len=1, batch_size=len(self))

    @classmethod
    def _batch(
        cls: Type[Batch], items: Iterable[Batch], batch_size: int, len: int
    ) -> LenIterable[Batch]:
        """
        Given an iterable of DataBatches containing one instance each, batch the
        them into size `batch_size` DataBatches. The result is a DataBatch with
        the values for the various fields being of the `batch_size` size.
        """

        assert batch_size > 0, f"batch_size={batch_size} must be positive"

        it = iter(items)

        def generator():
            while True:
                instances = []
                try:
                    for _ in range(batch_size):
                        instances.append(next(it))
                except StopIteration:
                    pass

                if instances.__len__() > 0:
                    yield cls.collate(instances)
                else:
                    return

        return LenIterable(generator(), len=len, batch_size=batch_size)

    @classmethod
    def rebatch(cls: Type[Batch], batches: LenIterable[Batch],
                batch_size: int) -> LenIterable[Batch]:
        """
        Given an iterable over DataBatches of some size, rebatch them into
        DataBatches of `batch_size` size.
        """

        assert batch_size > 0, f"batch_size={batch_size} must be positive"

        len_guess = ceil(len(batches) * batches.batch_size / batch_size)

        # First flatten into single-instance batches.
        instances = cls.flatten_batches(batches)

        # The batch into the new size.
        return cls._batch(items=instances, batch_size=batch_size, len=len_guess)
