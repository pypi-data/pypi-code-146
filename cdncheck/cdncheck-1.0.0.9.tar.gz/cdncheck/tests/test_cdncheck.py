import pytest
import cdncheck
from dns import resolver

def test_cdncheck():
    assert cdncheck.cdncheck('192.168.1.1') == ""
    azurewebsites_ip = str(list(resolver.resolve('test.azurewebsites.net'))[0])
    assert cdncheck.cdncheck(azurewebsites_ip) == "azure"
