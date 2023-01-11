from itertools import chain
from itertools import islice
import logging
from math import ceil
from typing import Callable, Iterable, Iterator, Optional, Tuple

import numpy as np
from trulens.nn.backend import Backend

from truera.client.nn import NNBackend as NNB
from truera.client.nn import wrappers as base
from truera.client.nn.nn_wrappers_torch import Torch
from truera.client.nn.wrappers import nlp
from truera.client.util.iter_utils import LenIterable
from truera.rnn.general.utils import log

log.configure(logging.INFO)

_SEED_VAL = 3489534


def _is_lengthed(obj):
    """Determine whether the given object has a fixed length."""

    try:
        len(
            obj
        )  # note that need to call as some containers define __len__ but fail if you try to call it
        return True
    except:
        return False


def _batch_indexable(indexable, batch_size=1):
    """
    Batch a container that can be indexed into generator of batches of the given size.
    """

    if not _is_lengthed(indexable):
        log.warning(
            f"Container of type {type(indexable)} is not indexable, will have to collect it first."
        )
        indexable = [item for item in indexable]

    l = len(indexable)

    for ndx in range(0, l, batch_size):
        yield indexable[ndx:min(ndx + batch_size, l)]


def prepare_datasplit(
    ds: Iterable,
    *,
    backend: Backend,
    batch_size: int,
    model: NNB.Model,
    model_wrapper: base.Wrappers.ModelRunWrapper,
    tokenizer_wrapper: Optional[nlp.Wrappers.TokenizerWrapper] = None,
    standardize_fn: Callable = None,
    num_take_records: Optional[int] = None,
    shuffle: Optional[bool] = False,
) -> Tuple[LenIterable, int, bool]:
    """
    Standardizes the iteration strategy of the various iterables coming out of
    ModelRunWrapper.get_ds.

    ds may be:
       - pytorch DataLoader?
       - List?
       - pandas DataFrame?
       - tensorflow something?

    Args:
        - ds (Iterable): An iterable dataset from ModelRunWrapper.get_ds.
        - backend (Backend): The trulens discerned backend,
        - batch_size (int): The number of desired items per batch.
        - model (Model): The model object.
        - model_wrapper (Base.ModelRunWrapper): The ModelRunWrapper
          implementation.
        - tokenizer_wrapper (TokenizerWrapper, optional): The TokenizerWrapper
          implementation if this is an NLP domain. Defaults to None.
        - num_take_records (int, optional): The desired total number of items in
          the dataset. Defaults to None (All items kept).
        - shuffle (bool, optional): Whether to shuffle the dataset. Defaults to
          False.

    Returns:
        Iterable: The standardized iterable dataset.
    """
    if tokenizer_wrapper is not None:
        return prepare_datasplit_nlp(
            ds,
            num_take_records=num_take_records,
            shuffle=shuffle,
            standardize_fn=standardize_fn
        )

    if _is_lengthed(ds):
        log.warning(
            f"Datasplit (type {type(ds)}) has length {(len(ds))} which means it might have been entirely preloaded."
        )

    is_unknown_ds_type = False
    fn = prepare_datasplit_torch if backend == Backend.PYTORCH else prepare_datasplit_tf
    try:
        prepared_ds = fn(
            ds, batch_size, num_take_records=num_take_records, shuffle=shuffle
        )

    except Exception as err:

        log.warning("Exception reading data. Treating dataset as iterable.")
        log.warning(err)
        is_unknown_ds_type = True

        if hasattr(ds, '__getitem__'):
            dataset_single_batch = ds[0]  # get item directly
        elif isinstance(ds, Iterator):
            dataset_single_batch = next(ds)
            ds = chain([dataset_single_batch], ds)
        else:
            dataset_single_batch = next(iter(ds))

        truera_elements = model_wrapper.trubatch_of_databatch(
            dataset_single_batch, model=model
        )
        # We cannot guarantee our old batchsize, so reset to the ds batchsize
        # TODO: why?
        if hasattr(truera_elements, "index"):
            batch_size = truera_elements.index.shape[0]
        else:
            batch_size = truera_elements.ids.shape[0]

        if num_take_records is not None:
            if batch_size > num_take_records:
                # If batch_size is greater than the number of records we want,
                # reduce the batch size to it and grab a batch of exactly that
                # size.

                log.warning(
                    f"Decreasing batch_size to num_take_records={num_take_records}."
                )

                batch_size = num_take_records

                def new_iterator():
                    try:
                        only_batch = next(iter(ds))
                        yield only_batch[0:batch_size]
                    except StopIteration:
                        return

                prepared_ds = LenIterable(
                    new_iterator(), len=1, batch_size=batch_size
                )

            else:
                num_take_batches = ceil(num_take_records / batch_size)
                prepared_ds = LenIterable(
                    islice(ds, None, num_take_batches),
                    len=num_take_batches,
                    batch_size=batch_size
                )

        else:
            prepared_ds = ds
        if standardize_fn is not None:
            prepared_ds = prepared_ds.map(standardize_fn)
        return prepared_ds, batch_size, is_unknown_ds_type


