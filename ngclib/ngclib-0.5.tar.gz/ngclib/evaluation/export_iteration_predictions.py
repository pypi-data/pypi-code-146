"""Exports the prediction in an iteration"""
from typing import Dict, List
from pathlib import Path
from lightning_module_enhanced import LightningModuleEnhanced
from tqdm import trange
from nwgraph import Node
import torch as tr
import numpy as np

from ..graph_cfg import GraphCfg
from ..ngcdir import NGCDir
from ..models import NGC
from ..logger import logger


def compute_out_files(paths: Dict, output_dir: Path, i: int) -> Dict[str, Path]:
    """Prepares the output file paths for one reader iteration"""
    out_files = {}
    for node in paths.keys():
        out_files[node] = {"edges": [], "vote": None}
        for edge in paths[node]:
            path = Path(f"{output_dir}/{node}/edges/{edge}/{i}.npz")
            out_files[node]["edges"].append(path)
        # selection
        vote_path = Path(f"{output_dir}/{node}/vote/{i}.npz")
        out_files[node]["vote"] = vote_path
    return out_files

# pylint: disable=unused-argument
def compute_out_dir_names(y: Dict, input_nodes: List, graph_cfg: GraphCfg) -> Dict:
    """Computes the name of the directories based on one prediction by splitting the message manually"""
    # TODO? use graph_cfg for naming
    paths = {}
    for node in y.keys():
        if str(node) in input_nodes:
            continue
        all_paths = tuple(y[node])[0].path[0].split("|")
        paths[node] = all_paths
        assert len(paths[node]) == tuple(y[node])[0].input.shape[0]
    return paths

def all_edge_files_exist(out_files: Dict) -> bool:
    """Returns true if all edge paths exist"""
    for _, values in out_files.items():
        edge_paths = values["edges"]
        for edge_path in edge_paths:
            if not edge_path.exists():
                return False
    return True

def all_vote_files_exist(out_files: Dict) -> bool:
    """Returns true if all vote paths exist"""
    for _, values in out_files.items():
        if not values["vote"].exists():
            return False
    return True

def should_skip(overwrite: bool, export_edges: bool, export_vote: bool, out_files: Dict) -> bool:
    """
    Checks if all paths are already exported and we don't want to overwrite. Speeds up export by a lot if partial
    exports were done before and we just want to continue.
    """
    if overwrite:
        return False
    if export_vote and export_edges:
        return all_edge_files_exist(out_files) and all_vote_files_exist(out_files)
    if export_vote and not export_edges:
        return all_vote_files_exist(out_files)
    if not export_vote and export_edges:
        return all_edge_files_exist(out_files)
    return None

def create_dirs(out_dir: Path, paths: Dict):
    """Creates the output directory structure for all output nodes"""
    if out_dir.exists():
        logger.info(f"Output directory '{out_dir}' already exists. The models might overwrite predictions.")

    out_dir.mkdir(parents=True, exist_ok=True)
    for k, v in paths.items():
        for edge_name in v:
            Path(out_dir / str(k) / "edges" / edge_name).mkdir(parents=True, exist_ok=True)
        Path(out_dir / str(k) / "vote").mkdir(parents=True, exist_ok=True)

def tensors_from_prediction(y_node: Dict):
    """Gets the tensor from a single prediction"""
    edge_tensors = tuple(y_node)[0].input[:, 0]
    vote_tensor = tuple(y_node)[0].output[0]
    return {"edges": edge_tensors, "vote": vote_tensor}

# pylint: disable=unused-argument
def identity(x: tr.Tensor, _: Node) -> tr.Tensor:
    """Identity function"""
    return x

def _export_str(ngc_dir: NGCDir, iteration: int, reader: "NGCNpzReader", output_path: Path, output_nodes: List[Node],
                input_nodes: List[Node], export_edges: bool, export_vote: bool, overwrite: bool) -> str:
    """Returns a string for the logger with this export"""
    f_str = "[Exporting predictions]"
    f_str += f"\n - NGC Dir: '{ngc_dir.path}'"
    f_str += f"\n - Dataset path: '{reader.path}'"
    f_str += f"\n - Output path: '{output_path}'"
    f_str += f"\n - Iteration: {iteration}"
    f_str += f"\n - Overwriting existing: {overwrite}"
    f_str += f"\n - Input nodes (GT): {input_nodes}. Exported nodes: {output_nodes}"
    f_str += f"\n - Exporting edges: {export_edges}. Exporting graph ensemble (vote): {export_vote}"
    return f_str

def export_iteration_predictions(model: NGC, ngc_dir: NGCDir, iteration: int, reader: "NGCNpzReader", output_path: Path,
                                 export_edges: bool = True, export_vote: bool = True,
                                 overwrite: bool = False, pbar: bool = True, debug: bool = True):
    """The main function that exports the prediction of an iteration for all output nodes"""
    assert ngc_dir.num_iterations >= iteration, f"Total iterations: {ngc_dir.num_iterations} vs {iteration}"
    assert ngc_dir.is_iteration_trained(iteration), f"Iteration {iteration} is not fully trained"
    assert export_vote or export_edges, "At least one must be set!"
    logger.info(_export_str(ngc_dir, iteration, reader, output_path, model.output_nodes, model.input_nodes,
                            export_edges, export_vote, overwrite))

    logger.info(reader)

    model.load_all_edges(weights_dir=ngc_dir.all_data_dirs(iteration + 1)["models"][iteration])
    lme_model = LightningModuleEnhanced(model)

    # Setup stuff based on first prediction
    x = {k: reader[0]["labels"][k][None] for k in model.input_nodes}
    y = lme_model.np_forward(x)
    paths = compute_out_dir_names(y, model.input_nodes, ngc_dir.graph_cfg)
    create_dirs(output_path, paths)

    n = 5 if debug else len(reader)
    out_files = [compute_out_files(paths, output_path, i) for i in range(n)]
    _range = trange(n) if pbar else range(n)
    for i in _range:
        if should_skip(overwrite, export_edges, export_vote, out_files[i]):
            continue
        x = {k: reader[i]["labels"][k][None] for k in model.input_nodes}
        y = lme_model.np_forward(x)
        y = {k: y[k] for k in model.output_nodes}
        y = {k: tensors_from_prediction(y[k]) for k in model.output_nodes}

        for node in y.keys():
            y_node = y[node]
            paths_node = out_files[i][node]
            if export_edges:
                y_node_edges = y_node["edges"].numpy()
                paths_node_edges = paths_node["edges"]
                for path, y_edge in zip(paths_node_edges, y_node_edges):
                    if path.exists() and not overwrite:
                        continue
                    res = node.inverse_transform_to_disk(y_edge)
                    np.savez(path, res)
            if export_vote:
                y_node_vote = node.inverse_transform_to_disk(y_node["vote"].numpy())
                if paths_node["vote"].exists() and not overwrite:
                    continue
                np.savez(paths_node["vote"], y_node_vote)
    logger.info(f"Finished exporting at '{output_path}'.")
