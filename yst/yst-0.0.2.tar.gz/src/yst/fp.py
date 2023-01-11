def bind(f, *args, **kwargs):
    def helper(a):
        return f(*args, a, **kwargs)
    return helper


def fst(t):
    return t[0]


def snd(t):
    return t[1]
