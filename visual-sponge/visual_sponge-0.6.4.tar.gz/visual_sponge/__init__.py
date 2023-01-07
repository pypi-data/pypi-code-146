from configparser import ConfigParser
from pathlib import Path
from importlib import import_module
from collections import OrderedDict
import Xponge
import MDAnalysis
mda = MDAnalysis
ChainReader = MDAnalysis.coordinates.chain.ChainReader

__version__ = "0.6.4"

class MyConfigParser(ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

Configure = MyConfigParser()
ConfigurePath = Path(__file__).parent / "conf.ini"


class Model():
    id = 0
    models = OrderedDict()
    WORKING = None
    def __init__(self, name, u):
        self.u = u
        self.name = name
        self.id = Model.id
        self.traj_files = []
        Model.models[self.id] = self
        Model.id += 1

    def __repr__(self):
        return f"Model.models[{self.id}]"

    def __str__(self):
        return repr(self)


class MACROS:
    VERSION = __version__
    PACKAGE = "Visual Sponge"
    PORT = None
    DEBUG_MODE = False
    APP = None
    CMD = None
    TEXT = ""
    TEMP = None

def Initialize():
    Configure.read(ConfigurePath)
    translation = import_module(".translation." + \
        Configure.get("OTHER", "language", fallback="chinese"), __name__).translation
    def localization(key):
        return translation.get(key, key)
    MACROS.localization = localization
    MACROS.PORT = MACROS.PORT or int(Configure.get("OTHER", "port", fallback="10696"))
    if "FORCEFIELD" in Configure:
        for value in Configure["FORCEFIELD"].values():
            Xponge.source(value)
