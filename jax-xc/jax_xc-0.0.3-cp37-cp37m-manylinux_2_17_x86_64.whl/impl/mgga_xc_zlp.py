"""Generated from mgga_xc_zlp.mpl."""

import jax
import jax.numpy as jnp
from jax.numpy import array as array
from jax.numpy import int32 as int32
from jax.numpy import nan as nan
from typing import Callable


def pol(r0, r1, s0, s1, s2, l0, l1, tau0, tau1, params, p):
  t1 = jnp.cbrt(3)
  t3 = jnp.cbrt(0.1e1 / jnp.pi)
  t4 = t1 * t3
  t5 = jnp.cbrt(4)
  t6 = t5 ** 2
  t11 = r0 + r1
  t12 = t11 ** 2
  t13 = jnp.cbrt(t11)
  t14 = t13 ** 2
  t18 = jnp.cbrt(r0)
  t19 = t18 ** 2
  t25 = (r0 - r1) / t11
  t27 = 0.1e1 / 0.2e1 + t25 / 0.2e1
  t28 = jnp.cbrt(t27)
  t29 = t28 ** 2
  t32 = jnp.cbrt(r1)
  t33 = t32 ** 2
  t38 = 0.1e1 / 0.2e1 - t25 / 0.2e1
  t39 = jnp.cbrt(t38)
  t40 = t39 ** 2
  t52 = jnp.log(0.1e1 + 0.48849425066691677572e3 / t13)
  t57 = t1 ** 2
  res = -(0.207108 * t4 * t6 + 0.5387725e-2 * t4 * t6 * ((s0 + 0.2e1 * s1 + s2) / t14 / t12 / 0.8e1 - l0 / t19 / r0 * t29 * t27 / 0.8e1 - l1 / t33 / r1 * t40 * t38 / 0.8e1)) * (0.1e1 - 0.2047107e-2 * t52 * t13) * t57 / t3 * t5 * t13 / 0.3e1
  return res

def unpol(r0, s0, l0, tau0, params, p):
  t1 = jnp.cbrt(3)
  t3 = jnp.cbrt(0.1e1 / jnp.pi)
  t4 = t1 * t3
  t5 = jnp.cbrt(4)
  t6 = t5 ** 2
  t9 = r0 ** 2
  t10 = jnp.cbrt(r0)
  t11 = t10 ** 2
  t27 = jnp.log(0.1e1 + 0.48849425066691677572e3 / t10)
  t32 = t1 ** 2
  res = -(0.207108 * t4 * t6 + 0.5387725e-2 * t4 * t6 * (s0 / t11 / t9 / 0.8e1 - l0 / t11 / r0 / 0.8e1)) * (0.1e1 - 0.2047107e-2 * t27 * t10) * t32 / t3 * t5 * t10 / 0.3e1
  return res