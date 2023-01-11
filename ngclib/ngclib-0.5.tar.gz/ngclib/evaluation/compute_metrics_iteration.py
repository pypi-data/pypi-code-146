"""Metrics for an entire iteration given an ngc dir, a graph cfg, predictions & gt"""
from pathlib import Path
from typing import Dict, List, Tuple
from tqdm import tqdm
from nwgraph import Node

from .node_metrics_loco import node_metrics_loco
from ..logger import logger
from ..graph_cfg import GraphCfg

def _str_metrics(y_dir: Path, gt_dir: Path, output_dir: Path, graph_cfg: GraphCfg) -> str:
    """summary for exporter"""
    f_str = "[Metrics for NGC model]"
    f_str += f"\n - Predictions Dir: '{y_dir}'"
    f_str += f"\n - GT Dir: '{gt_dir}'"
    f_str += f"\n - Output dir: '{output_dir}'"
    f_str += f"\n - Graph cfg: '{graph_cfg.path}'"
    f_str += f"\n - Output nodes: {graph_cfg.output_nodes}"
    return f_str

def _get_node_out_paths(node_name: str, y_dir: Path, output_dir: Path) -> Dict[Path, Path]:
    """Computes the output paths for a node"""
    out_paths = {}
    edges_dirs = list((y_dir / node_name / "edges").iterdir())
    vote_dir = y_dir / node_name / "vote"
    for edge_dir in edges_dirs:
        out_paths[output_dir / node_name / f"edges_{edge_dir.name}.csv"] = edge_dir
    if vote_dir.exists():
        out_paths[output_dir / node_name / "vote.csv"] = vote_dir
    return out_paths

def _validate_node_out_paths(out_paths: Path, gt_path: Path):
    """Validates that the output paths match (as counts) with the GT paths for all edge exports of a node"""
    assert gt_path.exists(), gt_path
    n_gt = len(list(gt_path.iterdir()))
    for _, in_path in out_paths.items():
        assert in_path.exists()
        n_in_path = len(list(in_path.iterdir()))
        assert n_in_path == n_gt, f"Differs. In: '{in_path}' ({n_in_path}) vs. \n GT: '{gt_path}' ({n_gt})"

def _compute_iteration_out_paths(y_dir: Path, gt_dir: Path, output_dir: Path,
                                 out_nodes: List[Node]) -> Tuple[Dict, Dict]:
    """Computes the output paths for an entire iteration of predictions"""
    nodes_out_paths = {}
    nodes_gt_paths = {}
    for node in out_nodes:
        out_paths = _get_node_out_paths(node.name, y_dir, output_dir)
        gt_path = gt_dir / node.name
        _validate_node_out_paths(out_paths, gt_path)
        nodes_out_paths[node.name] = out_paths
        nodes_gt_paths[node.name] = gt_path
    return nodes_out_paths, nodes_gt_paths

def compute_metrics_iteration(y_dir: Path, gt_dir: Path, output_dir: Path, graph_cfg: GraphCfg, nodes: List[Node],
                              batch_size: int, num_batches: int, n_cores: int, pbar: bool = False):
    """Main function. Computes the metrics of an entire iteration, for all output nodes"""
    logger.info(_str_metrics(y_dir, gt_dir, output_dir, graph_cfg))
    assert len(graph_cfg.output_nodes) > 0, f"There are no output nodes in the cfg (all nodes: {graph_cfg.nodes})"

    # Compute and validate the output paths
    out_nodes = [ [node for node in nodes if node.name == node_name][0] for node_name in graph_cfg.output_nodes]
    nodes_out_paths, nodes_gt_paths = _compute_iteration_out_paths(y_dir, gt_dir, output_dir, out_nodes)

    cnt = sum(len(nodes_out_paths[k].keys()) for k in nodes_out_paths.keys())
    pbar = tqdm(total=cnt) if pbar else None
    res = {}

    for node in out_nodes:
        logger.info(f"Exporting metrics for node '{node}'")
        node_dfs = {}
        out_paths = nodes_out_paths[node.name]
        gt_path = nodes_gt_paths[node.name]
        for node_out_path, y_path in out_paths.items():
            df = node_metrics_loco(y_path, gt_path, node, batch_size, num_batches, n_cores, display_info=False)
            node_dfs[node_out_path] = df
            node_out_path.parent.mkdir(exist_ok=True, parents=True)
            df.to_csv(node_out_path)
            if pbar:
                pbar.update()
        res[node.name] = node_dfs
    return res
