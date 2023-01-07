import subprocess
from sun.daemon import Notify


def test_notify():
    out = subprocess.getoutput('ps -a')
    n = Notify()
    if 'sun_gtk' in out:
        assert True == n.gtk_loaded()