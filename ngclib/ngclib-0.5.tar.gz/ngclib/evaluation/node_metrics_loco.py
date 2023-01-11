"""Module that handles the evaluation of the metrics of one (loco) node and one full iteration (all output nodes)"""

from typing import List, Dict, Tuple, Optional, Union
from pathlib import Path
from functools import reduce
import torch as tr
import numpy as np
import pandas as pd
from pool_resources import PoolResources, TorchResource
from nwgraph import Node
from nwutils.functions import map_list
from nwutils.torch import tr_get_data
from nwutils.path import get_files_from_dir
from ngclib.utils import load_npz

from ..logger import logger

def _get_metrics(y: tr.Tensor, gt: tr.Tensor, node: Node, criterion: bool = False) -> Dict:
    """For a particular node and a set of y, gt results, return the metrics. If criterion is true, return loss, too"""
    assert hasattr(node, "offline_metrics"), node

    res = {}
    if criterion:
        res["criterion"] = node.node_criterion(y, gt)
    for metric_name, metric_fn in node.offline_metrics.items():
        res[metric_name] = metric_fn(y, gt)
    logger.debug2(f"Got metrics for this batch y={y.shape} gt={gt.shape}")
    return res

def _format_metrics(res):
    """Nicely formats the results as strings from floats by rounding"""
    if isinstance(res, (list, tuple)):
        return [_format_metrics(x) for x in res]
    # pylint: disable=comparison-with-itself
    if res != res:
        return res
    if isinstance(res, int):
        return res
    if isinstance(res, tr.Tensor):
        assert len(res.shape) in (0, 1)
        res = res.item()
    assert isinstance(res, float)
    assert res >= 0
    if res < 1:
        return round(res, 6)
    if res < 10:
        return round(res, 5)
    return round(res, 4)

def _get_batches(index, batch_size, num_batches, seed: int = 42):
    """Splits the entire index in chunks of batch_size. If num_batches is set, also it gives us first batches only"""
    if seed is not None:
        np.random.seed(seed)
        index = np.random.permutation(index)
    num_chunks = len(index) // batch_size + (len(index) % batch_size != 0)
    split_data = np.array_split(index, num_chunks)
    if num_batches is not None:
        assert 1 <= num_batches <= len(split_data)
        split_data = split_data[0 : num_batches]
    return split_data

def _batch_res(items):
    y_paths_batch, gt_paths_batch, get_data_from_paths_fn, node = items
    y, gt = get_data_from_paths_fn(y_paths_batch, gt_paths_batch, node)
    metrics = _get_metrics(y, gt, node)
    return metrics

def _tr_np_list(x):
    device = tr.device("cuda") if tr.cuda.is_available() else tr.device("cpu")
    res = tr.stack(tr_get_data(list(x))).to(device)
    res = res.type(tr.float32) if tr.dtype == tr.float16 else res
    return res

def get_data_from_paths(y_paths: List[Path], gt_paths: List[Path], node: Node) -> Tuple[tr.Tensor, tr.Tensor]:
    """Given two list of paths of identical size, return the data after transform"""
    assert len(y_paths) == len(gt_paths), f"{len(y_paths)} vs {len(gt_paths)}"
    assert len(y_paths) > 0
    logger.debug2(f"Got {len(y_paths)} paths for node {node}")
    if y_paths[0].name != gt_paths[0].name:
        logger.warning("Names mismatch, probably random seeds are not equal, be careful.")

    y = _tr_np_list(map_list([load_npz, node.transform_from_disk], y_paths))
    gt = _tr_np_list(map_list([load_npz, node.transform_from_disk], gt_paths))
    assert len(y) == len(gt)

    logger.debug2(f"Stacked tensors to shape: pred={y.shape} and gt={gt.shape}")
    return y, gt

def _str_metrics_loco(y_paths: List[Path], gt_paths: List[Path], node: Node,
                      batch_size: int, num_batches: int, n_cores: int) -> str:
    f_str = "[Node metrics loco]"
    f_str += f"\n - GT path: '{gt_paths[0].parent}' (total: {len(gt_paths)})"
    f_str += f"\n - Prediction path: '{y_paths[0].parent}' (total: {len(y_paths)})"
    f_str += f"\n - Node name: '{node}'"
    f_str += f"\n - Batch size: {batch_size}"
    f_str += f"\n - Num batches: {num_batches}"
    f_str += f"\n - Num cores: {n_cores}"
    f_str += f"\n - CUDA: {tr.cuda.is_available()}"
    return f_str

def node_metrics_loco(y_paths: Union[Path, List[Path]], gt_paths: Union[Path, List[Path]],
                      node: Node, batch_size: int = 1, num_batches: Optional[int] = None,
                      n_cores: int = 0, display_info: bool = True) -> pd.DataFrame:
    """For a directory of predictions and a directory of gts, return the per-item metrics"""
    assert batch_size > 0 and (num_batches is None or num_batches > 0) and n_cores >= 0
    if isinstance(y_paths, Path):
        logger.debug("Prediction path is a directory. Using get_files_from_dir with *.npz pattern.")
        y_paths: List[Path] = get_files_from_dir(y_paths, pattern="*.npz")
    if isinstance(gt_paths, Path):
        logger.debug("GT path is  adirectory. Using get_files_from_dir with *.npz pattern.")
        gt_paths: List[Path] = get_files_from_dir(gt_paths, pattern="*.npz")
    assert len(y_paths) == len(gt_paths), f"{len(y_paths)} vs {len(gt_paths)}"
    if display_info:
        logger.info(_str_metrics_loco(y_paths, gt_paths, node, batch_size, num_batches, n_cores))
    indexes = np.arange(len(y_paths))
    batches = _get_batches(indexes, batch_size, num_batches, seed=None)

    # Split for parallel call
    y_paths_batch = [y_paths[batch] for batch in batches]
    gt_paths_batch = [gt_paths[batch] for batch in batches]
    get_data = [get_data_from_paths for _ in batches]
    node_for_each_batch = [node for _ in batches]
    zipped = list(zip(y_paths_batch, gt_paths_batch, get_data, node_for_each_batch))

    n_cores = min(len(batches), n_cores)
    device = "cuda" if tr.cuda.is_available() else "cpu"
    resources = [TorchResource(f"{device}:{i}") for i in range(n_cores)]
    pool = PoolResources(resources, timeout=1, pbar=True)
    pool_res = pool.map(_batch_res, zipped)
    # pool_res = [f_batch_res(x) for x in tqdm(zipped)]

    # Combine results
    initializer = {k: [] for k in node.offline_metrics.keys()}
    metrics = reduce(lambda d1, d2: {k1: (v1 + v2) for (k1, v1), (k2, v2) in zip(d1.items(), d2.items())},
                     pool_res, initializer)

    indexes = reduce(np.append, batches, []).astype(int)
    str_metrics = {k: _format_metrics(v) for k, v in metrics.items()}
    df = pd.DataFrame(str_metrics, index=indexes)
    return df
