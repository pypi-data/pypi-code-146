"""Generated from lda_c_wigner.mpl."""

import jax
import jax.numpy as jnp
from jax.numpy import array as array
from jax.numpy import int32 as int32
from jax.numpy import nan as nan
from typing import Callable


def pol(r0, r1, params, p):
  t2 = (r0 - r1) ** 2
  t3 = r0 + r1
  t4 = t3 ** 2
  t9 = jnp.cbrt(3)
  t11 = jnp.cbrt(0.1e1 / jnp.pi)
  t13 = jnp.cbrt(4)
  t14 = t13 ** 2
  t15 = jnp.cbrt(t3)
  res = (0.1e1 - t2 / t4) * params.a / (params.b + t9 * t11 * t14 / t15 / 0.4e1)
  return res

def unpol(r0, params, p):
  t1 = jnp.cbrt(3)
  t3 = jnp.cbrt(0.1e1 / jnp.pi)
  t5 = jnp.cbrt(4)
  t6 = t5 ** 2
  t7 = jnp.cbrt(r0)
  res = params.a / (params.b + t1 * t3 * t6 / t7 / 0.4e1)
  return res