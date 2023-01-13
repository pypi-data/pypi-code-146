import os

from fuzzywuzzy import fuzz


def ratio():
    mot_1 = (
        os.environ["DEFAULT_MOT_UN"]
        if "DEFAULT_MOT_UN" in os.environ
        else "conception_logicielle"
    )
    mot_2 = (
        os.environ["DEFAULT_MOT_DEUX"]
        if "DEFAULT_MOT_DEUX" in os.environ
        else "configuration"
    )
    return fuzz.ratio(mot_1, mot_2)
