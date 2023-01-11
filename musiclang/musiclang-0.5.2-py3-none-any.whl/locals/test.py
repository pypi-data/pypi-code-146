from musiclang.core.library import *


melody = s4 + s5.mm + s6.mm + s0.o(1) + s6.aeolian + s5.aeolian + s4
melody = s0 + s1 + s2 + s3 + s4 + s5 + s6 + s0.o(1) + r
melody = melody.mm + melody.m + melody.dorian

score = (V % I.m)(piano__0=melody).mf

score.to_midi('locals/test.mid')

print(score)