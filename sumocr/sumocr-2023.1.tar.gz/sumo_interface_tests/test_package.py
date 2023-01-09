"""
High-level tests for the whole package
"""

import subprocess
from sumo_interface_tests.common.marker import *


@unit_test
@functional
def test_licenses():
    #TODO: there seems to be a bug in the tool
    return
    # only list non-restrictive licenses compliant with BSD
    allowed_licenses = ["MIT License",
                        "BSD License",
                        "Mozilla Public License 2.0 (MPL 2.0)",
                        "ISC License (ISCL)",
                        "Python Software Foundation License",
                        "Apache Software License"]
    allowed_licenses = ";".join(allowed_licenses)
    print(subprocess.run(["pip-licenses", f"--allow-only='{allowed_licenses}'"], check=True))