"""A Flax-based implementation for the Neural Net layers"""
from typing import Callable

from flax import linen as nn
from jax import lax
import jax
import jax.numpy as jnp


def factorized_glorot_normal(mean=1.0, stddev=0.1):
    """Initializes the parameters for a Factorized NN

    :param mean: _description_, defaults to 1.0
    :type mean: float, optional
    :param stddev: _description_, defaults to 0.1
    :type stddev: float, optional
    """

    def init(key, shape):
        key1, key2 = jax.random.split(key)
        w = nn.initializers.glorot_normal()(key1, shape)
        s = mean + nn.initializers.normal(stddev)(key2, (shape[-1], ))
        s = jnp.exp(s)
        v = w / s
        return s, v

    return init


class DenseLayer(nn.Module):

    features: int
    kernel_init: Callable = nn.initializers.glorot_normal()
    bias_init: Callable = nn.initializers.zeros

    @nn.compact
    def __call__(self, inputs):
        kernel = self.param(
            "kernel",
            self.kernel_init,  # Initialization function
            (inputs.shape[-1], self.features),
        )

        y = lax.dot_general(
            inputs,
            kernel,
            (((inputs.ndim - 1, ), (0, )), ((), ())),
        )
        bias = self.param("bias", self.bias_init, (self.features, ))

        return y + bias


class QResLayer(nn.Module):
    features: int
    kernel_init: Callable = nn.initializers.glorot_normal()
    bias_init: Callable = nn.initializers.zeros

    @nn.compact
    def __call__(self, inputs):
        kernel1 = self.param(
            "kernel1",
            self.kernel_init,  # Initialization function
            (inputs.shape[-1], self.features),
        )
        kernel2 = self.param(
            "kernel2",
            self.kernel_init,  # Initialization function
            (inputs.shape[-1], self.features),
        )
        y1 = lax.dot_general(
            inputs,
            kernel1,
            (((inputs.ndim - 1, ), (0, )), ((), ())),
        )
        y2 = lax.dot_general(
            inputs,
            kernel2,
            (((inputs.ndim - 1, ), (0, )), ((), ())),
        )
        bias = self.param("bias", self.bias_init, (self.features, ))

        return y1 + y1 * y2 + bias


class LLAAFLayer(nn.Module):
    features: int
    alpha_ratio: float = 10.0
    kernel_init: Callable = nn.initializers.glorot_normal()
    bias_init: Callable = nn.initializers.zeros

    @nn.compact
    def __call__(self, inputs):
        kernel = self.param(
            "kernel",
            self.kernel_init,  # Initialization function
            (inputs.shape[-1], self.features),
        )
        alpha = self.param(
            "alpha",
            lambda key, shape: nn.initializers.ones(key, shape) / self.
            alpha_ratio,  # Initialization function
            (1, ),
        )
        y = lax.dot_general(
            inputs,
            kernel,
            (((inputs.ndim - 1, ), (0, )), ((), ())),
        )
        bias = self.param("bias", self.bias_init, (self.features, ))

        return alpha * (y + bias)


class NLAAFLayer(nn.Module):
    features: int
    alpha_ratio: float = 10.0
    kernel_init: Callable = nn.initializers.glorot_normal()
    bias_init: Callable = nn.initializers.zeros

    @nn.compact
    def __call__(self, inputs):
        kernel = self.param(
            "kernel",
            self.kernel_init,  # Initialization function
            (inputs.shape[-1], self.features),
        )
        alpha = self.param(
            "alpha",
            lambda key, shape: nn.initializers.ones(key, shape) / self.
            alpha_ratio,  # Initialization function
            (self.features, ),
        )
        y = lax.dot_general(
            inputs,
            kernel,
            (((inputs.ndim - 1, ), (0, )), ((), ())),
        )
        bias = self.param("bias", self.bias_init, (self.features, ))

        return alpha * (y + bias)


class FactorizedDense(nn.Module):
    features: int

    @nn.compact
    def __call__(self, x):
        s, v = self.param("kernel", factorized_glorot_normal(),
                          (x.shape[-1], self.features))
        kernel = s * v
        bias = self.param("bias", nn.initializers.zeros, (self.features, ))
        y = jnp.dot(x, kernel) + bias
        return y


# layer_dict = {
#    "dense": DenseLayer,
#   "qres": QResLayer,
#   "llaaf": LLAAFLayer,
#   "nlaaf": NLAAFLayer,
#   "fact": FactorizedDense,
# }
