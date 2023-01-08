import django
from .exception import VersionError 


def check_version_compatibility():
    if django.VERSION < (3, 0):
        raise VersionError("finflo works with django 3.0 and higher , please upgrade to the latest version \
        of django")
    return check_version_compatibility


