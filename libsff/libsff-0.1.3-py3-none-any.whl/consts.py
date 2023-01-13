from enum import Enum


TYPES = {
    0: "Dialogue",
    1: "Square",
    2: "Thinking",
    3: "ST",
    4: "OT"
}


TYPES_TO_STR = {
    0: "(): ",
    1: "[]: ",
    2: r"{}: ",
    3: "ST: ",
    4: "OT: "
}


R_TYPES = {
    "Dialogue": 0,
    "Square": 1,
    "Thinking": 2,
    "ST": 3,
    "OT": 4
}


IMG = {
    0: "No",
    1: "Yes"
}


R_IMG = {
    "No": 0,
    "Yes": 1
}


class Out(Enum):
    """
    Output Types Enum (RAW, GZIP, LZMA, TXT)
    """
    RAW = 0
    GZIP = 1
    LZMA = 2
    TXT = 3
