"""Generated from lda_c_rpa.mpl."""

import jax
import jax.numpy as jnp
from jax.numpy import array as array
from jax.numpy import int32 as int32
from jax.numpy import nan as nan
from typing import Callable


def pol(r0, r1, params, p):
  t1 = jnp.cbrt(3)
  t3 = jnp.cbrt(0.1e1 / jnp.pi)
  t4 = t1 * t3
  t5 = jnp.cbrt(4)
  t6 = t5 ** 2
  t8 = jnp.cbrt(r0 + r1)
  t10 = t6 / t8
  t11 = t4 * t10
  t13 = jnp.log(t11 / 0.4e1)
  res = 0.311e-1 * t13 - 0.48e-1 + 0.225e-2 * t4 * t10 * t13 - 0.425e-2 * t11
  return res

def unpol(r0, params, p):
  t1 = jnp.cbrt(3)
  t3 = jnp.cbrt(0.1e1 / jnp.pi)
  t4 = t1 * t3
  t5 = jnp.cbrt(4)
  t6 = t5 ** 2
  t7 = jnp.cbrt(r0)
  t9 = t6 / t7
  t10 = t4 * t9
  t12 = jnp.log(t10 / 0.4e1)
  res = 0.311e-1 * t12 - 0.48e-1 + 0.225e-2 * t4 * t9 * t12 - 0.425e-2 * t10
  return res