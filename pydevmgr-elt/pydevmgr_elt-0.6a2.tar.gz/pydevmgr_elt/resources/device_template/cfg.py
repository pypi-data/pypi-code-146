from pydevmgr_core import   NodeVar
from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt

from enum import Enum
Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 



class MotorCfg(Base):
    class Config(Base.Config):
        pass    
    class Data(Base.Data):
        pass           

