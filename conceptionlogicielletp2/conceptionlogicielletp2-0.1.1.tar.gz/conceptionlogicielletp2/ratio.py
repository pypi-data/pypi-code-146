import os

from fuzzywuzzy import fuzz


def ratio():
    mot_1 = (
        os.environ["MOT_UN"]
        if "MOT_UN" in os.environ
        else "conception_logicielle"
    )
    mot_2 = (
        os.environ["MOT_DEUX"]
        if "MOT_DEUX" in os.environ
        else "configuration"
    )
    return fuzz.ratio(mot_1, mot_2)
