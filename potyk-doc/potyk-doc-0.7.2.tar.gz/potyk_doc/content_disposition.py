import dataclasses
from typing import Dict
from urllib.parse import urlencode, quote

from potyk_doc.models import Mimetype


@dataclasses.dataclass
class ContentDisposition:
    filename: str
    mimetype: Mimetype = Mimetype.any

    @property
    def content_type(self):
        return self.mimetype.value

    @classmethod
    def docx(cls, filename):
        return cls(filename, Mimetype.docx)

    @classmethod
    def xlsx(cls, filename):
        return cls(filename, Mimetype.xlsx)

    @classmethod
    def pdf(cls, filename):
        return cls(filename, Mimetype.pdf)

    @classmethod
    def zip(cls, filename):
        return cls(filename, Mimetype.zip)

    @classmethod
    def guess(cls, filename):
        return cls(filename, Mimetype.guess(filename))

    @property
    def filename_encoded(self) -> str:
        """
        >>> ContentDisposition.xlsx('Отчет.xlsx').filename_encoded
        'filename=%D0%9E%D1%82%D1%87%D0%B5%D1%82.xlsx'
        """
        return urlencode({"filename": self.filename}, quote_via=quote)

    @property
    def header(self) -> str:
        """
        >>> ContentDisposition.xlsx('report.xlsx').header
        'attachment; filename=report.xlsx'
        """
        return f'attachment; {self.filename_encoded}'

    @property
    def header_dict(self) -> Dict[str, str]:
        """
        >>> ContentDisposition.xlsx('report.xlsx').header_dict
        {'Content-Disposition': 'attachment; filename=report.xlsx'}
        """
        return {'Content-Disposition': self.header}
