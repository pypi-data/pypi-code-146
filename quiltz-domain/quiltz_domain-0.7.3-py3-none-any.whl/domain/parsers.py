from datetime import date
from .results import Success, Failure


class StringToDateParser():
    def parse_from(self, date_string, success_attribute='date'):
        if not date_string:
            return Failure(message=f'{success_attribute} is missing')
        try:
            return Success(**{success_attribute: date.fromisoformat(date_string)})
        except ValueError as e:
            return Failure(message=f'{success_attribute}: {e}')


class StringToIntParser:
    def parse_from(self, int_string, success_attribute='int_val'):
        try:
            return Success(**{success_attribute: int(int_string)})
        except ValueError as e:
            return Failure(message="'{}' is not a valid integer".format(int_string))


date_from_iso = StringToDateParser()
int_from_string = StringToIntParser()
