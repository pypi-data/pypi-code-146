from django.utils import timezone


class Receipt:
    _reference_id: str = None
    _driver: str = None
    _date = None

    def __init__(self, driver, reference_id):
        self._driver = driver
        self._reference_id = reference_id
        self._date = timezone.now()

    def get_driver(self) -> str:
        return self._driver

    def get_reference_id(self) -> str:
        return self._reference_id

    def get_date(self):
        return self._date
