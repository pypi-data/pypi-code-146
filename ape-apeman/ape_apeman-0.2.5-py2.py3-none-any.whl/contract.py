# ape_apeman contract module


class ContractCallResult:
    def __init__(self, ret=None):
        self.decoded_logs = []
        self.receipt = None
        self.ret = ret

    def set_receipt(self, receipt):
        self.receipt = receipt
        self.decoded_logs = [log for log in receipt.decode_logs()]
        if len(self.decoded_logs):
            self.ret = self.decoded_logs[0]
        else:
            self.ret = None

    def dict(self):
        return dict(
            ret=self.ret, receipt=self.receipt.dict() if self.receipt else None
        )
