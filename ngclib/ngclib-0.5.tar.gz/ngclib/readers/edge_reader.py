"""Edge Reader module"""
from copy import deepcopy
from torch.utils.data import Dataset
from ..models.edges import NGCEdge

class EdgeReader(Dataset):
    """Edge Reader is used to train a specific edge"""
    def __init__(self, base_reader: Dataset, edge: NGCEdge):
        assert not isinstance(base_reader, EdgeReader), f"Got {type(base_reader)}"
        self.base_reader = deepcopy(base_reader)
        self.edge = edge
        self.in_keys = self.edge.get_in_keys()
        self.out_key = edge.output_node.name

    def __getitem__(self, index):
        return self.base_reader.__getitem__(index)

    def __len__(self) -> int:
        return len(self.base_reader)

    def collate_fn(self, x):
        """The main difference is here, in the fact that the label is just the out_key without any dictionary"""
        y = self.base_reader.collate_fn(x)
        data = {k: y["data"][k] for k in self.in_keys}
        labels = y["labels"][self.out_key]
        return {"data": data, "labels": labels}

    def __str__(self) -> str:
        A, B = self.edge.nodes
        str_type = str(type(self.edge)).split(".")[-1][0 : -2]
        f_str = f"[EdgeReader] {A}->{B} (Edge Type: {str_type} in_keys: {self.in_keys})"
        f_str += super().__str__()
        return f_str
