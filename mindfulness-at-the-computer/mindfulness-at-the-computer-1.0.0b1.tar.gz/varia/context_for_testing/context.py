# noinspection PyUnresolvedReferences

"""

This file is one way to ensure that the development version of the application is tested.

If we run tests with ordinary imports we may be using a version of the application which has been
installed with pip

Inspiration for this file:
https://docs.python-guide.org/writing/structure/#structure-of-the-repository



An alternative approach, and the one we are now using is to install the application using
`pip3 -U -e .` which means that it will be installed in editable mode
This is the method used by Brian Okken in his book about PyTest


Old code which doesn't seem to be needed anymore:

import os
import sys

this_dir: str = os.path.dirname(__file__)
project_dir: str = os.path.abspath(os.path.join(this_dir, ".."))
sys.path.insert(0, project_dir)
# package_dir: str = os.path.join(project_dir, "mindfulness-at-the-computer")
# package_dir: str = os.path.join(project_dir, "matc")
# print(f"Inserting package directory: {package_dir=}")
# sys.path.insert(0, package_dir)
print(f"{sys.path=}")


# Problem: "ImportError: attempted relative import with no known parent package"

Please note: This only seems to happen when running "python3 -m unittest discover -s test", and not
when using pytest (which can run standard python unittests)

"""

# noinspection PyUnresolvedReferences
import matc.gui.modal_dialogs
# noinspection PyUnresolvedReferences
import matc.main_object
# noinspection PyUnresolvedReferences
import matc.shared
# noinspection PyUnresolvedReferences
import matc.state
