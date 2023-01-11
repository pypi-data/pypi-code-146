"""Utils module"""
from functools import lru_cache
from typing import List
from pathlib import Path
import shutil
import numpy as np
from ..logger import drange, logger


@lru_cache
def load_npz(path: Path) -> np.ndarray:
    """Loads a NPZ given a path. Caveats for VRE exported npz."""
    try:
        item = np.load(path, allow_pickle=True)["arr_0"]
    except Exception as e:
        print(f"Error at reading file '{path}'.")
        raise Exception(e)
    # For items exported using VRE.
    if item.dtype == object:
        item = item.item()
        assert isinstance(item, dict)
        assert "data" in item
        item = item["data"]
    assert item.dtype in (np.uint8, np.uint32, np.float16, np.float32, np.float64), f"Got {item.dtype} for {path}"
    if item.shape[0] == 1:
        item = item[0]
    return item

def load_npz_from_list(paths: List[Path]) -> np.ndarray:
    """Loads a list of npz given a list of paths using load_npz function."""
    items = []
    for i in drange(len(paths), desc="Loading Npz"):
        item = load_npz(paths[i])
        items.append(item)
    items = np.array(items).astype(np.float32)
    return items

def generate_random_data(output_dir: Path, names: List[str], dims: List[int], types: List[str],
                         shape: List[int], num_items: List[int], overwrite: bool = False, prefix: str = ""):
    """Generates a dataset in ngcdir format"""
    if output_dir.exists():
        if not overwrite:
            logger.warning(f"'{output_dir}' exists and overwrite is set to False. Returning early.")
            return
        logger.warning(f"'{output_dir}' exists and overwrite is set to True. Removing it first.")
        shutil.rmtree(str(output_dir))
    k = len(names)
    dims = k * [dims] if isinstance(dims, int) else dims
    types = k * [types] if isinstance(types, str) else types
    num_items = k * [num_items] if isinstance(num_items, int) else num_items
    assert len(names) == len(dims) == len(types) == len(num_items)

    output_dir.mkdir(exist_ok=True, parents=True)
    for name, D, node_type, N in zip(names, dims, types, num_items):
        assert node_type in ("float", "categorical"), node_type
        (output_dir / name).mkdir()
        if node_type == "float":
            data = np.random.rand(N, *shape, D).astype(np.float16)
        else:
            data = np.random.randint(0, D-1, size=(N, *shape)).astype(np.uint8)

        for j in drange(N, desc=name):
            out_file = output_dir / name / f"{prefix}{j}.npz"
            np.savez(out_file, data[j])
