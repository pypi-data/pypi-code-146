import logging
from pathlib import Path
from typing import Dict

import pandas as pd
import pandas.errors

from fiddler.v2.schema.common import DatasetInfo

LOG = logging.getLogger(__name__)

NUM_ROWS = 1
JUST_THE_HEADER = 0


def validate_dataset_info(info: DatasetInfo) -> None:
    if not isinstance(info, DatasetInfo):
        raise ValueError(
            'Parameter `info` must be of type `DatasetInfo`. '
            f'Instead found object of type {type(info)}.'
        )


def validate_dataset_shape(files: Dict[str, Path]) -> None:
    rows = 0
    columns = 0

    for _, file_path in files.items():
        try:
            df = pd.read_csv(file_path, nrows=NUM_ROWS)
            rows, columns = df.shape
        except pandas.errors.EmptyDataError:
            rows = 0
            columns = 0

        # empty checks.
        if columns == 0:
            raise ValueError('No columns found in dataset provided.')
        if rows == 0:
            raise ValueError('No rows found in dataset provided.')


def validate_dataset_columns(dataset_info: DatasetInfo, file_path: Path) -> None:
    # we can safely assume that file_path points to a csv file
    df = pd.read_csv(file_path, nrows=JUST_THE_HEADER)

    missing_cols = set(col.name for col in dataset_info.columns) - set(
        df.columns.str.strip()
    )
    if len(missing_cols) > 0:
        LOG.warning(
            'Following columns are missing from uploaded dataset, '
            f'but are present in DatasetInfo schema: {missing_cols}.'
        )
