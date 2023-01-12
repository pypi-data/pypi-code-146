"""Test ``__init__.py``."""
import sys
from unittest import TestCase

from sphinxcontrib.eval import eval_python, eval_sh

from . import AppMixin


class Test(AppMixin, TestCase):
    """Test."""

    def test_eval_sh(self) -> None:
        """Test eval sh.

        :rtype: None
        """
        rst = eval_sh("a=1; echo -n $a")
        assert rst == "1"
        rst = eval_sh("|")
        assert rst == ""

    def test_eval_python(self) -> None:
        """Test eval python.

        :rtype: None
        """
        rst = eval_python("print(sys.version_info, end='')")
        assert rst == ""
        rst = eval_python("import sys; print(sys.version_info, end='')")
        assert rst == str(sys.version_info)

    def test_setup(self):
        """Test setup."""
        app = self.app
        assert app.env.config.eval_funcs == {"sh": eval_sh}  # type: ignore
