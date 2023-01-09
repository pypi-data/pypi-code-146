import enum
import os.path
from typing import Tuple, NamedTuple


# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
# https://en.wikipedia.org/wiki/Media_type
class Mimetype(str, enum.Enum):
    text = 'text/plain'
    html = 'text/html'
    csv = 'text/csv'
    json = 'application/json'
    pdf = 'application/pdf'
    zip = 'application/zip'
    any = 'application/octet-stream'
    docx = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    xlsx = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    @classmethod
    def guess(cls, filename):
        """
        >>> Mimetype.guess('archive.zip')
        <Mimetype.zip: 'application/zip'>
        """
        _, ext = os.path.basename(filename).split('.')
        return cls.__members__[ext]


class DocumentType(str, enum.Enum):
    pdf = 'pdf'
    docx = 'docx'

    @property
    def mime_type(self):
        """
        >>> DocumentType.pdf.mime_type
        'application/pdf'
        """
        return Mimetype.__members__[self.value].value


FileData = bytes
FileName = str


class File(NamedTuple):
    """Файл - тьюпл из байтов и названия файла"""
    data: FileData
    name: FileName


HTMLStr = str
