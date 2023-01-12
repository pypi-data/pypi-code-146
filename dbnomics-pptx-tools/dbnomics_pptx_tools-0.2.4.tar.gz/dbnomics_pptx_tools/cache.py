from pathlib import Path
from typing import Optional

import pandas as pd
from pandas import DataFrame
from slugify import slugify


class SeriesCache:
    def __init__(self, *, auto_create_dir=True, cache_dir: Path):
        self._auto_create_dir = auto_create_dir
        self._cache_dir = cache_dir

    def get(self, series_id: str) -> Optional[DataFrame]:
        file_path = self._get_series_json_file_path(series_id)
        if not file_path.is_file():
            return None
        return pd.read_json(
            file_path, convert_dates=["period"], dtype={"original_period": str}, orient="records"  # type: ignore
        )

    def has(self, series_id: str) -> bool:
        file_path = self._get_series_json_file_path(series_id)
        return file_path.is_file()

    def set(self, series_id: str, series_df: DataFrame):
        file_path = self._get_series_json_file_path(series_id)
        if self._auto_create_dir:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        series_df.to_json(file_path, date_format="iso", indent=2, orient="records")

    def _get_series_json_file_name(self, series_id: str) -> str:
        return slugify(series_id) + ".json"

    def _get_series_json_file_path(self, series_id: str) -> Path:
        return self._cache_dir / self._get_series_json_file_name(series_id)
