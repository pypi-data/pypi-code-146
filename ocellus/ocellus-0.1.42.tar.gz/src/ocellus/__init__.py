# Copyright © 2022 Byte Motion AB
import sys
from os import path
  
# Adding the cwd to the path is needed since
# scripts generated from protos do not take the
# module name into consideration when importing.
cwd = path.abspath(path.dirname(__file__))
sys.path += [cwd]
