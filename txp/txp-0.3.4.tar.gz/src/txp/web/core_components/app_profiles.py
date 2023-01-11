import enum
from typing import List


class AppProfile(enum.Enum):
    def __new__(cls, *values):
        obj = object.__new__(cls)
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        obj.display_value = values[1]
        return obj

    """This enumeration defines the valid Application Profiles supported."""
    RESUMEN = 0, "Resumen"
    ANALYTICS = 1, "Análisis"
    CONFIGURATION = 2, "Configuración"

    def get_display_value(self) -> str:
        return self.display_value

    @classmethod
    def get_display_values(cls) -> List[str]:
        """Returns the List of display value strings for the profiles"""
        r = []
        for profile in cls:
            r.append(profile.display_value)
        return r
