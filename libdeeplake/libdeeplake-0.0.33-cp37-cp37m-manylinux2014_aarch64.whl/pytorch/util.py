from deeplake.util.iterable_ordered_dict import IterableOrderedDict
import numpy as np
from typing import Union
import math


def transform_collate_batch(batch, transform_fn, collate_fn, upcast, raw_tensor_set):
    if raw_tensor_set:
        for sample in batch:
            for k, v in sample.items():
                if k in raw_tensor_set and isinstance(v, np.ndarray):
                    sample[k] = v.tobytes()
    if upcast:
        it_order_dict_batch = [
            IterableOrderedDict((k, upcast_array(v)) for k, v in sample.items())
            for sample in batch
        ]
    else:
        it_order_dict_batch = [IterableOrderedDict(sample) for sample in batch]
    if transform_fn is not None:
        transformed = list(map(transform_fn, it_order_dict_batch))
    else:
        transformed = it_order_dict_batch
    if collate_fn is not None:
        collated = collate_fn(transformed)
    else:
        collated = transformed
    return collated


def upcast_array(arr: Union[np.ndarray, bytes]):
    if isinstance(arr, list):
        return [upcast_array(a) for a in arr]
    if isinstance(arr, np.ndarray):
        if arr.dtype == np.uint16:
            return arr.astype(np.int32)
        if arr.dtype == np.uint32:
            return arr.astype(np.int64)
        if arr.dtype == np.uint64:
            return arr.astype(np.int64)
    return arr


def get_indexes(
    dataset, rank=None, num_replicas=None, shuffle=False, drop_last=True, seed=0
):
    import torch.distributed as dist

    if num_replicas is None:
        if not dist.is_available():
            raise RuntimeError("Requires distributed package to be available")
        num_replicas = dist.get_world_size()
    if rank is None:
        if not dist.is_available():
            raise RuntimeError("Requires distributed package to be available")
        rank = dist.get_rank()
    if rank >= num_replicas or rank < 0:
        raise ValueError(
            "Invalid rank {}, rank should be in the interval"
            " [0, {}]".format(rank, num_replicas - 1)
        )
    # If the dataset length is evenly divisible by # of replicas, then there
    # is no need to drop any data, since the dataset will be split equally.
    if drop_last and len(dataset) % num_replicas != 0:  # type: ignore[arg-type]
        # Split to nearest available length that is evenly divisible.
        # This is to ensure each rank receives the same amount of data when
        # using this Sampler.
        num_samples = math.ceil(
            # `type:ignore` is required because Dataset cannot provide a default __len__
            # see NOTE in pytorch/torch/utils/data/sampler.py
            (len(dataset) - num_replicas)
            / num_replicas  # type: ignore[arg-type]
        )
    else:
        num_samples = math.ceil(len(dataset) / num_replicas)  # type: ignore[arg-type]
    total_size = num_samples * num_replicas

    indices = list(range(len(dataset)))  # type: ignore[arg-type]

    if not drop_last:
        # add extra samples to make it evenly divisible
        padding_size = total_size - len(indices)
        if padding_size <= len(indices):
            indices += indices[:padding_size]
        else:
            indices += (indices * math.ceil(padding_size / len(indices)))[
                :padding_size
            ]
    else:
        # remove tail of data to make it evenly divisible.
        indices = indices[:total_size]
    assert len(indices) == total_size

    # subsample
    indices = indices[rank * num_samples : (rank + 1) * num_samples]
    assert len(indices) == num_samples

    return indices
