"""Generated from mgga_xc_lp90.mpl."""

import jax
import jax.numpy as jnp
from jax.numpy import array as array
from jax.numpy import int32 as int32
from jax.numpy import nan as nan
from typing import Callable


def pol(r0, r1, s0, s1, s2, l0, l1, tau0, tau1, params, p):
  t3 = r0 + r1
  t4 = t3 ** 2
  t5 = jnp.cbrt(t3)
  t6 = t5 ** 2
  t11 = jnp.cbrt(r0)
  t12 = t11 ** 2
  t18 = (r0 - r1) / t3
  t20 = 0.1e1 / 0.2e1 + t18 / 0.2e1
  t21 = jnp.cbrt(t20)
  t22 = t21 ** 2
  t26 = jnp.cbrt(r1)
  t27 = t26 ** 2
  t32 = 0.1e1 / 0.2e1 - t18 / 0.2e1
  t33 = jnp.cbrt(t32)
  t34 = t33 ** 2
  res = -(0.80569 + 0.37655e-3 * (s0 + 0.2e1 * s1 + s2) / t6 / t4 - 0.37655e-3 * l0 / t12 / r0 * t22 * t20 - 0.37655e-3 * l1 / t27 / r1 * t34 * t32) / (0.1e1 / t5 + 0.40743e-2)
  return res

def unpol(r0, s0, l0, tau0, params, p):
  t1 = r0 ** 2
  t2 = jnp.cbrt(r0)
  t3 = t2 ** 2
  res = -(0.80569 + 0.37655e-3 * s0 / t3 / t1 - 0.37655e-3 * l0 / t3 / r0) / (0.1e1 / t2 + 0.40743e-2)
  return res