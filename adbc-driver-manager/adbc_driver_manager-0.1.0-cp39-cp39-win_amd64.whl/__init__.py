# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Low-level ADBC bindings for Python.

The root module provides a fairly direct, 1:1 mapping to the C API
definitions in Python.  For a higher-level interface, use
:mod:`adbc_driver_manager.dbapi`.  (This requires PyArrow.)
"""


# start delvewheel patch
def _delvewheel_init_patch_1_1_4():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'adbc_driver_manager.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-adbc_driver_manager-0.1.0')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-adbc_driver_manager-0.1.0')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    ctypes.WinDLL(lib_path)


_delvewheel_init_patch_1_1_4()
del _delvewheel_init_patch_1_1_4
# end delvewheel patch



from ._lib import (
    INGEST_OPTION_MODE,
    INGEST_OPTION_MODE_APPEND,
    INGEST_OPTION_MODE_CREATE,
    INGEST_OPTION_TARGET_TABLE,
    AdbcConnection,
    AdbcDatabase,
    AdbcInfoCode,
    AdbcStatement,
    AdbcStatusCode,
    ArrowArrayHandle,
    ArrowArrayStreamHandle,
    ArrowSchemaHandle,
    DatabaseError,
    DataError,
    Error,
    GetObjectsDepth,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Warning,
)
from ._version import __version__

__all__ = [
    "__version__",
    "INGEST_OPTION_MODE",
    "INGEST_OPTION_MODE_APPEND",
    "INGEST_OPTION_MODE_CREATE",
    "INGEST_OPTION_TARGET_TABLE",
    "AdbcConnection",
    "AdbcDatabase",
    "AdbcInfoCode",
    "AdbcStatement",
    "AdbcStatusCode",
    "ArrowArrayHandle",
    "ArrowArrayStreamHandle",
    "ArrowSchemaHandle",
    "DatabaseError",
    "DataError",
    "Error",
    "GetObjectsDepth",
    "IntegrityError",
    "InterfaceError",
    "InternalError",
    "NotSupportedError",
    "OperationalError",
    "ProgrammingError",
    "Warning",
]