class ExpectedPaymentResponse:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json.get('id')

    @property
    def amount_upper_bound(self):
        return self.json.get('amount_upper_bound')

    @property
    def amount_lower_bound(self):
        return self.json.get('amount_lower_bound')

    @property
    def direction(self):
        return self.json.get('direction')

    @property
    def internal_account_id(self):
        return self.json.get('internal_account_id')

    @property
    def type(self):
        return self.json.get('type')

    @property
    def currency(self):
        return self.json.get('currency')

    @property
    def date_upper_bound(self):
        return self.json.get('date_upper_bound')

    @property
    def date_lower_bound(self):
        return self.json.get('date_lower_bound')

    @property
    def description(self):
        return self.json.get('description')

    @property
    def statement_descripto(self):
        return self.json.get('statement_descriptor')

    @property
    def metadata(self):
        return self.json.get('metadata')
