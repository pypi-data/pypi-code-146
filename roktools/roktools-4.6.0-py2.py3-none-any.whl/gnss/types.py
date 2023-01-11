from enum import Enum
from dataclasses import dataclass

class ConstellationId(Enum):
    GPS : str = 'G' 
    GALILEO : str = 'E'
    
    
class ChannelCode(Enum):
    c_1C : str = "1C"
    c_5Q : str = "5Q"
    
    
@dataclass 
class Satellite:
    constellation_id: ConstellationId
    satellite_id: int
    
    
    def __repr__(self) -> str:
        return f"{self.constellation_id.value}{self.satellite_id:02d}"


@dataclass
class Signal:
    satellite: Satellite
    channel: ChannelCode
    

    def __repr__(self) -> str:
        return f"{self.satellite}{self.channel.value}"
    
    
class GnssSystem:
    constellation_id: ConstellationId
    number_satellites: int
    channels: list[ChannelCode]
    signals: list[Signal]
    

    def __init__(self, constellation_id: ConstellationId, number_satellites: int, channels: list[ChannelCode]):
        self.constellation_id = constellation_id
        self.number_satellites = number_satellites
        self.channels = channels
        self.signals = self.get_signals()
        

    def get_signals(self) -> list[Signal]:
        signals = []
        for index in range(1, self.number_satellites + 1):
            for channel in self.channels:
                signals.append(Signal(Satellite(self.constellation_id, index), channel))
                
        return signals

@dataclass    
class GnssSystems:
    gnss_systems: list[GnssSystem]
    

    def get_constellations(self) -> list[str]:
        return [system.constellation_id.value for system in self.gnss_systems]
    

    def get_signals(self) -> list[Signal]:
        signals = []
        for system in self.gnss_systems:
            signals.extend(system.get_signals())
        return signals