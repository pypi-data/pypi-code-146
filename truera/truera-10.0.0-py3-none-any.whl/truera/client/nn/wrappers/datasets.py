from dataclasses import make_dataclass
from itertools import chain
from typing import Any, Callable, Iterable, Mapping, Optional, Sequence

import numpy as np
import pandas as pd

from truera.client.nn import Batch
from truera.client.nn.wrappers import Types
from truera.client.util.iter_utils import LenIterable


def convert_to_truera_iterable(
    dataset: Any,
    *,
    accessors: Optional[Mapping[str, Callable]] = None,
    batch_size: int = 16,
    n_records: Optional[int] = None
) -> LenIterable[Batch]:
    """Converts dataset into a LenIterable object for TruEra.

    Args:
        dataset (Any): A dataset object. Can be a pandas DataFrame, PyTorch or Tensorflow Dataset, or any other iterable. 
        accessors (Optional[Mapping[str, Callable]], optional): Mapping from field names to functions that acccess fields from each element in `dataset`. If `None`, will infer based on the datatype of `dataset` elements. Defaults to None.
        batch_size (int, optional): The batch size used for computing influences. Defaults to 16.
        n_records (Optional[int], optional): The number of entries in `dataset`. Defaults to None.

    Returns:
        LenIterable[Batch]: A LenIterable data structure for internal TruEra batching and shuffling. 
    """

    if isinstance(dataset, Batch):
        return dataset.batch(batch_size=batch_size)
    elif isinstance(dataset, LenIterable):
        return Batch.rebatch(dataset, batch_size=batch_size)
    elif isinstance(dataset, pd.DataFrame):
        keyed_iterables_kwargs = {col: dataset[col] for col in dataset.columns}
        keyed_iterables_kwargs['index'] = dataset.index

        fields = [
            (col_name, np.ndarray, Batch.field(np.array))
            for col_name in dataset.columns
        ]
        fields.append(("index", np.ndarray, Batch.field(np.array)))
        PandasDataBatch = make_dataclass(
            'PandasDataBatch', fields, bases=(Types.DataBatch,)
        )
        everything = PandasDataBatch(**keyed_iterables_kwargs)
        return everything.batch(batch_size=batch_size)
    elif isinstance(dataset, Iterable):
        ds_iter = iter(dataset)
        single_record = next(ds_iter)
        ds_iter = chain([single_record], ds_iter)

        if accessors is None:
            if isinstance(single_record, Sequence):
                accessors = {
                    f"idx_{i}":
                    (lambda i: lambda x: x[i])(i
                                              )  # currying for variable scoping
                    for i in range(len(single_record))
                }
            elif isinstance(single_record, Mapping):
                accessors = {
                    str(key): lambda x: x[key] for key in single_record.keys()
                }
            else:
                raise ValueError(
                    f"Encountered unhandled record type {type(single_record)}"
                )

        for key, acc in accessors.items():
            try:
                acc(single_record)
            except Exception as e:
                raise ValueError(
                    f"Accessor for key {key} failed with error: {str(e)}"
                )

        IteratorDataBatch = make_dataclass(
            'IterDataBatch', [
                (key, np.ndarray, Batch.field(np.array))
                for key in accessors.keys()
            ],
            bases=(Types.DataBatch,)
        )

        def iterator_batcher():
            batch = []
            for element in ds_iter:
                keyed_iterables_kwargs = {
                    key: [acc(element)] for key, acc in accessors.items()
                }
                batch.append(IteratorDataBatch(**keyed_iterables_kwargs))
                if len(batch) >= batch_size:
                    yield IteratorDataBatch.collate(batch)
                    batch = []
            yield IteratorDataBatch.collate(batch)

        return LenIterable(
            iterator_batcher(), len=n_records, batch_size=batch_size
        )
