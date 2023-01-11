from musiclang.generate.random_score import generate_random_score
from musiclang.core.library import *

import numpy as np
#np.random.seed(44)
DURATION = 32 * Q
NB_VOICES = 3
INSTS = ['french_horn__0', 'oboe__0', 'flute__0']
CANDIDATES_CHORD = [I % I.M, V % V.M, I % I.m, V % II.M]
score = generate_random_score(DURATION, INSTS, CANDIDATES_CHORD)
score.to_midi("locals/test.mid", tempo=60)