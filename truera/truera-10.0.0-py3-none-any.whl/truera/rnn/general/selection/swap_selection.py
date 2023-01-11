from enum import Enum


class SwapComparisons(Enum):
    NONE = 1
    TP_TO_FN = 2
    FN_TO_TP = 3
    TN_TO_FP = 4
    FP_TO_TN = 5
