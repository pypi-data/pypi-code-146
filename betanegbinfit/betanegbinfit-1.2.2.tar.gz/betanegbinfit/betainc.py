# -*- coding: utf-8 -*-
"""
This module concerns mostly effective gradient-friendly computation of betainc
function.
"""
import jax.numpy as jnp
from jax.scipy.special import betaln
from jax.lax import cond
from jax import jit
from functools import partial


@partial(jit, inline=True)
def calc_a(p, q, f, n):
    a = f**2*(p**2*(p + 2*q - 2)**2/(16*(2*n + p - 2)**2) + (p - 1)*(p + 1)*(p + 2*q - 3)*(p + 2*q - 1)/(32*(2*n + p - 1)) - (p - 1)*(p + 1)*(p + 2*q - 3)*(p + 2*q - 1)/(32*(2*n + p - 3)) - 1/16)
    first = f * (q - 1) / (p + 1)
    a = a.at[0].set(first)
    return a


@partial(jit, inline=True)
def calc_b(p, q, f, n):
    fp = f * p /4
    return fp * (-(p + 2*q - 2) / (2 * n + p - 2) + (p + 2*q - 2) / (2*n + p)) +  f / 2 + 1


@partial(jit, inline=True)
def calc_ratio(p, q, f, n):
    return p**2/(-f**2*n**2 + f**2*n*q + f**2*n - f**2*q) + p*(2*f*n - f*q + 6*n - q - 5)/(-f**2*n**2 + f**2*n*q + f**2*n - f**2*q) + (6*f*n**2 - 4*f*n*q - 8*f*n + f*q**2 + 3*f*q + 11*n**2 - 5*n*q - 17*n + q**2 + 3*q + 6)/(-f**2*n**2 + f**2*n*q + f**2*n - f**2*q) + 12*n*(-n + q - 1)/(f*(-n + q)*(n - 1)*(n + 1)*(2*n + p)*(-n + q - 2)) + n*(n - 2)*(n - 1)*(f*q + n + 1)/(f**2*(-n + q)*(n + 1)*(q - 1)*(n + p - 1)) - (-n + q)*(-n + q - 1)*(-n + q + 1)*(f*q - 2*f - n + q - 2)/(f**2*(n - 1)*(q - 1)*(-n + q - 2)*(n + p + q - 2))


@partial(jit, static_argnums=(3,))
def _logbetainc(p, q, x, n=10):
    ns = jnp.arange(1.0, n + 1.0)
    f = x / (1.0 - x)
    an = calc_a(p, q, f, ns)
    bn = calc_b(p, q, f, ns)
    an, bn = bn, an
    b = betaln(p, q)
    res = p * jnp.log(x) + (q - 1.0) * jnp.log1p(-x) - jnp.log(p) - b
    c = 1.0
    d = 0.0
    for i in range(n):
        c = an[i] + bn[i] / c
        t = an[i] + bn[i] * d
        c = jnp.clip(c, a_min=1e-15)
        t = jnp.clip(t, a_min=1e-15)
        d = 1.0 / t
        res += jnp.log(jnp.abs(c)) - jnp.log(jnp.abs(t))
    res = jnp.clip(res, a_max=0.0)
    return res


@partial(jit, static_argnums=(3,))
def _betaincc2(p, q, x, n=10.0):
    ns = jnp.arange(1, n + 1)
    f = x / (1.0 - x)
    an = calc_a(p, q, f, ns)
    bn = calc_b(p, q, f, ns)
    an, bn = bn, an
    b = betaln(p, q)
    res = p * jnp.log(x) + (q - 1) * jnp.log1p(-x) - jnp.log(p) - b
    res = -jnp.expm1(res)
    c = 1.0
    d = 0.0
    for i in range(n):
        c = an[i] + bn[i] / c
        t = an[i] + bn[i] * d
        c = jnp.clip(c, a_min=1e-15)
        t = jnp.clip(t, a_min=1e-15)
        d = 1.0 / t
        res = res * (c / d) + (d - c) / d 
    res = jnp.clip(res, a_min=0.0, a_max=1.0)
    return res


@partial(jit, inline=True)
def _betainc(p, q, x):
    return jnp.exp(_logbetainc(p, q, x))


@partial(jit, inline=True)
def _betaincc(p, q, x):
    return -jnp.expm1(_logbetainc(q, p, 1.0 - x))


@partial(jit, inline=True)
def _logbetaincc(p, q, x):
    return jnp.log(_betaincc(p, q, x))


@jit
@jnp.vectorize
def logbetainc(p, q, x):
    alpha = p + 1.0
    beta = p + 0.25
    c = q <= alpha / x - beta
    return cond(c, _logbetainc, _logbetaincc, p, q, x)


@jit
@jnp.vectorize
def betainc(p, q, x):
    alpha = p + 1.0
    beta = p + 0.25
    c = q <= alpha / x - beta
    return cond(c, _betainc, _betaincc, p, q, x)
