"""stuff regarding train set, inside the semisup algorithm"""
import os
from typing import List
from pathlib import Path
from natsort import natsorted

def find_intersection(dirs: List[List[str]]) -> List[str]:
    """Given a list of lists, find the intersection of those lists"""
    assert len(dirs) >= 1
    res = set(dirs[0])
    for _dir in dirs[1: ]:
        res = res.intersection(_dir)
    return natsorted(list(res))

def find_union(dirs: List[List[str]]) -> List[str]:
    """Given a list of lists, find the union of those lists"""
    assert len(dirs) >= 1
    res = set(dirs[0])
    for _dir in dirs[1: ]:
        res = res.union(_dir)
    return natsorted(list(res))

def make_iter1_data(dataset_path: Path, out_path: Path, node_names: List[str]):
    """Given a path to a dataset with potential holes, return the highest intersection of the given nodes"""
    files = [ [x.name for x in (dataset_path / node_name).iterdir()] for node_name in node_names ]
    common_files = find_intersection(files)
    for node_name in node_names:
        (out_path / node_name).mkdir(exist_ok=True, parents=True)
        for file_name in common_files:
            in_file = dataset_path / node_name / file_name
            out_file = out_path / node_name / file_name
            if not out_file.exists():
                os.symlink(in_file, out_file)
            else:
                assert out_file.is_symlink(), f"Out file must be symlink here, not a pseudolabel: '{out_file}'"
