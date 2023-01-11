class IncomingPaymentDetailResponse:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json.get('id')
