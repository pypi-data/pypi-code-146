def bind(f, *args, **kwargs):
    def helper(a):
        return f(*args, a, **kwargs)
    return helper


def rbind(f, *args, **kwargs):
    def helper(a):
        return f(a, *args, **kwargs)
    return helper


def fst(t):
    return t[0]


def snd(t):
    return t[1]
