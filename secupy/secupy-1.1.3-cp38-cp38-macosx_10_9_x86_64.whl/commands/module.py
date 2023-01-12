import os
import sys
from runpy import _run_module_as_main


def main():
    os.environ["PYTHONPATH"] = os.getcwd()
    sys.path.append(os.getcwd())

    # Run the module specified as the next command line argument
    if len(sys.argv) < 3:
        print("No module specified for execution", file=sys.stderr)
    else:
        del sys.argv[0]  # Make the requested module sys.argv[0]
        del sys.argv[0]  # Make the requested module sys.argv[0]
        _run_module_as_main(sys.argv[0])
