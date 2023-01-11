from yst.fp import *


def foo(a, b, c):
    return [a, b, c]


assert bind(foo, 1, c=3)(2), [1, 2, 3]
assert rbind(foo, 1, c=3)(2), [2, 1, 3]

assert fst((1, 2)), 1
assert snd((1, 2)), 2
