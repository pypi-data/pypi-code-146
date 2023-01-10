"""Generated from lda_x_sloc.mpl."""

import jax
import jax.numpy as jnp
from jax.numpy import array as array
from jax.numpy import int32 as int32
from jax.numpy import nan as nan
from typing import Callable


def pol(r0, r1, params, p):
  t1 = params.b + 0.1e1
  t5 = r0 + r1
  t6 = t5 ** params.b
  t9 = (r0 - r1) / t5
  t10 = 0.1e1 + t9
  t12 = p.zeta_threshold ** t1
  t13 = t10 ** t1
  t14 = jnp.where(t10 <= p.zeta_threshold, t12, t13)
  t15 = 0.1e1 - t9
  t17 = t15 ** t1
  t18 = jnp.where(t15 <= p.zeta_threshold, t12, t17)
  res = -params.a / t1 * t6 * (t14 + t18) / 0.2e1
  return res

def unpol(r0, params, p):
  t1 = params.b + 0.1e1
  t5 = r0 ** params.b
  t7 = p.zeta_threshold ** t1
  t8 = jnp.where(0.1e1 <= p.zeta_threshold, t7, 1)
  res = -params.a / t1 * t5 * t8
  return res