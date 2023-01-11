from unittest import TestCase
import sys

import busy
from busy import PYTHON_VERSION

class TestPythonVersion(TestCase):

    def test_python_version(self):
        self.assertTrue(sys.version_info >= PYTHON_VERSION)
