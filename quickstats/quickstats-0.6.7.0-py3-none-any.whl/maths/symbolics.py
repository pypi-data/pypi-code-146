def get_coeff_dict(expr, *x, strict:bool=True, linear:bool=False):
    if strict and (set(expr.free_symbols) != set(x)):
        raise RuntimeError("supplied symbols and expression symbols mismatch")
    from sympy import Poly, Add, S
    collected = Poly(expr, *x).as_expr()
    i, d = collected.as_independent(*x, as_Add=True)
    rv = dict(i.as_independent(*x, as_Mul=True)[::-1] for i in Add.make_args(d))
    if i:
        assert 1 not in rv
        rv.update({S.One: i})
    if linear and (not set(rv.keys()).issubset(set(x))):
        raise RuntimeError("expression contains nonlinear terms")
    return rv