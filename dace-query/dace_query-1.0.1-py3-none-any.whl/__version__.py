import sys

major, minor, micro = sys.version_info.major, sys.version_info.minor, sys.version_info.micro

# Support, will be deprecated
if major >= 3 and minor >= 8:
    from importlib.metadata import metadata, PackageNotFoundError
else:
    from importlib_metadata import metadata, PackageNotFoundError

# Define the package name
__pkg_name__ = __package__  # Can be replaced by __package__ if root folder and package are the same

try:
    __title__ = metadata(__pkg_name__)['name']
    __version__ = metadata(__pkg_name__)['version']
except PackageNotFoundError:
    __title__ = 'dev'
    __version__ = '0.0.0-dev'

__py_version__ = '.'.join(map(str, [major, minor, micro]))
