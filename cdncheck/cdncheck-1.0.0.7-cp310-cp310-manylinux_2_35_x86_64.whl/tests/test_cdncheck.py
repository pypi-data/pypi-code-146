import pytest
import cdncheck

def test_cdncheck():
    assert cdncheck.cdncheck('192.168.1.1') == ""
