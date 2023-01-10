"""Generated from lda_c_gombas.mpl."""

import jax
import jax.numpy as jnp
from jax.numpy import array as array
from jax.numpy import int32 as int32
from jax.numpy import nan as nan
from typing import Callable


def pol(r0, r1, params, p):
  t2 = jnp.cbrt(r0 + r1)
  t3 = 0.1e1 / t2
  t10 = jnp.log((t3 + 0.239e1) * t2)
  res = -0.357e-1 / (0.1e1 + 0.562e-1 * t3) - 0.311e-1 * t10
  return res

def unpol(r0, params, p):
  t1 = jnp.cbrt(r0)
  t2 = 0.1e1 / t1
  t9 = jnp.log((t2 + 0.239e1) * t1)
  res = -0.357e-1 / (0.1e1 + 0.562e-1 * t2) - 0.311e-1 * t9
  return res