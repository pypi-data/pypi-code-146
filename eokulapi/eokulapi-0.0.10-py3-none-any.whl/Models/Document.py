from dataclasses import dataclass

from eokulapi.Models import from_str


@dataclass
class Document:
    """Document model"""

    doc_type: str
    """Type of the document"""
    term: str
    """Term of the document"""
    grade: str
    """Grade of the document"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to Document object

        Args:
            obj (dict): Object to be converted

        Returns:
            Document: Document object that is converted from dict
        """
        tur = from_str(obj.get("BelgeTuru"))
        donem = from_str(obj.get("Donemi"))
        sinif = from_str(obj.get("Sinifi"))
        return cls(tur, donem, sinif)
