from dataclasses import dataclass

from eokulapi.Models import from_float, from_list, from_str, month_to_int, str_to_float
from eokulapi.Models.Absenteeism import Absenteeism


@dataclass
class AbsenteeismContainer:
    """Absenteeism container model"""

    excused_count: float
    """Excused absence count"""
    not_excused_count: float
    """Not excused absence count"""
    by_month: dict[int, float]
    """Absence count by month"""
    data: list[Absenteeism]
    """Absenteeism data as list of Absenteeism objects"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to AbsenteeismContainer object

        Args:
            obj (dict): Object to be converted

        Returns:
            AbsenteeismContainer: AbsenteeismContainer object that is converted from dict
        """
        by_month: dict = {}
        ozurlu = str_to_float(obj.get("Ozurlu"))
        ozursuz = str_to_float(obj.get("Ozursuz"))

        for abs in obj.get("DevamsizlikGrafikler"):
            ay = from_str(abs.get("Ay"))
            gun = from_float(abs.get("GunSayisi"))
            ay_int = month_to_int(ay)
            by_month[ay_int] = gun

        liste = from_list(Absenteeism.from_dict, obj.get("DevamsizlikListesi"))
        return cls(ozurlu, ozursuz, by_month, liste)
