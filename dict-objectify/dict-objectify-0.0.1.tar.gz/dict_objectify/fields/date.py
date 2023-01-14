from datetime import datetime
from typing import Optional, Union

from dict_objectify.base.field_base import FieldBase

DEFAULT_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class Datetime(FieldBase):
    def __init__(self,
                 tag: str = None,
                 *,
                 datetime_format: str = DEFAULT_FORMAT,
                 primary: bool = False,
                 nullable: bool = True) -> None:
        self.datetime_format = datetime_format
        super().__init__(tag, primary=primary, nullable=nullable)

    def __set__(self, instance, value: Union[str, datetime]):
        if hasattr(value, 'strftime'):
            value = value.strftime(self.datetime_format)

        super().__set__(instance, value)

    def _parse_datetime(self, element: datetime) -> datetime:
        return element

    def _parse_string(self, element: str) -> Optional[datetime]:
        standard_formats = [DEFAULT_FORMAT,
                            self.datetime_format,
                            '%Y-%m-%d']

        for standard_format in standard_formats:
            try:
                return datetime.strptime(element, standard_format)
            except ValueError:
                pass

        raise ValueError(
            f'The standardised Datetime field '
            f'parses only the following formats: '
            f'{standard_formats}. The value "{element}" is incompatible.')

    def __get__(self, instance, owner) -> Optional[datetime]:
        return super().__get__(instance, owner)
