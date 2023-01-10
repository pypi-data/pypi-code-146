"""Generated from lda_xc_1d_ehwlrg.mpl."""

import jax
import jax.numpy as jnp
from jax.numpy import array as array
from jax.numpy import int32 as int32
from jax.numpy import nan as nan
from typing import Callable


def pol(r0, r1, params, p):
  t1 = r0 + r1
  t3 = t1 ** 2
  t6 = t1 ** params.alpha
  res = (params.a2 * t1 + params.a3 * t3 + params.a1) * t6
  return res

def unpol(r0, params, p):
  t1 = r0 ** 2
  t5 = r0 ** params.alpha
  res = (params.a2 * r0 + params.a3 * t1 + params.a1) * t5
  return res