"""NGCDir status and to json"""
from typing import Dict, List
from pathlib import Path
from datetime import datetime
import json
import numpy as np
from ..logger import logger

def ngcdir_status(ngcdir: "NGCDir") -> Dict:
    """ Gets the status of this ngcdir as a parsable dictionary. """

    res = {
        "brief": {
            "path": str(ngcdir.path),
            "num_iterations": ngcdir.num_iterations,
            "num_nodes": len(ngcdir.nodes),
            "num_edges": len(ngcdir.edges),
            "iteration_train_status": {i: f"{ngcdir.num_trained_edges(i)} / {len(ngcdir.edges)}"
                                       for i in range(1, ngcdir.num_iterations + 1)}
        },
        "graph_cfg": {
            "nodes": ngcdir.nodes,
            "edges": ngcdir.edges,
        },
        "iterations":  [_iteration_status(ngcdir, i + 1) for i in range(ngcdir.num_iterations)]
    }
    return res

def ngcdir_to_json(ngcdir: "NGCDir"):
    """Returns a json of the status"""
    return json.dumps(ngcdir_status(ngcdir), indent=2)

def _edge_metadata(ngcdir: "NGCDir", edge: str, iteration: int) -> Dict:
    models_dir: Path = ngcdir.path / f"iter{iteration}/models"
    ckpt_path = models_dir / edge / "checkpoints/model_best.ckpt"
    fit_metadata_path: Path = ckpt_path.parent.parent / "fit_metadata.json"
    if not fit_metadata_path.exists():
        return None
    metadata = json.load(open(fit_metadata_path, "r"))
    res = {}
    if "epoch_metrics" in metadata and "val_loss" in metadata["epoch_metrics"]:
        res["last_epoch"] = int(list(metadata["epoch_metrics"]["val_loss"].keys())[-1]) + 1
    if "fit_start_date" in metadata:
        res["fit_start"] = metadata["fit_start_date"]
    if "fit_end_date" in metadata:
        res["fit_end"] = metadata["fit_end_date"]
    if "fit_duration" in metadata:
        res["fit_duration"] = metadata["fit_duration"]
    return res

def _iteration_model_status(ngcdir: "NGCDir", iteration: int) -> Dict:
    """Get the iteration model status."""

    def _get_edges_status(ngcdir: "NGCDir", models_dir: Path) -> List:
        """Get the status of each edge"""
        if not models_dir.exists():
            return []
        edges = []
        for edge in ngcdir.edges:
            this_edge = {
                "name": edge, # ngc name
                "train": {
                    "status": ngcdir.is_edge_trained(edge, iteration),
                    "metadata": _edge_metadata(ngcdir, edge, iteration)
                }
            }
            edges.append(this_edge)
        return edges

    def _get_time_status(res: Dict) -> Dict:
        """Get the time status of the iteration, if can be computed from edges statuses"""
        if not (len(res["edges"]) > 0 and "train" in res["edges"][0] and "metadata" in res["edges"][0]["train"] and \
                res["edges"][0]["train"]["metadata"] is not None and \
                "fit_start" in res["edges"][0]["train"]["metadata"] and \
                "fit_end" in res["edges"][0]["train"]["metadata"]):
            return {}
        epoch = datetime(1900, 1, 1, 0, 0, 0, 0)
        # Keep only those edges that have metadata already computed
        edge_metas_d = {edge["name"]: edge["train"]["metadata"] for edge in res["edges"]}
        edge_metas_d = {e: {"fit_start": m["fit_start"], "fit_duration": m["fit_duration"]} \
            for e, m in edge_metas_d.items() if m is not None and "fit_start" in m and "fit_duration" in m}
        edge_names, edge_metas = list(edge_metas_d.keys()), edge_metas_d.values()
        edge_metas = [{
                        "fit_start": datetime.strptime(x["fit_start"], "%Y-%m-%d %H:%M:%S.%f"),
                        "fit_duration": datetime.strptime(x["fit_duration"], "%H:%M:%S.%f") - epoch
                      } for x in edge_metas]
        # compute earliest start and latest end. Use fit_start + duration, not fit_end, to account for in training ones
        current_ends = [e["fit_start"] + e["fit_duration"] for e in edge_metas]
        last_end_ix = np.argsort(current_ends)[-1]
        first_start_ix = np.argsort([e["fit_start"] for e in edge_metas])[0]
        return {
            "first_edge": edge_names[first_start_ix],
            "last_edge": edge_names[last_end_ix],
            "duration": str(current_ends[last_end_ix] - edge_metas[first_start_ix]["fit_start"]),
        }

    models_dir = ngcdir.path / f"iter{iteration}/models"
    res = {
        "edges": _get_edges_status(ngcdir, models_dir),
        "total_edges": len(ngcdir.edges),
        "trained_edges": ngcdir.num_trained_edges(iteration),
        "in_training_edges": sum(ngcdir.is_edge_trained(edge, iteration) == "training" for edge in ngcdir.edges),
        "iteration_trained": ngcdir.is_iteration_trained(iteration),
    }
    res["time_status"] = _get_time_status(res)

    return res

def _iteration_data_status(ngcdir: "NGCDir", iteration: int) -> Dict:
    """
    Returns a dict like this:
    {
        "node_1": {"supervised": 10, "semisupervised": 5}
        ...
        "node_k": {"supervised": 15, "semisupervised": 0}
    }

    Supervised data is supposed to be obtained as symbolic links (dir linker will link data from a separate dir)
    Semisupervised data, however, is generated by a pseudolabel algorithm, thus for the output nodes, it'll be
    composed of actual files, not symlinks.
    """
    data_dir = ngcdir.path / f"iter{iteration}/data"
    node_data_dirs = list(filter(lambda x: x.is_dir(), data_dir.iterdir()))
    if len(node_data_dirs) == 0:
        return {}
    all_npz_files: Dict[str, List] = {node_dir.name: list(node_dir.glob("*.npz")) for node_dir in node_data_dirs}
    all_supervised_files = {node: [x for x in all_npz_files[node] if x.is_symlink()] for node in all_npz_files}
    all_semisup_files = {node: [x for x in all_npz_files[node] if not x.is_symlink()] for node in all_npz_files}

    res = {node: {"supervised": len(all_supervised_files[node]),
                    "semisupervised": len(all_semisup_files[node])} for node in all_npz_files}
    for node in ngcdir.graph_cfg.input_nodes:
        if res[node]["semisupervised"] != 0:
            logger.warning(f"Input node '{node}' has semisupervised files. This might be a mistake.")
    return res


def _iteration_status(ngcdir: "NGCDir", iteration: int) -> Dict[str, Dict]:
    """Get the iteration status"""
    return {
        "data": _iteration_data_status(ngcdir, iteration),
        "models": _iteration_model_status(ngcdir, iteration)
    }
