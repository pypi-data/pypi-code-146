import copy
import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional, Tuple

import flax.linen as fnn
import jax
import jax.numpy as jnp
import numpy as np

from selcol.runtime.interface import SelColInferencerBase


@dataclass
class JaxSelColInferencer(SelColInferencerBase):
    f: Callable[[np.ndarray], float]
    grad: Callable[[np.ndarray], np.ndarray]
    joint_names: List[str]
    eval_joint_indices: Optional[np.ndarray]  # int
    _context: Optional[np.ndarray]
    eps_numerical_grad: float = 1e-4

    @dataclass
    class JaxLinear:
        w: np.ndarray
        b: np.ndarray

        @classmethod
        def from_numpy(cls, w_: np.ndarray, b: np.ndarray):
            w = jax.numpy.transpose(w_, (1, 0))
            return cls(jnp.array(w), jnp.array(b))

        def __call__(self, x):
            return jnp.dot(x, self.w) + self.b

    @classmethod
    def load_from_path(
        cls, dir_path: Path, eval_joint_names: Optional[List[str]] = None
    ) -> "JaxSelColInferencer":
        dir_path = dir_path.expanduser()

        # joint stuff
        metadata_path = dir_path / "metadata.json"
        with metadata_path.open(mode="r") as f:
            json_dict = json.load(f)
        joint_names: List[str] = json_dict["joint_names"]

        eval_joint_indices: Optional[np.ndarray] = None
        if eval_joint_names is not None:
            eval_joint_indices = np.array([joint_names.index(name) for name in eval_joint_names])

        # load and parse flax model
        model_path = dir_path / "numpy_layers.pkl"

        with model_path.open(mode="rb") as f:
            numpy_layers = pickle.load(f)

        flax_layers = []
        for numpy_layer in numpy_layers:
            if numpy_layer["type"] == "linear":
                params = numpy_layer["params"]
                w = params["w"]
                b = params["b"]
                flax_layers.append(cls.JaxLinear.from_numpy(w, b))
            elif numpy_layer["type"] == "relu":
                flax_layers.append(fnn.relu)
            elif numpy_layer["type"] == "sigmoid":
                flax_layers.append(fnn.sigmoid)
        model = fnn.Sequential(flax_layers)

        # convert model to jit function
        dummy_input = jnp.empty((len(joint_names),))
        variables = model.init(jax.random.PRNGKey(0), dummy_input)
        f = jax.jit(lambda x: model.apply(variables, x).reshape(()))
        grad = jax.jit(jax.grad(f))
        f(dummy_input)  # jit compile
        grad(dummy_input)  # jit compile
        return cls(f, grad, joint_names, eval_joint_indices, None)

    def infer(self, q: np.ndarray, with_grad: bool = False) -> Tuple[float, np.ndarray]:
        if self.eval_joint_indices is None:
            tweak_indices = np.arange(self.dof)
        else:
            tweak_indices = self.eval_joint_indices

        if self._context is not None:
            q_all = copy.deepcopy(self._context)
            q_all[tweak_indices] = q
        else:
            q_all = q

        f0 = self.f(q_all)
        if not with_grad:
            return f0, np.empty(0)

        # if use jax grad
        use_jit_grad = False
        if use_jit_grad:
            gradval = self.grad(q_all)[tweak_indices]
        else:
            # numerical grad
            gradval = np.zeros(self.eval_dof)
            for i, idx in enumerate(tweak_indices):
                q_all_plus = copy.deepcopy(q_all)
                q_all_plus[idx] += self.eps_numerical_grad
                f1 = self.f(q_all_plus)
                gradval[i] = (f1 - f0) / self.eps_numerical_grad
        return f0, gradval
