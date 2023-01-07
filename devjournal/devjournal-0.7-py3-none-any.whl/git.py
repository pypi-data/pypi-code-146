import subprocess
import sys
from pathlib import Path


def run_git_script(name):  # pragma: no cov
    """
    Runs a script in a separate process.

    In tests, this method is mocked out and replaced with one that
    runs the script synchronously instead.
    """
    process = subprocess.Popen(
        [sys.executable, "-m", f"devjournal.git_scripts.{name}"],
        cwd=str(Path(__file__).parent.parent),
    )

    # Needed to avoid ResourceWarning, see https://bugs.python.org/issue38890
    process.returncode = 0
