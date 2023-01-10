from dataclasses import dataclass

from eokulapi.Models import from_list
from eokulapi.Models.EndtermMark import EndtermMark


@dataclass
class EndtermMarkContainer:
    """Endterm mark container model"""

    data: list[EndtermMark]
    """Endterm mark data as list of EndtermMark objects"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to EndtermMarkContainer object

        Args:
            obj (dict): Object to be converted

        Returns:
            EndtermMarkContainer: EndtermMarkContainer object that is converted from dict
        """
        liste = from_list(EndtermMark.from_dict, obj.get("YilSonuNotListesi"))

        return cls(liste)
