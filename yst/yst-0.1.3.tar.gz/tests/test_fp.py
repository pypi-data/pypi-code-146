from yst.fp import *
from operator import add, mul


def foo(a, b, c):
    return [a, b, c]


assert bind(foo, 1, c=3)(2) == [1, 2, 3]
assert rbind(foo, 1, c=3)(2) == [2, 1, 3]

assert fst((1, 2)), 1
assert snd((1, 2)), 2

add1 = bind(add, 1)
mul3 = bind(mul, 3)
add1mul3 = compose(add1, mul3)
assert pipe(1, add1mul3) == 6

assert pipe(range(10),
            cmap(mul3),
            cfilter(lambda x: x % 2 == 0),
            list) == [6, 12, 18, 24, 30]
