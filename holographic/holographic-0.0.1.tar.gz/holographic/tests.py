import os
import subprocess
import tempfile

import pytest

def test_changes():
    """
    Confirm that the consumer end of the transmission stays in-sync with the producer end over a series of
    changes to the producer-end of the filesystem. We are going to do this by running the producer and the
    server as subprocesses and then interacting with the server through http requests.
    """
    server_process = subprocess.run(
        f"python {dot_slash('server.py')}",
        shell=True,
        capture_output=True,
    )



def dot_slash(relpath):
    """
    Creates an absolute path from the specified relative path with the packages root 
    as the base of the path.
    """
    here = os.path.dirname(os.path.realpath(__file__))
    return os.path.normpath(os.path.join(here, relpath))