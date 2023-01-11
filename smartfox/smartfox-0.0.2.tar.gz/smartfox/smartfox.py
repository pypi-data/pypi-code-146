"""SmartFox API wrapper for Python"""

import io
from xml.etree import ElementTree
from datetime import datetime
import requests

from .smartfoxObjects import PowerValue, EnergyValue, Phase, Relay, AnalogOut, PercentValue, TempValue


class Smartfox():
    def __init__(self, host:str, port:int=80, verify:bool=False, scheme:str="http", **kwargs):
        self.host = host
        self.port = port
        self.verify = verify
        self.scheme = scheme
        
        self.valuesPath = kwargs.get("valuesPath", "values.xml")
        self.timeout = kwargs.get("timeout", 5)
        
        # ToDo Fill these values
        self.mac = None
        self.version = None
        self.wlanVersion = None
        self.ip = None
        
        self.lastUpdate = None
        
        # Power
        self.consumption = PowerValue()
        self.pv = PowerValue()
        self.carCharger = PowerValue()
        self.heatPump = PowerValue()
        self.power = PowerValue()
        self.effectivePower = PowerValue()
        self.heatPumpPower = PowerValue()
        self.heatPumpThermPower = PowerValue()
        self.batteryPower = PowerValue()
        
        # Energy
        self.energy = EnergyValue()
        self.returnEnergy = EnergyValue()
        self.effectiveEnergy = EnergyValue()
        self.apparentEnergy = EnergyValue()
        self.dayEnergy = EnergyValue()
        self.dayReturnEnergy = EnergyValue()
        self.dayEffectiveEnergy = EnergyValue()
        self.carChargerCurrentChargeEnergy = EnergyValue()
        self.carChargerEnergy = EnergyValue()
        self.heatPumpEnergy = EnergyValue()
        self.heatPumpThermEnergy = EnergyValue()
        
        # Phaes
        self.phase1 = Phase()
        self.phase2 = Phase()
        self.phase3 = Phase()
        
        # Relays
        self.relay1 = Relay(id=1, smartfox=self)
        self.relay2 = Relay(id=2, smartfox=self)
        self.relay3 = Relay(id=3, smartfox=self)
        self.relay4 = Relay(id=4, smartfox=self)
        
        # Analog
        self.analog = AnalogOut(smartfox=self)
        
        # Percentage
        self.soc = PercentValue()
        
        # Temperature
        self.bufferHot = TempValue()
        self.bufferCold = TempValue()
        self.warmWater = TempValue()

        
    def updateValues(self, values:dict) -> bool:
        """Update values on the SmartFox device"""
        # Power Values
        self.consumption.value = values.get("u5255-41")
        self.pv.value  = values.get("u5272-41")
        self.carCharger.value  = values.get("u6095-41")
        self.heatPump.value  = values.get("u4541-41")
        self.power.value  = values.get("u5790-41")
        self.effectivePower.value  = values.get("u5815-41")
        self.heatPumpPower.value  = values.get("u6134-41")
        self.heatPumpThermPower.value = values.get("u6164-41")
        self.batteryPower.value = values.get("u6209-41")
        
        # Energy Values
        self.energy.value  = values.get("u5827-41")
        self.returnEnergy.value  = values.get("u5824-41")
        self.effectiveEnergy.value  = values.get("u5842-41")
        self.apparentEnergy.value  = values.get("u5845-41")
        
        self.dayEnergy.value  = values.get("u5863-41")
        self.dayReturnEnergy.value  = values.get("u5872-41")
        self.dayEffectiveEnergy.value  = values.get("u5881-41")
        
        self.carChargerCurrentChargeEnergy.value = values.get("u6122-41")
        self.carChargerEnergy.value = values.get("u6096-41")
        
        self.heatPumpEnergy.value = values.get("u6140-41")
        self.heatPumpThermEnergy.value = values.get("u6164-41")
        
        # Phases
        self.phase1.current.value=values.get("u5999-41")
        self.phase1.voltage.value=values.get("u5978-41")
        self.phase1.power.value=values.get("u6017-41")
        self.phase1.powerFactor.value=values.get("u6074-41")

        self.phase2.voltage.value=values.get("u5981-41")
        self.phase2.current.value=values.get("u5996-41")
        self.phase2.power.value=values.get("u6014-41")
        self.phase2.powerFactor.value=values.get("u6083-41")

        self.phase3.voltage.value=values.get("u5984-41")
        self.phase3.current.value=values.get("u5984-41")
        self.phase3.power.value=values.get("u5984-41")
        self.phase3.powerFactor.value=values.get("u6086-41")
        
        # Relays
        self.relay1.state = values.get("u5674-41")
        self.relay1.remainingTime.value = values.get("u5737-41")
        self.relay1.overallTime.value = values.get("u5773-41")
        
        self.relay2.state = values.get("u5704-41")
        self.relay2.remainingTime.value = values.get("u5740-41")
        self.relay2.overallTime.value = values.get("u5776-41")

        self.relay3.state = values.get("u5710-41")
        self.relay3.remainingTime.value = values.get("u5743-41")
        self.relay3.overallTime.value = values.get("u5779-41")
        
        self.relay4.state = values.get("u5707-41")
        self.relay4.remainingTime.value = values.get("u5746-41")
        self.relay4.overallTime.value = values.get("u5782-41")

        # Analog
        self.analog.percentage.value = values.get("u5641-41")
        self.analog.power.value = values.get("u4505-41")

        # Percentage
        self.soc.value = values.get("u6221-41")
        
        # Temperature
        self.bufferHot = values.get("u6176-41")
        self.bufferCold = values.get("u6182-41")
        self.warmWater = values.get("u6182-41")

        self.lastUpdate = datetime.now()
        return True

    def parseXML(self, resp):
        tree = ElementTree.parse(io.StringIO(resp.content.decode("utf-8")))
        root = tree.getroot()
        values = {}
        for element in root:
            values[element.attrib.get("id")] = element.text
        return values
        
    def getValues(self):
        """Get all values from the SmartFox device"""
        resp = requests.get(f"{self.scheme}://{self.host}/{self.valuesPath}", verify=self.verify)
        if resp.status_code == 200:
            return self.updateValues(self.parseXML(resp))

    def setRelay(self, relay: Relay, state: bool) -> bool:
        """Set a relay on the SmartFox device"""
        resp = requests.get(f"{self.scheme}://{self.host}/setswrel.cgi?rel={relay.id}&state={'1' if state else '0'}", verify=self.verify)
        if resp.status_code == 200:
            self.updateValues(self.parseXML(resp))
            return True
        return False

    def setAnalog(self, value: int, mode: int = 0)  -> bool:
        """Set the analog output on the SmartFox device"""
        resp = requests.get(f"{self.scheme}://{self.host}/setswaout.cgi?mode={mode}&power={value}", verify=self.verify)
        if resp.status_code == 200:
            self.updateValues(self.parseXML(resp))
            return True
        return False