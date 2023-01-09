from pydantic import BaseModel
from typing import (List, Union, Literal, Dict)

from steam_sdk.data.DataModelMagnet import Circuit, PowerSupply, EnergyExtraction


############################
# General parameters
class General(BaseModel):
    """
        Level 1: Class for general information on the case study
    """
    name: str = None
    place: str = None
    date: str = None
    time: str = None  # TODO: correct that it is a str?
    type: str = None  # natural quench, provoked discharge, powering cycle
    type_trigger: str = None
    circuit: str = None
    magnet: str = None
    conductor: str = None
    item: str = None  # another measured item that is not circuit, magnet, or conductor
    state: str = None  # occurred, predicted
    initial_temperature: str = None

############################
# Powering
class Powering(BaseModel):
    """
        Level 1: Class for information on the power supply and its current profile
    """
    # initial_current: str = None
    current_at_discharge: str = None
    max_dI_dt: str = None
    max_dI_dt2: str = None
    # custom_powering_cycle: List[List[float]] = [[]]  # optional
    PowerSupply: PowerSupply = PowerSupply()


############################
# Quench Heaters
class QuenchHeater(BaseModel):
    """
        Level 2: Class for information on the quench heater protection system
    """
    N_circuits: int = None
    strip_per_circuit: List[List[int]] = [[]]
    t_trigger: List[float] = []
    U0: List[float] = []
    C: List[float] = []
    R_warm: List[float] = []
    R_cold: List[float] = []
    R_total: List[float] = []
    L: float = None


############################
# CLIQ
class CLIQ(BaseModel):
    """
        Level 2: Class for information on the CLIQ protection system
    """
    t_trigger: float = None
    U0: float = None
    C: float = None
    R: float = None
    L: float = None


############################
# Quench protection
class QuenchProtection(BaseModel):
    """
        Level 1: Class for information on the quench protection system
    """
    Energy_Extraction: EnergyExtraction = EnergyExtraction()
    Quench_Heaters: QuenchHeater = QuenchHeater()
    CLIQ: CLIQ = CLIQ()
    # FQPLs: FQPLs = FQPLs()


############################
# Quench
class Quench(BaseModel):
    """
        Level 1: Class for information on the quench location
    """
    t_quench: str = None
    location_coil: str = None
    location_block: str = None
    location_turn: str = None
    location_half_turn: str = None


############################
# Highest level
class DataEventMagnet(BaseModel):
    '''
        **Class for the STEAM magnet event**

        This class contains the data structure of a magnet event analyzed with STEAM_SDK.

        :param N: test 1
        :type N: int
        :param n: test 2
        :type n: int

        :return: DataModelCircuit object
    '''

    GeneralParameters: General = General()
    Circuit: Circuit = Circuit()
    Powering: Powering = Powering()
    QuenchProtection: QuenchProtection = QuenchProtection()
    Quench: Quench = Quench()
