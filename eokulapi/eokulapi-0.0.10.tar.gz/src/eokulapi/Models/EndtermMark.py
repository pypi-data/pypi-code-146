from dataclasses import dataclass

from eokulapi.Models import from_str, str_to_float


@dataclass
class EndtermMark:
    """Endterm mark model"""

    academic_year: str
    """Academic year of the mark"""
    grade: str
    """Grade of the mark"""
    endterm_mark: float
    """Endterm mark"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to EndtermMark object

        Args:
            obj (dict): Object to be converted

        Returns:
            EndtermMark: EndtermMark object that is converted from dict
        """
        yil = from_str(obj.get("OGRETIMYILI"))
        sinif = from_str(obj.get("SINIF"))
        yilsonunot = str_to_float(obj.get("YILSONUNOTU"))
        return cls(yil, sinif, yilsonunot)
