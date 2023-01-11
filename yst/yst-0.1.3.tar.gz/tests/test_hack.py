import yst.hack
from yst.fp import *
from operator import add

l = [1, 2, 3]
assert l.size(), 3

assert l.map(bind(add, 1)).to_list() == [2, 3, 4]
