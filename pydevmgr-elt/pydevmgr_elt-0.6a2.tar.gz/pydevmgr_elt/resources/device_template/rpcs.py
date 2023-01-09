from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt

from enum import Enum
Base = EltDevice.Rpcs

R = Base.Rpc # Base Node
RC = R.Config


class RPC_ERROR(int, Enum):
    
    UNREGISTERED = -9999
    
enum_txt ({ # copy past on MgetRpcErrorTxt in PLC
          
        RPC_ERROR.UNREGISTERED:          'Unregistered RPC Error',
})



class MotorRpcs(Base):
    RPC_ERROR = RPC_ERROR

    class Config(Base.Config):
        pass   


