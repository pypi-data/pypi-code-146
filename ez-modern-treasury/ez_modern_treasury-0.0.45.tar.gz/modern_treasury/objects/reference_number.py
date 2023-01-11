from dataclasses import dataclass

class ReferenceNumberObjectType:
    PAYMENT_REFERENCE = "payment_reference"


@dataclass
class ReferenceNumber:
    id: str
    object: str # "payment_reference"
    live_mode : bool
    created_at: str # "2022-08-03T16:06:43Z"
    updated_at: str # "2022-08-03T16:06:43Z"
    reference_number: str
    reference_number_type: str

    def is_payment_reference(self):
        return self.object == ReferenceNumberObjectType.PAYMENT_REFERENCE

    @staticmethod
    def create(data: dict):
        return ReferenceNumber(
            id=data.get("id"),
            object=data.get("object"),
            live_mode=data.get("live_mode"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            reference_number=data.get("reference_number"),
            reference_number_type=data.get("reference_number_type")
        )