"""PyTorch implementations of the datafactory module contents."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Union, cast

from bitfount.backends.pytorch.data.dataloaders import (
    PyTorchBitfountDataLoader,
    PyTorchIterableBitfountDataLoader,
    _BasePyTorchBitfountDataLoader,
)
from bitfount.backends.pytorch.data.datasets import (
    _PyTorchDataset,
    _PyTorchIterableDataset,
)
from bitfount.data.datafactory import _DataFactory
from bitfount.data.datasources.base_source import BaseSource, IterableSource

if TYPE_CHECKING:
    from bitfount.data.datasets import _BaseBitfountDataset
    from bitfount.data.datasplitters import DatasetSplitter
    from bitfount.data.schema import TableSchema
    from bitfount.data.types import DataSplit, _SemanticTypeValue
    from bitfount.transformations.batch_operations import BatchTimeOperation


class _PyTorchDataFactory(_DataFactory):
    """A PyTorch-specific implementation of the DataFactory provider."""

    def create_dataloader(
        self,
        dataset: _BaseBitfountDataset,
        batch_size: Optional[int] = None,
    ) -> _BasePyTorchBitfountDataLoader:
        """See base class."""
        if isinstance(dataset, _PyTorchIterableDataset):
            return PyTorchIterableBitfountDataLoader(
                dataset=dataset, batch_size=batch_size
            )
        elif isinstance(dataset, _PyTorchDataset):
            return PyTorchBitfountDataLoader(dataset, batch_size=batch_size)

        raise TypeError(
            "The _PyTorchDataFactory class only supports "
            "subclasses of PyTorch Dataset for creating a DataLoader."
        )

    def create_dataset(
        self,
        datasource: BaseSource,
        data_splitter: Optional[DatasetSplitter],
        data_split: DataSplit,
        schema: TableSchema,
        selected_cols: List[str],
        selected_cols_semantic_types: Mapping[_SemanticTypeValue, List[str]],
        target: Optional[Union[str, List[str]]] = None,
        batch_transforms: Optional[List[BatchTimeOperation]] = None,
        auto_convert_grayscale_images: bool = True,
        **kwargs: Any,
    ) -> Union[_PyTorchDataset, _PyTorchIterableDataset]:
        """See base class."""
        if datasource.iterable:
            return _PyTorchIterableDataset(
                schema=schema,
                selected_cols_semantic_types=selected_cols_semantic_types,
                data_splitter=data_splitter,
                datasource=cast(IterableSource, datasource),
                target=target,
                selected_cols=selected_cols,
                batch_transforms=batch_transforms,
                data_split=data_split,
                auto_convert_grayscale_images=auto_convert_grayscale_images,
                **kwargs,
            )

        return _PyTorchDataset(
            schema=schema,
            selected_cols_semantic_types=selected_cols_semantic_types,
            data_splitter=data_splitter,
            datasource=datasource,
            target=target,
            selected_cols=selected_cols,
            batch_transforms=batch_transforms,
            data_split=data_split,
            auto_convert_grayscale_images=auto_convert_grayscale_images,
            **kwargs,
        )
