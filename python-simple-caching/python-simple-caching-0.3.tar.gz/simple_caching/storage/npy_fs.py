"""Npy FS module. Caches data on the disk using numpy (pickle) format."""
from typing import Optional
from pathlib import Path
from overrides import overrides
import numpy as np
from ..cache import Cache, EncodedKeyType, ValueType

class NpyFS(Cache):
    """Npy FS implementation"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.base_dir = Path.cwd() / self.name
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.iterdir = [x.name for x in self.base_dir.iterdir()]

    @overrides
    def _set_value(self, encoded_key: EncodedKeyType, value: ValueType):
        file_name = self.base_dir / NpyFS._npy_key(encoded_key)
        np.save(file_name, value)
        self.iterdir = [x.name for x in self.base_dir.iterdir()]

    @overrides
    def _get(self, encoded_key: EncodedKeyType) -> Optional[ValueType]:
        file_name = self.base_dir / NpyFS._npy_key(encoded_key)
        item = np.load(file_name, allow_pickle=True)
        try:
            return item.item()
        except ValueError:
            return item

    @overrides
    def _check(self, encoded_key: EncodedKeyType) -> bool:
        check = NpyFS._npy_key(encoded_key) in self.iterdir
        return check

    @staticmethod
    def _npy_key(key: EncodedKeyType) -> str:
        return f"{key}.npy"

    def __str__(self) -> str:
        f_str = "[NpyFS]"
        f_str += f"\n - Dir: {self.base_dir}"
        f_str += f"\n - Num top level keys: {len(list(self.base_dir.iterdir()))}"
        return f_str

    def __repr__(self) -> str:
        return self.__str__()
