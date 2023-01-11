"""NGCDir implementation"""
from pathlib import Path
from typing import List, Dict, Tuple, Union

from .ngcdir_status import ngcdir_to_json, ngcdir_status
from ..graph_cfg import GraphCfg
from ..models import build_model_type

class NGCDir:
    """
    Generic ngc dir analysis class. It should be able to tell us what edges are trained, for how many iterations and
    other analysis stuff like this.
    """
    def __init__(self, path: Path, graph_cfg: GraphCfg):
        self.path = Path(path).absolute()
        self.graph_cfg = GraphCfg(graph_cfg) if isinstance(graph_cfg, (str, Path, dict)) else graph_cfg
        self.graph_type = build_model_type(self.graph_cfg.cfg["NGC-Architecture"])

        assert self.path.exists(), self.path
        assert self.graph_cfg is not None
        assert len(self.graph_cfg.edges) > 0, "No edges"

    @property
    def nodes(self) -> Dict[str, List[str]]:
        """Gets the nodes, types and names of this ngc dir"""
        res = {}
        for node_type, node_name in zip(self.graph_cfg.node_types, self.graph_cfg.node_names):
            res[node_name] = {"type": node_type, "input_node": node_name in self.graph_cfg.input_nodes}
        return res

    @property
    def edges(self) -> List[Tuple[str]]:
        """Get the list of edges from the graph cfg"""
        return self.graph_cfg.edges

    @property
    def num_iterations(self) -> int:
        """Gets the available iterations of this ngc dir"""
        all_dirs = list(filter(lambda x: x.is_dir() and x.name.startswith("iter"), self.path.iterdir()))
        return len(all_dirs)

    @property
    def status(self) -> Dict:
        """Gets the status of the ngcdir (iteration model/data status)"""
        return ngcdir_status(self)

    def is_edge_trained(self, edge: str, iteration: int) -> Union[bool, str]:
        """Whether an edge given as edge string is trained (by looking for the checkpoint). TODO: partial train"""
        models_dir = self.path / f"iter{iteration}/models"
        ckpt_path = models_dir / edge / "checkpoints/model_best.ckpt"
        # If model_best.ckpt exists, it is fully trained
        if ckpt_path.exists():
            return "finished"
        # If the parent directory doesn't exist, training hasn't started yet
        if not ckpt_path.parent.exists():
            return "not trained"
        # Parent directory exists, but no model_best => it is currently training.
        fit_metadata_path = ckpt_path.parent.parent / "fit_metadata.json"
        if not fit_metadata_path.exists():
            return "not trained"
        return "training"

    def is_iteration_trained(self, iteration: int) -> bool:
        """Returns true if all edges of the defined graph cfg are trained in this ngc dir"""
        models_dir = self.path / f"iter{iteration}/models"
        if not models_dir.exists():
            return False
        edge_dirs = [x for x in models_dir.iterdir() if x.is_dir()]
        return self.num_trained_edges(iteration) == len(edge_dirs)

    def num_trained_edges(self, iteration: int) -> int:
        """For a given iteration, return the number of trained edges"""
        models_dir = self.path / f"iter{iteration}/models"
        if not models_dir.exists():
            return 0
        cnt = 0
        for edge_dir in self.edges:
            if (models_dir / edge_dir / "checkpoints/model_best.ckpt").exists():
                cnt += 1
        return cnt

    def to_json(self):
        """Gets the status as a json object"""
        return ngcdir_to_json(self)

    def __str__(self) -> str:
        iter_status = {i: f"{self.num_trained_edges(i)}/{len(self.edges)}" for i in range(1, self.num_iterations + 1)}
        return f"[NGCDir] Path: '{self.path}'. Num iterations: {self.num_iterations}. " \
               f"Node: {len(self.nodes)}. Edges: {len(self.edges)}. Iteration status: {iter_status}."
