from dataclasses import dataclass

from eokulapi.Models import from_list, from_str


@dataclass
class AdditionalExam:
    """Additional exam model"""

    name: str | None
    """Name of the additional exam"""

    appeal: list
    """Appeal state of the additional exam"""

    result: list
    """Result of the additional exam"""
    location: list
    """Location of the additional exam"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to AdditionalExam object

        Args:
            obj (dict): Object to be converted

        Returns:
            AdditionalExam: AdditionalExam object that is converted from dict
        """
        name = from_str(obj.get("SinavAdi"))
        basv = from_list(list, obj.get("sinavBasvuruListesi"))
        sonuc = from_list(list, obj.get("sinavSonucListesi"))
        yer = from_list(list, obj.get("sinavYeriListesi"))
        return cls(name, basv, sonuc, yer)
