"""
unid 0.0.0

a module designed to make unique identifiers
for variables and other constants

FUTURE FEATURES

    - communicative id manager (sockets)
    - more extensive overlays
    - allow multiple base-? overlays

TESTED ON

    - Python 3.11.1 (MacOS)
"""

__version__ = "0.0.0"

# module imports
import os
import pathlib
import dbm


HOME_PATH = pathlib.Path.home()  # computer's home path
PACKAGE_ROOT = os.path.join(HOME_PATH, ".unid")  # package data storage location

# overlays
TYPE_OVERLAY = "typeoverlay"
TYPE_BASEOVERLAY = "typebaseoverlay"  # base? nums


"""OVERLAYS"""
class PipelineStructuringError(Exception):
    pass


class OverlayPipeline:
    """
    Allow multiple overlays to be overlayed
    on an ID manager.
    """

    def __init__(self, overlays=[]):
        """
        Initialize overlay pipeline

        overlays -- list of overlays to apply
        """
        self.overlays = overlays

    def _overlay(self, num):
        """Apply each of the overlays"""
        for overlay in self.overlays:
            num = overlay._overlay(num)
        return num


class Overlay:
    TYPE = TYPE_OVERLAY

    def __init__(self):
        pass

    def _overlay(self, num):
        pass


class BinaryOverlay(Overlay):
    TYPE = TYPE_BASEOVERLAY

    def _overlay(self, num):
        return bin(num)


class Base10Overlay(Overlay):
    TYPE = TYPE_BASEOVERLAY

    def _overlay(self, num):
        return int(num)


class OctalOverlay(Overlay):
    TYPE = TYPE_BASEOVERLAY

    def _overlay(self, num):
        return oct(num)


class HexadecimalOverlay(Overlay):
    TYPE = TYPE_BASEOVERLAY

    def _overlay(self, num):
        return hex(num)


# pointers
Base2Overlay = BinaryOverlay  # pointer to binary function
Base8Overlay = OctalOverlay  # pointer to octal function
Base16Overlay = HexadecimalOverlay  # pointer to hexadecimal function


"""ID MANAGERS"""


class IDManager():
    """
    A system for creating unique
    IDs.
    """

    def __init__(self, overlay=Base10Overlay):
        """
        Initialize an ID Manager

        system -- ID generation system
        """
        self._curid = -1  # integer curid
        self.curid = -1  # overlayed curid
        self.overlay = overlay  # should be callable

    def __iter__(self):
        return self

    def __next__(self):
        return self.new

    def _apply_overlay(self):
        if self.overlay is not None:
            self._curid = int(self._curid)
            self.curid = self.overlay._overlay(self._curid)
        else:
            self.curid = self._curid

    @property
    def new(self):
        """Generate new ID"""
        self._curid += 1
        self._apply_overlay()
        return self.curid

    def reset(self):
        """Reset ID counter"""
        self._curid = -1


class PersistentIDManager(IDManager):
    def __init__(self, name, overlay=None):
        super().__init__()

        self.name = name.encode()
        self.overlay = overlay
        self.db_path = os.path.join(PACKAGE_ROOT, "unid-data")
        self._read_data()

    def _read_data(self):
        db = dbm.open(self.db_path, "c")
        if self.name in db.keys():
            print("exists")
            self._curid = int(db[self.name])  # int upon load
        else:
            print("aint existant")
            db[self.name] = str(self._curid)  # save as str
        db.close()

    def _save_curid(self):
        db = dbm.open(self.db_path, "c")
        db[self.name] = str(self._curid)

    @property
    def new(self):
        self._curid += 1
        self._apply_overlay()
        self._save_curid()
        return self.curid

    def reset(self):
        self._curid = -1
        self._save_curid()

