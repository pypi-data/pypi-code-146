import os
import sys
import GRANNY as granny

gn = granny.GRANNY()
fname = "test2/"
gn.setAction("extract", fname = fname, mode = 2)
gn.main()
