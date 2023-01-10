from dataclasses import dataclass
from datetime import date

from eokulapi.Models import from_float, from_str, month_to_int, str_to_date


@dataclass
class Absenteeism:
    """Absenteeism model"""

    date: date
    """Date of the absence"""
    count: float
    """Count of the absence as in the E-Okul"""
    reason: str
    """Reason of the absence"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to Absenteeism object

        Args:
            obj (dict): Object to be converted

        Returns:
            Absenteeism: Absenteeism object that is converted from dict
        """
        date_list = from_str(obj.get("Gun")).split()
        date_str = f"{date_list[0]:02};{month_to_int(date_list[1]):02};{date_list[2]}"
        date = str_to_date(date_str)

        count = from_float(obj.get("GunSayi"))
        reason = from_str(obj.get("Nedeni"))

        return cls(date, count, reason)
