from dataclasses import dataclass


@dataclass
class CustomResponse:
    shipment_code: str
    label_file: str