def prepare_datasplit_nlp(
    ds: LenIterable,
    *,
    num_take_records: Optional[int] = None,
    shuffle: Optional[bool] = False,
    standardize_fn: Callable = None,
) -> Tuple[LenIterable, int, bool]:
    """
    Truncate and (future) shuffle data coming from ModelRunWrapper.get_ds.

    Args:
        - ds (Iterable): An iterable dataset from ModelRunWrapper.get_ds.
        - num_take_records (int, optional): The desired total number of items in
          the dataset. Defaults to None (All items kept).
        - shuffle (bool, optional): Whether to shuffle the dataset. Defaults to
          False.

    Returns:
        Iterable: The standardized iterable dataset.
    """

    assert isinstance(ds, LenIterable), "LenIterable expected for NLP models"
    assert not shuffle, "Shuffle not yet supported for NLP models"

    is_unknown_ds_type = True

    batch_size = ds.batch_size
    if num_take_records is not None:
        if batch_size > num_take_records:
            # If batch_size is greater than the number of records we want,
            # reduce the batch size to it and grab a batch of exactly that
            # size.

            log.warning(
                f"Decreasing batch_size to num_take_records={num_take_records}."
            )

            batch_size = num_take_records

            def new_iterator():
                try:
                    only_batch = next(iter(ds))
                    yield only_batch[0:batch_size]
                except StopIteration:
                    return

            prepared_ds = LenIterable(
                new_iterator(), len=1, batch_size=batch_size
            )

        else:
            num_take_batches = ceil(num_take_records / batch_size)
            prepared_ds = LenIterable(
                islice(ds, None, num_take_batches),
                len=num_take_batches,
                batch_size=batch_size
            )

    else:
        prepared_ds = ds
    if standardize_fn is not None:
        prepared_ds = prepared_ds.map(standardize_fn)
    return prepared_ds, batch_size, is_unknown_ds_type


def prepare_datasplit_text(
    text_ds, batch_size, num_take_records=None, shuffle=True
):
    """
    Adjust the given iterable to be shuffled and/or return a subset of records.
    """

    if shuffle:
        np.random.seed(_SEED_VAL)

    if num_take_records:
        indices = np.arange(num_take_records
                           ) if not shuffle else np.random.choice(
                               len(text_ds[0]), num_take_records
                           )
        text_ds = text_ds[indices]

    ds = _batch_indexable(text_ds, batch_size=batch_size)

    return ds


def prepare_datasplit_torch(
    ds: Iterable,
    batch_size: int,
    num_take_records=None,
    shuffle=False
) -> 'torch.utils.data.DataLoader':
    # NOT USED FOR BETA
    """
    Standardizes the iteration strategy of the torch iterables coming out of
    ModelRunWrapper.get_ds.

    Args:
        - ds (Iterable): An iterable dataset from ModelRunWrapper.get_ds.
        - batch_size (int): The number of desired items per batch.
        - num_take_records (int, optional): The desired total number of items in
          the dataset. Defaults to None (All items kept).
        - shuffle (bool, optional): Whether to shuffle the dataset. Defaults to
          False.

    Returns:
        torch.utils.data.DataLoader: The new dataset in a torch Dataloader
    """
    import torch
    from torch.utils.data import DataLoader
    from torch.utils.data import Subset

    assert isinstance(ds, DataLoader)

    ds_cls = ds.__class__
    ds_unbatched = ds.dataset  # might be IterableDataset

    assert not isinstance(
        ds_unbatched, Torch.IterableDataset
    ), "iterable dataset given but indexed one expected"

    if num_take_records:
        num_take_records = min(num_take_records, len(ds_unbatched))

    if shuffle:
        np.random.seed(_SEED_VAL)
        torch.manual_seed(_SEED_VAL)
        torch.cuda.manual_seed(_SEED_VAL)

    indices = np.arange(num_take_records) if not shuffle else np.random.choice(
        len(ds_unbatched), num_take_records, replace=False
    )
    # TODO: replace this with custom subset if needed
    ds_unbatched = Subset(ds_unbatched, indices)

    ds = DataLoader(ds_unbatched, batch_size=batch_size)

    return ds


def prepare_datasplit_tf(
    ds: Iterable,
    batch_size: int,
    num_take_records=None,
    shuffle=True
) -> 'tf.data.Dataset':
    # NOTE USED FOR BETA
    """
    Standardizes the iteration strategy of the tensorflow iterables coming out
    of ModelRunWrapper.get_ds.

    Args
    ----
    - ds (Iterable): An iterable dataset from ModelRunWrapper.get_ds.
    - batch_size (int): The number of desired items per batch.
    - num_take_records (int, optional): The desired total number of items in the
      dataset. Defaults to None (All items kept).
    - shuffle (bool, optional): Whether to shuffle the dataset. Defaults to
      False.

    Returns
    -------
    - tf.data.Dataset: The new dataset in a tf Dataset
    """
    import tensorflow as tf

    assert isinstance(ds, tf.data.Dataset)

    try:
        # Dataset may or may not be batched. There is no easy way to check other than to try unbatching.
        unbatched = ds.unbatch()
        ds = unbatched
    except:
        log.info("Dataset is already unbatched")
    if shuffle:
        ds = ds.shuffle(buffer_size=30000, seed=_SEED_VAL)
    if num_take_records is not None:
        ds = ds.take(num_take_records)
    ds = ds.batch(batch_size)

    return ds
