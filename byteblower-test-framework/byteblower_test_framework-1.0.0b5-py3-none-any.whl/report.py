"""Reporting interfaces."""
from ._report.byteblowerhtmlreport import ByteBlowerHtmlReport
from ._report.byteblowerjsonreport import ByteBlowerJsonReport
# NOTE: Not really required in user interface:
# `ByteBlowerReport` is not really needed, but is useful for type hinting:
from ._report.byteblowerreport import ByteBlowerReport  # noqa: F401
from ._report.byteblowerunittestreport import ByteBlowerUnitTestReport
from ._report.options import Layer2Speed
from ._report.unittestreport import UnitTestReport

# Export the user interfaces.
#
# Outcomes:
# * Limits import on `from byteblower_test_framework.report import *`
# * Exposes the interfaces in the (Sphinx) documentation
#
# NOTE
#   Exporting imported variables does not introduce them in the (Sphinx) docs.
#   It does introduce their name and value in `help()` of this module though.
#
__all__ = (
    # Reporting options:
    Layer2Speed.__name__,
    # Reporting bases:
    ByteBlowerReport.__name__,
    UnitTestReport.__name__,
    # Report types:
    ByteBlowerHtmlReport.__name__,
    ByteBlowerJsonReport.__name__,
    ByteBlowerUnitTestReport.__name__,
)
