# Spoof module atelier_fabrique, so module should will be imported from ../atelier_fabrique dir

import importlib
import os
import sys
from importlib.abc import MetaPathFinder

DEF_PATH = sys.path[0]

cur_file_path = os.path.dirname(os.path.abspath(__file__))
LIB_NAME = 'fabrique_nodes_core'

LIB_LOCAL_FILE_PATH = f"{cur_file_path}/../{LIB_NAME}/__init__.py"

sys.modules.pop(LIB_NAME, None)  # if lib installed - ignore it


class LocalFinder(MetaPathFinder):
    def find_module(self, fullname, path=DEF_PATH):
        if fullname == LIB_NAME:
            module_spec = importlib.util.spec_from_file_location(fullname, LIB_LOCAL_FILE_PATH)
            print(f'"{LIB_NAME}" ->  "{LIB_LOCAL_FILE_PATH}" spoofed')
            return module_spec.loader
        else:
            return super().find_module(fullname, path)


sys.meta_path = [LocalFinder(), ] + sys.meta_path
