from dataclasses import dataclass

from eokulapi.Models import from_list
from eokulapi.Models.Document import Document


@dataclass
class DocumentContainer:
    """Document container model"""

    data: list[Document]
    """Document data as list of Document objects"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to DocumentContainer object

        Args:
            obj (dict): Object to be converted

        Returns:
            DocumentContainer: DocumentContainer object that is converted from dict
        """
        liste = from_list(Document.from_dict, obj.get("TumBelgeler"))
        return cls(liste)
