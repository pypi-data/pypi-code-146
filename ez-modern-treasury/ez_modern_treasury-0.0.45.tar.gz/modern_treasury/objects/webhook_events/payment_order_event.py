from modern_treasury.objects.reference_number import ReferenceNumber
from .base import Event, Data


class PaymentOrderEventStates:
    CREATED = "created"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    DENIED = "denied"
    APPROVED = "approved"


class PaymentOrderData(Data):
    @property
    def id(self):
        return self.json_data.get("id")

    @property
    def is_completed(self):
        return self.status == PaymentOrderEventStates.COMPLETED

    @property
    def is_cancelled(self):
        return self.status == PaymentOrderEventStates.CANCELLED
    
    @property
    def is_denied(self):
        return self.status == PaymentOrderEventStates.CANCELLED

    @property
    def id(self):
        return self.json_data.get("id")

    @property
    def reference_numbers(self) -> ReferenceNumber:
        return [ReferenceNumber.create(ref_number)  for ref_number in self.json_data.get("reference_numbers", [])]


class PaymentOrderEvent(Event):
    @property
    def data(self):
        return PaymentOrderData(json_data=self.json_data.get("data", {}))

    @property
    def event_type(self):
        return self.json_data.get("event")
