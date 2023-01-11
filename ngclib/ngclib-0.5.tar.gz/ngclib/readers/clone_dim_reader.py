"""CloneDimReader module"""
from typing import Dict, Callable
from torch.utils.data import Dataset

class CloneDimReader(Dataset):
    """
    A Reader used to clone some identical dimensions.
    For example: dims: {"rgb2": "rgb", "rgb3": "rgb"} means that "rgb", "rgb2" and "rgb3" use the same underlying data,
    so, in the final result we return a dictionary with all 3 keys pointing to the same "rgb" data coming from the
    base reader.
    """
    def __init__(self, base_reader: Dataset, dims: Dict):
        self.base_reader = base_reader
        self.dims = dims

    def __getitem__(self, index):
        original_data = self.base_reader.__getitem__(index)
        res = {}
        for dim in original_data.keys():
            if dim not in self.dims:
                res[dim] = original_data[dim]
            else:
                for sub_dim in self.dims[dim]:
                    assert sub_dim not in res
                    res[sub_dim] = original_data[dim]
        return res

    def __len__(self) -> int:
        return len(self.base_reader)

    def collate_fn(self, x) -> Callable:
        """Collate fn for this wrapper"""
        return self.base_reader.collate_fn(x)
