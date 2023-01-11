"""semisupervised generic algorithm implementation"""
from typing import List, Dict
from pathlib import Path
import os
from natsort import natsorted
from tqdm import tqdm
from torch.utils.data import DataLoader
from nwgraph import Node
import torch as tr
import numpy as np

from ..logger import logger
from ..models import NGC
from ..readers import NGCNpzReader

def _copy_in_files_to_new_dir(data_path: Path, out_path: Path, in_nodes: List[Node]):
    """Copy all input nodes' files to the output dir"""
    all_files = natsorted([x.name for x in (data_path / in_nodes[0].name).iterdir()])
    for item in tqdm(all_files):
        for in_node in in_nodes:
            (out_path / in_node.name).mkdir(exist_ok=True, parents=True)
            in_file = data_path / in_node.name / item
            out_file = out_path / in_node.name / item
            if out_file.exists():
                continue
            os.symlink(in_file, out_file)
    logger.info(f"Copied all input node data to '{out_path}'")

def _all_out_files_exist(x: Dict[str, tr.Tensor], input_nodes: List[Node], output_nodes: List[Node],
                        out_path: Path, all_files_view: List[str]) -> bool:
    """Internal function to skip some computation by not generating previously generated pseudolabels"""
    mb = len(x[input_nodes[0]])
    for i in range(mb):
        for out_node in output_nodes:
            out_file = out_path / out_node.name / all_files_view[i]
            if not out_file.exists():
                return False
    return True

def _generate_pseudo_for_all_missing(graph: NGC, out_path: Path, batch_size: int):
    """Generate pseudolabels in that directory, assuming input nodes' data is there already"""
    # This code is ran after _copy_in_files_to_new_dir, so the reader below, which works only with GT input nodes, can
    # generate psueolabels for all these found inputs
    all_files = natsorted([x.name for x in (out_path / graph.input_nodes[0].name).iterdir()])
    reader = NGCNpzReader(out_path, nodes=graph.input_nodes, out_nodes=[])
    loader = DataLoader(reader, collate_fn=reader.collate_fn, batch_size=batch_size, shuffle=False)
    cnt = 0
    for item in tqdm(iter(loader)):
        x = item["data"]
        mb = len(x[graph.input_nodes[0]])
        if _all_out_files_exist(x, graph.input_nodes, graph.output_nodes, out_path, all_files[cnt: ]):
            continue
        with tr.no_grad():
            y = graph.forward(x)
        for in_node in graph.input_nodes:
            assert tr.allclose(x[in_node], y[in_node])
        for i in range(mb):
            for out_node in graph.output_nodes:
                (out_path / out_node.name).mkdir(exist_ok=True, parents=True)
                out_file = out_path / out_node.name / all_files[cnt]
                np_y = y[out_node][i].to("cpu").type(tr.float16).numpy()
                np_y = out_node.inverse_transform_to_disk(np_y)
                np.savez(out_file, np_y)
            cnt += 1

def _overwrite_potential_gt(data_path: Path, out_path: Path, in_nodes: List[Node], out_nodes: List[Node]):
    cnt = 0
    all_files = natsorted([x.name for x in (out_path / in_nodes[0].name).iterdir()])
    for item in all_files:
        for node in out_nodes:
            in_file = data_path / node.name / item
            out_file = out_path / node.name / item
            assert out_file.exists(), out_file
            if in_file.exists() and not out_file.is_symlink():
                os.unlink(out_file)
                os.symlink(in_file, out_file)
                cnt += 1
    logger.info(f"Out of {len(all_files) * len(out_nodes)} pseudolabels, {cnt} had GT, thus replaced.")

def pseudo_algo(graph: NGC, semisup_data_path: Path, out_path: Path, batch_size: int = 1):
    """
    Generates pseudolabels for a set of given inputs using the model, copying GT data from data_path to out_path.
    Parameters:
    graph: The NGC graph used to generate pseudolabels with
    data_path: The input data path, where the input nodes' GT data is copied from.
    out_path: The output path, where the input nodes' GT data and output nodes' pseudolabels are stored at
    """
    n_outputs = len(list((semisup_data_path / graph.input_nodes[0].name).iterdir()))
    logger.info(f"Got {n_outputs} * {len(graph.output_nodes)} out nodes to generate pseudolabels for.")
    # copy all the input data required for the output data
    _copy_in_files_to_new_dir(semisup_data_path, out_path, graph.input_nodes)
    # create a reader for the required output data and generate the new pseudolabels
    _generate_pseudo_for_all_missing(graph, out_path, batch_size)
    _overwrite_potential_gt(semisup_data_path, out_path, graph.input_nodes, graph.output_nodes)
