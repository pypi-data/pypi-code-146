import sys
import os

# Prepend local dir to path to override possibly installed docker_parser
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))

import docker_parser as dp
import unittest

from cases.parser import *

if __name__ == "__main__":
    unittest.main()