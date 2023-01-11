def bind(f, *args, **kwargs):
    return lambda a: f(*args, a, **kwargs)


def rbind(f, *args, **kwargs):
    return lambda a: f(a, *args, **kwargs)


def fst(t):
    return t[0]


def snd(t):
    return t[1]


def cmap(f):
    "curryed map"
    return lambda l: map(f, l)


def cfilter(f):
    "curryed filter"
    return lambda l: filter(f, l)


def pipe(v, *args):
    for f in args:
        v = f(v)
    return v


def compose(*args):
    return lambda v: pipe(v, *args)
