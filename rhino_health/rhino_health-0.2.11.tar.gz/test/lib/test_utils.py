import sys

import pytest

from rhino_health.lib.utils import RhinoSDKException, rhino_error_wrapper, setup_traceback


class TestUtils:
    def test_exception_wrapper(self):
        setup_traceback(sys.excepthook, True)  # Set it up
        # Test wrapped function properly wraps
        @rhino_error_wrapper
        def test_function():
            raise RuntimeError("Hi")

        with pytest.raises(RhinoSDKException):
            test_function()
        # Test unwrapped errors still properly display
        with pytest.raises(ValueError):
            raise ValueError("Bye")
