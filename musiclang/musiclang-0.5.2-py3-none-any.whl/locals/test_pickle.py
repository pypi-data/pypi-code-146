import pickle
from musiclang.core.library import *
from musiclang import *

with open('test.pickle', 'wb') as f:
    C = I % I.M
    print(C)
    pickle.dump(C, f)


with open('test.pickle', 'rb') as f:
    c = pickle.load(f)

