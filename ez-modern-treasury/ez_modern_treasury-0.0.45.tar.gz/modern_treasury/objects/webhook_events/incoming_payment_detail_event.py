from .base import Event, Data


class IncomingPaymentDetailsEventStates:
    COMPLETED = "completed"
    FAILED = "failed"


class IncomingPaymentDetailEventData(Data):
    @property
    def id(self):
        return self.json_data.get("id")

    @property
    def bank_transaction_id(self):
        return self.json_data.get("data", {}).get("id")

    @property
    def payment_type(self):
        return self.json_data.get("type")

    @property
    def is_payment_type_ach(self):
        return self.payment_type == "ach"

    @property
    def is_completed(self):
        return self.status == IncomingPaymentDetailsEventStates.COMPLETED

    @property
    def is_failed(self):
        return self.status == IncomingPaymentDetailsEventStates.FAILED

    @property
    def virtual_account_id(self):
        return self.json_data.get("virtual_account_id")


class IncomingPaymentDetailEvent(Event):
    @property
    def data(self):
        return IncomingPaymentDetailEventData(json_data=self.json_data.get("data", {}))

    @property
    def virtual_account_id(self):
        return self.data.virtual_account_id
