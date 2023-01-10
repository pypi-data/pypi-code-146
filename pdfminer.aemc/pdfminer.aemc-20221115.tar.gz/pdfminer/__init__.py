# __version__ = "__VERSION__"  # auto replaced with tag in github actions

# if __name__ == "__main__":
#     print(__version__)


import sys
import warnings


__version__ = '20221115'

if sys.version_info < (3, 6):
    warnings.warn('Please upgrade to Python 3.6 or newer.')

if __name__ == '__main__':
    print(__version__)
