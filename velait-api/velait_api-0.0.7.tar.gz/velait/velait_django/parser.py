from djangorestframework_camel_case.parser import CamelCaseFormParser
from djangorestframework_camel_case.parser import CamelCaseMultiPartParser
from djangorestframework_camel_case.parser import CamelCaseJSONParser


class VelaitFormParser(CamelCaseFormParser):
    pass


class VelaitMultiPartParser(CamelCaseMultiPartParser):
    pass


class VelaitAPIParser(CamelCaseJSONParser):
    pass


__all__ = [
    'VelaitFormParser',
    'VelaitMultiPartParser',
    'VelaitAPIParser',
]
