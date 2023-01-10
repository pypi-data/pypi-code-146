import uuid


class Invoice:
    _details: dict = {}
    transaction_id: str
    amount: int
    driver: str

    def __init__(self):
        self.create_uuid()

    def create_uuid(self, uuid_param=None):
        if not uuid_param:
            uuid_param = str(uuid.uuid4())

        self.uuid = uuid_param

    def get_uuid(self):
        return self.uuid

    def via(self, driver):
        self.driver = driver

    def set_amount(self, amount):
        if not isinstance(amount, int):
            raise Exception('Amount value should be a number (integer).')
        self.amount = amount

    def set_transaction_id(self, transaction_id):
        self.transaction_id = transaction_id

    def get_transaction_id(self):
        return self.transaction_id

    def set_details(self, key, value):
        self._details[key] = value

    def get_details(self) -> dict:
        return self._details

    def get_detail(self, key) -> str:
        return self._details.get(key)
