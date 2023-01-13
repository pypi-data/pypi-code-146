"""
CLI package that has all the fuctionality directly related to the cli
implemented with click. qalx is the main function object that provides all the
cli related functionality
"""

from qalxcli.cli.qalx import qalx  # noqa

# The rest of the imports are needed to ensure all the decorators from the other
# modules of cli are bound to the qalx object
from qalxcli.cli import bots  # noqa
from qalxcli.cli import factory  # noqa
