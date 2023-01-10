"""Generated from lda_c_lp96.mpl."""

import jax
import jax.numpy as jnp
from jax.numpy import array as array
from jax.numpy import int32 as int32
from jax.numpy import nan as nan
from typing import Callable


def pol(r0, r1, params, p):
  t2 = jnp.cbrt(r0 + r1)
  t5 = t2 ** 2
  res = params.C1 + params.C2 / t2 + params.C3 / t5
  return res

def unpol(r0, params, p):
  t1 = jnp.cbrt(r0)
  t4 = t1 ** 2
  res = params.C1 + params.C2 / t1 + params.C3 / t4
  return res