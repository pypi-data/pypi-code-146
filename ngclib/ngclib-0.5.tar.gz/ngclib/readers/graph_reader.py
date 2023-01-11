"""Graph Reader module"""
from typing import List, Callable
from torch.utils.data import Dataset

class GraphReader(Dataset):
    """GraphReader used to feed data for an entire NGC Graph"""
    def __init__(self, base_reader: Dataset, data_dims: List[str], label_dims: List[str]):
        self.base_reader = base_reader
        self.data_dims = data_dims
        self.label_dims = label_dims

    def __getitem__(self, index):
        original_data = self.base_reader.__getitem__(index)
        data, labels = {}, {}
        for dim in original_data.keys():
            if dim in self.data_dims:
                data[dim] = original_data[dim]
            if dim in self.label_dims:
                labels[dim] = original_data[dim]
        return {"data": data, "labels": labels}

    def __len__(self):
        return len(self.base_reader)

    def collate_fn(self, x) -> Callable:
        """Graph collate fn"""
        data = [y["data"] for y in x]
        labels = [y["labels"] for y in x]
        data = self.base_reader.collate_fn(data)
        labels = self.base_reader.collate_fn(labels)
        return {"data": data, "labels": labels}
