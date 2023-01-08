from enum import Enum


class Values(Enum):
    DRAFT = "DRAFT"
    RETURN = "RETURN"
    NO_SIGN = "NO_SIGN"
    AWAITING_SIGN_A = "Awaiting_sign_A"
    AWAITING_SIGN_B = "Awaiting_sign_B"
    AWAITING_SIGN_C = "Awaiting_sign_C"
    SIGN_A  = "Sign_A"
    SIGN_B = "Sign_B"
    SIGN_C = "Sign_C"



# IMP_NOTE:  THE DRAFT IS DEFAULT VALUE FOR A TRANSITION STARTED PACK 