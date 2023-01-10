from base64 import b64decode
from binascii import Error
from dataclasses import dataclass

from correos_preregistro.errors import ErrorDecodingPDFLabel


@dataclass
class ResponsePreregistroEnvio:
    shipment_code: str
    label_file: str

    def get_pdf_label(self):
        try:
            return b64decode(self.label_file, validate=True)
        except Error:
            raise ErrorDecodingPDFLabel("PDF label not valid")
