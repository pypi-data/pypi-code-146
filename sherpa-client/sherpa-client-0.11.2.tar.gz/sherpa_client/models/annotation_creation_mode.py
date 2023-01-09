from enum import Enum


class AnnotationCreationMode(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    UNDEFINED = "undefined"

    def __str__(self) -> str:
        return str(self.value)
