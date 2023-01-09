
from pydevmgr_core import   NodeVar
from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt

from enum import Enum
Base = EltDevice.Stat

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 



class SUBSTATE(int, Enum):
    OFF = 0
    NOT_OP = 1
    OP = 2
    
    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute         
enum_group ({
        SUBSTATE.OFF                   : GROUP.UNKNOWN,
        SUBSTATE.OP                    : GROUP.OK,
    })
    


class ERROR(int,  Enum):
    OK				      = _inc(0) # init the inc to zero 
    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute     
enum_txt ({
    ERROR.OK:				   'OK',
    ERROR.UNREGISTERED:        'ERROR: Unregistered Error'
    })



    #  ____  _        _     ___       _             __                 
    # / ___|| |_ __ _| |_  |_ _|_ __ | |_ ___ _ __ / _| __ _  ___ ___  
    # \___ \| __/ _` | __|  | || '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \ 
    #  ___) | || (_| | |_   | || | | | ||  __/ |  |  _| (_| | (_|  __/ 
    # |____/ \__\__,_|\__| |___|_| |_|\__\___|_|  |_|  \__,_|\___\___| 

class MotorStat(Base):
    # Add the constants to this class 
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    
    class Config(Base.Config):
        # define all the default configuration for each nodes. 
        # e.g. the suffix can be overwriten in construction (from a map file for instance)
        # all configured node will be accessible by the Interface
        pass

    # We can add some nodealias to compute some stuff on the fly 
    # If they node to be configured one can set a configuration above 
    
    # Node Alias here     
    # Build the Data object to be use with DataLink, the type and default are added here 
    class Data(Base.Data):
        error_code: NV[ERROR] = ERROR.OK
        pass

if __name__ == "__main__":
    MotorStat( )
