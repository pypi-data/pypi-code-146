from musiclang.analyze.voice_separation import *


# TODO : BEAM Size (store only top n proba for each step in case of backtracking)
# TODO : Order in exploration : Explore only MAX orders solutions for evaluation
# TODO : Note generator : Generate incoming notes as note list that have same onset time
# TODO : Check overlap function to constraint candidates space

S = [
    [[2, 3, 50]],
    [[0, 1, 56], [1, 2, 55]],
    [[0, 1, 60], [1, 2, 62], [2, 3, 64]],
]

n1 = [[3, 4, 50], [3, 4, 60]]
w1 = [1, -3]

n2 = [[3, 4, 50], [3, 4, 60]]
w2 = [1, 3]

proba1 = P_T(S, n1, w1)
proba2 = P_T(S, n2, w2)

print(proba1, proba2)


from pdb import set_trace; set_trace()