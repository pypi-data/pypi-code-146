import copy
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import onnxruntime as ort

from selcol.runtime.interface import SelColInferencerBase


@dataclass
class OrtSelColInferencer(SelColInferencerBase):
    session_table: Dict[int, ort.InferenceSession]
    joint_names: List[str]
    eval_joint_indices: Optional[np.ndarray]  # int
    _context: Optional[np.ndarray]
    metadata_dict: Dict
    eps_numerical_grad: float = 1e-4

    @classmethod
    def load_from_path(
        cls, dir_path: Path, eval_joint_names: Optional[List[str]] = None
    ) -> "OrtSelColInferencer":
        dir_path = dir_path.expanduser()

        metadata_path = dir_path / "metadata.json"
        with metadata_path.open(mode="r") as f:
            json_dict = json.load(f)
        joint_names: List[str] = json_dict["joint_names"]

        session_table = {}
        for filepath in dir_path.iterdir():
            if filepath.name.endswith(".onnx"):
                match = re.search(r"\d+", filepath.name)
                assert match is not None
                n_batch = int(match.group())
                session = ort.InferenceSession(str(filepath))
                session_table[n_batch] = session

        eval_joint_indices: Optional[np.ndarray] = None
        if eval_joint_names is not None:
            eval_joint_indices = np.array([joint_names.index(name) for name in eval_joint_names])

        return cls(session_table, joint_names, eval_joint_indices, None, json_dict)

    def infer(self, q: np.ndarray, with_grad: bool = False) -> Tuple[float, np.ndarray]:
        assert q.ndim == 1
        if self.eval_joint_indices is not None:
            assert (
                self._context is not None
            ), "if you specified eval joints, you neeed specify context"

        if not with_grad:
            return self._infer_without_grad(q)
        else:
            return self._infer_with_grad(q)

    def _find_session_key(self, n_eval: int) -> int:
        batches = np.array(list(self.session_table.keys()))
        n_batch = np.min(batches[batches >= n_eval])
        return n_batch

    def _infer_without_grad(self, q: np.ndarray) -> Tuple[float, np.ndarray]:
        n_batch = self._find_session_key(1)
        session = self.session_table[n_batch]

        if self.eval_joint_indices is None:
            inp = q.reshape(n_batch, -1)
        else:
            assert self._context is not None
            inp = copy.deepcopy(self._context).reshape(1, -1)
            inp[0][self.eval_joint_indices] = q
        input_dict = {"x": inp.astype(np.float32)}
        out = session.run(None, input_dict)[0].item()
        return float(out), np.empty(0)

    def _infer_with_grad(self, q: np.ndarray) -> Tuple[float, np.ndarray]:
        # because we need to compute numerical gradient ...
        n_batch_required = 1 + self.eval_dof
        n_batch = self._find_session_key(n_batch_required)
        assert n_batch >= n_batch_required
        session = self.session_table[n_batch]

        if self.eval_joint_indices is None:
            inp = np.tile(q, (n_batch, 1))
            for i in range(self.dof):
                inp[i + 1, i] += self.eps_numerical_grad
            input_dict = {"x": inp.astype(np.float32)}
            out = session.run(None, input_dict)[0]
            f0 = out[0].item()
            f1s = out[1 : 1 + self.dof, 0]
            grad = (f1s - f0) / self.eps_numerical_grad
            return f0, grad
        else:
            assert self._context is not None
            q_all = copy.deepcopy(self._context)
            q_all[self.eval_joint_indices] = q
            inp = np.tile(q_all, (n_batch, 1))
            for i, idx in enumerate(self.eval_joint_indices):
                inp[i + 1, idx] += self.eps_numerical_grad
            input_dict = {"x": inp.astype(np.float32)}
            out = session.run(None, input_dict)[0]
            f0 = out[0].item()
            f1s = out[1:n_batch_required, 0]
            grad = (f1s - f0) / self.eps_numerical_grad
            return f0, grad
