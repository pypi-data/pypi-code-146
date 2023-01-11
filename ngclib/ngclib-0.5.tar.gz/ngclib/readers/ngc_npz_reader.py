"""NGC Npz Reader module"""
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Callable, Union
from natsort import natsorted
import numpy as np
from nwgraph import Node
from nwutils.torch import tr_get_data
from torch.utils.data import Dataset
from ..logger import logger
from ..utils import load_npz, NGCAugmentation, GeneralPrototype, NodeSpecificPrototype

TransformsType = Union[Callable, Dict[Node, Callable]]


class NGCNpzReader(Dataset):
    """
    NGC Npz Reader implementation
    Expected directory structure:
    For Npy reader, we expect a structure of:
    path/
      node_1/0.npz, ..., N.npz
      ...
      node_n/0.npz, ..., N.npz

    Names can differ (i.e. 2022-01-01.npz), but must be consistent and equal across all nodes.
    """
    def __init__(self, path: Path, nodes: List[Node], out_nodes: List[str],
                 general_augmentation: List[GeneralPrototype] = None,
                 node_specific_augmentation: Dict[str, List[NodeSpecificPrototype]] = None,
                 in_key_transforms: Dict[str, str] = None):

        in_key_transforms = {} if in_key_transforms is None else in_key_transforms
        for gt_node in out_nodes:
            assert gt_node in nodes, f"GT node '{gt_node}' not in all nodes {nodes}"
        # Link to itself
        for node in nodes:
            if node.name not in in_key_transforms.keys():
                in_key_transforms[node.name] = node.name

        self.path = Path(path).absolute()
        self.nodes = list(nodes)
        self.out_nodes = [node for node in self.nodes if node.name in out_nodes]
        self.in_nodes = set(self.nodes).difference(self.out_nodes)
        self.name_to_node = {x.name: x for x in nodes}
        self.in_key_transforms = in_key_transforms
        self.in_files = self._build_dataset()
        self.augmentation = NGCAugmentation(nodes, general_augmentation, node_specific_augmentation)

    def collate_fn(self, x):
        """Collate fn for this reader"""
        # Merge the data in batches.
        data = {k.name: np.array([y["data"][k.name] for y in x]) for k in self.in_nodes}
        labels = {k.name: np.array([y["labels"][k.name] for y in x]) for k in self.out_nodes}
        names = np.array([y["name"] for y in x])
        # Put them together so we can augment them the same
        all_data = {**data, **labels}
        all_data_augmented = self.augmentation(all_data)
        data_augmented = tr_get_data({k.name: all_data_augmented[k] for k in self.in_nodes})
        labels_augmented = tr_get_data({k.name: all_data_augmented[k] for k in self.out_nodes})
        return {"data": data_augmented, "labels": labels_augmented, "name": names}

    def subreader(self, nodes: List[str]) -> NGCNpzReader:
        """Clones this reader with just a subset of nodes (used for partial graphs training)"""
        assert len(nodes) > 0
        diff = list(set(nodes).difference(self.nodes))
        if len(diff) != 0:
            logger.warning(f"New nodes in subreader: {diff}. Ignoring them.")
            nodes = set(nodes).intersection(self.nodes)
        new_out_nodes = list(set(self.out_nodes).intersection(nodes))
        new_in_keys = {k: v for k, v in self.in_key_transforms.items() if k in nodes}
        assert len(new_out_nodes) > 0, f"No gt nodes remaining when calling subreader. {self.out_nodes} and {nodes}"
        return NGCNpzReader(self.path, nodes, new_out_nodes, in_key_transforms=new_in_keys)

    def __getitem__(self, index: int):
        """Read the data for each node. Input nodes go in 'data', while output nodes in 'labels' (for training)"""
        data, labels = {}, {}
        first_key = self.in_key_transforms[self.nodes[0]]
        item_name = Path(self.in_files[first_key][index]).stem

        for node in self.nodes:
            node_key = self.in_key_transforms[node]
            this_item_name = Path(self.in_files[node_key][index]).stem
            assert item_name == this_item_name, f"Names differ: '{item_name}' vs '{this_item_name}'"
            item = self._read_node_data(node, index).astype(np.float32)
            if node in self.out_nodes:
                labels[node.name] = item
            else:
                data[node.name] = item
        return {"data": data, "labels": labels, "name": item_name}

    def __len__(self) -> int:
        first_key = list(self.in_key_transforms.values())[0]
        return len(self.in_files[first_key])

    def _build_dataset(self) -> Dict[str, List[Path]]:
        logger.debug2(f"Building dataset from: '{self.path}'")
        logger.debug2(f"Nodes: {self.nodes}")
        logger.debug2(f"GT Nodes: {self.out_nodes}")
        in_files = {}
        for node in self.nodes:
            dir_name = self.path / self.in_key_transforms[node.name]
            items = dir_name.glob("*.npz")
            items = natsorted([str(x) for x in items])
            in_files[self.in_key_transforms[node.name]] = items
        lens = [len(x) for x in in_files.values()]
        assert np.std(lens) == 0, f"Lens: {dict(zip(self.name_to_node.keys(), lens))}"
        assert len(in_files) > 0
        logger.debug(f"Found {lens[0]} images")
        assert lens[0] > 0, lens
        return in_files

    def _read_node_data(self, node: Node, index: int) -> np.ndarray:
        """Reads the npz data from the disk and transforms it properly"""
        node_in_key = self.in_key_transforms[node.name]
        item = load_npz(self.in_files[node_in_key][index])
        if hasattr(node, "transform_from_disk"):
            transformed_item = node.transform_from_disk(item)
        else:
            logger.debug2(f"Node '{node}' has no 'transform_from_disk' method. Using raw npz data.")
            transformed_item = item
        return transformed_item

    def __str__(self):
        f_str = "[NGC Npz Reader]"
        f_str += f"\n - Path: '{self.path}'"
        f_str += f"\n - Nodes ({len(self.nodes)}): {list(self.name_to_node)}"
        f_str += f"\n - Input Nodes ({len(self.in_nodes)}): {[x.name for x in self.in_nodes]}"
        f_str += f"\n - Output Nodes ({len(self.out_nodes)}): {[x.name for x in self.out_nodes]}"
        f_str += f"\n - Length: {len(self)}"
        return f_str

    def __repr__(self):
        return str(self)
