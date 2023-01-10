from enum import IntEnum


class MentalHealthRiskScore(IntEnum):
    """Enum class to classify the mental health risk"""
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class QualityErrorType(IntEnum):
    NONE = 0
    TOO_CLOSE = 1
    TOO_FAR = 2
    NOT_CENTERED = 3
    NO_CHEST = 4
    BAD_POSE = 5
    BAD_LIGHTING = 6
    NOT_ENOUGH_SKIN = 7
