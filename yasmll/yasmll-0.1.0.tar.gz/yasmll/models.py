from typing import Callable, Any, List, Tuple
from jax import numpy as jnp, random
from flax import linen as nn
import jax

import yasmll as yl


class InputEncoding:
    def __init__(
        self,
        encoding_type: str = None,
        dims: Tuple[int, int] = (1, 1),
        ff_freq: float = 5.0,
        num_fe: int = 4,
        rng_seed: int = 0,
    ):
        """Input encoding class.

        Args:
            encoding_type (str): encoding_type
            dims (Tuple[int, int]): dims
            ff_freq (float): ff_freq
            num_fe (int): num_fe
            rng_seed (int): rng_seed
        """
        self.encoding_type = encoding_type
        self.ff_freq = ff_freq
        self.num_fe = num_fe
        self.rng_key = random.PRNGKey(rng_seed)
        self.dims = dims
        self.encoding_coeffs = self.init_encoding_coeffs()

    def fourier_features_encoding(self, x: jnp.ndarray, w: jnp.ndarray) -> jnp.ndarray:
        """fourier_features_encoding.

        Args:
            x (jnp.ndarray): The inputs vector.
            w (jnp.ndarray): The encoding coefficients.

        Returns:
            jnp.ndarray: The encoded inputs.
        """
        return jnp.hstack([jnp.sin(jnp.dot(x, w)), jnp.cos(jnp.dot(x, w))])

    def features_expansion_encoding(self, x: jnp.ndarray, w: jnp.ndarray) -> jnp.ndarray:
        return jnp.hstack([x] + [f(a * x) for a in w for f in (jnp.cos, jnp.sin)])

    def init_encoding_coeffs(
        self,
    ):
        if self.encoding_type == "ff":
            return self.ff_freq * random.normal(self.rng_key, (self.dims[0], self.dims[1] // 2))
        elif self.encoding_type == "fe":
            return jnp.linspace(jnp.pi, self.num_fe * jnp.pi, self.num_fe)
        else:
            return None

    def __call__(self, x):
        """__call__.

        Args:
            x: The inputs vector.
        """
        if self.encoding_type == "ff":
            return self.fourier_features_encoding(x, self.encoding_coeffs)
        elif self.encoding_type == "fe":
            return self.features_expansion_encoding(x, self.encoding_coeffs)
        else:
            return x


class NeuralNet(nn.Module):
    input_dim: int = 2
    hidden_dim: int = 10
    output_dim: int = 1
    num_layers: int = 3
    layers_type: nn.Module = yl.layers.DenseLayer
    lb: jnp.ndarray = jnp.asarray([0.0, 0.0])
    ub: jnp.ndarray = jnp.asarray([1.0, 1.0])
    encoding_type: str = None
    ff_freq: float = 5.0
    num_fe: int = 4
    activation_fn: Callable = jax.nn.tanh

    def setup(
        self,
    ) -> None:
        # Build the list of neurons in each layer
        self.layers_list = [self.input_dim] + self.num_layers * [self.hidden_dim] + [self.output_dim]
        # Initialize the input encoding.
        self.input_encoding_fn = InputEncoding(
            encoding_type=self.encoding_type,
            ff_freq=self.ff_freq,
            num_fe=self.num_fe,
            dims=(self.layers_list[0], self.layers_list[1]),
        )

    @nn.compact
    def __call__(self, *inputs) -> jnp.ndarray:
        x = 2.0 * (jnp.stack(inputs) - self.lb) / (self.ub - self.lb) - 1.0
        x = self.input_encoding_fn(x)

        for idl, features in enumerate(self.layers_list[1:]):
            x = self.layers_type(features=features, name=f"layer_{idl}")(x)
            if idl != len(self.layers_list) - 1:
                x = self.activation_fn(x)

        x = x.flatten()
        return self.ansatz_fn(inputs, x)

    def ansatz_fn(self, inputs, outputs):
        return outputs


class ScalarDeepONet(NeuralNet):
    input_dims: Dict[str, int] = {"branch": 10, "trunk": 3}
    hidden_dim: Dict[str, int] = {"branch": 10, "trunk": 3}
