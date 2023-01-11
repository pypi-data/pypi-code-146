

""""""# start delvewheel patch
def _delvewheel_init_patch_1_2_0():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'threedigrid_builder.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    if not is_pyinstaller or os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_2_0()
del _delvewheel_init_patch_1_2_0
# end delvewheel patch

from .application import *  # NOQA
from .exceptions import *  # NOQA

# fmt: off
__version__ = '1.7.0'
# fmt: on
