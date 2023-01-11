

class PowerValue():
    """Smartfox Power Value used for Objects with Power Values"""
    def __init__(self):
        self._value = None
        self.unit = "W"

    def getValue(self):
        """Get a Power Value"""
        return self._value
    
    def parseValue(self, value) -> float:
        """Parse a Power Value"""
        if len(value.split(" ")) == 2: # if ther is a Unit
            if value.split(" ")[1] == "kW":
                return float(value.split(" ")[0])*1000
            elif value.split(" ")[1] == "W":
                return float(value.split(" ")[0])
            else:
                return 0
        else: # no unit
            return float(value)
        
    def setValue(self, value):
        self._value = self.parseValue(value)
        
    value = property(getValue, setValue)
    
    def __str__(self):
        return f"power value: {str(self.value)} {self.unit}"

class EnergyValue():
    """Smartfox Energy Value used for Objects with Energy Values"""
    def __init__(self, ):
        self._value = None
        self.unit = "Wh"

    def getValue(self):
        """Get a Power Value"""
        return self._value
    
    def parseValue(self, value) -> float:
        """Parse a Power Value"""
        if len(value.split(" ")) == 2: # if ther is a Unit
            if value.split(" ")[1] == "kWh":
                return float(value.split(" ")[0])*1000
            elif value.split(" ")[1] == "Wh":
                return float(value.split(" ")[0])
            elif value.split(" ")[1] == "kVAh":
                self.unit = "kVAh"
                return float(value.split(" ")[0])
        else:
            return float(value)
    
    def setValue(self, value):
        self._value = self.parseValue(value)
        
    value = property(getValue, setValue)
    
    def __str__(self):
        return f"energy value: {str(self.value)} {self.unit}"

class VoltageValue():
    """Smartfox Voltage Value used for Objects with Voltage Values"""
    def __init__(self):
        self._value = None
        self.unit = "V"

    def getValue(self):
        """Get a Power Value"""
        return self._value
    
    def parseValue(self, value) -> float:
        """Parse the Value"""
        return float(value.split(" ")[0])

    def setValue(self, value):
        self._value = self.parseValue(value)
        
    value = property(getValue, setValue)

    def __str__(self):
        return f"voltage value: {str(self.value)} {self.unit}"

class CurrentValue():
    """Smartfox Current Value used for Objects with Current Values"""
    def __init__(self):
        self._value = None
        self.unit = "A"

    def getValue(self):
        """Get a Power Value"""
        return self._value
    
    def parseValue(self, value) -> float:
        """Parse the Value"""
        if len(value.split(" ")) == 2: # Value in Str
            return float(value.split(" ")[0])
        else:
            return float(value)

    def setValue(self, value):
        self._value = self.parseValue(value)
        
    value = property(getValue, setValue)
    
    def __str__(self):
        return f"current value: {str(self.value)} {self.unit}"
    
class PFValue():
    """Smartfox PowerFactor Value used for Objects with PowerFactor Values"""
    def __init__(self):
        self._value = None
        self.unit = "°"

    def getValue(self):
        """Get a Power Value"""
        return self._value
    
    def parseValue(self, value) -> float:
        """Parse the Value"""
        return float(value.split(" ")[0])

    def setValue(self, value):
        self._value = self.parseValue(value)
        
    value = property(getValue, setValue)
    
    def __str__(self):
        return f"power-factor value: {str(self.value)} {self.unit}"

class Phase():
    """Smartfox Phase used for Objects with Phase Values"""
    def __init__(self) -> None:
        self.voltage = VoltageValue()
        self.current = CurrentValue()
        self.power = PowerValue()
        self.powerFactor = PFValue()

class TimeValue():
    """Smartfox PowerFactor Value used for Objects with PowerFactor Values"""
    def __init__(self):
        self.unit = "min"
        self._value = None

    def getValue(self) -> int:
        """Get a Value"""
        if self._value is None:
            return None
        return int(self._value)

    def setValue(self, value):
        self._value = value.split(" ")[0]
        
    value = property(getValue, setValue)

    def __str__(self):
        return f"time value: {str(self.value)} {self.unit}"

class Relay():
    """Smartfox Relay"""
    def __init__(self, smartfox, id: int = None) -> None:
        self._state = None
        self.id = id
        self.remainingTime = TimeValue()
        self.overallTime = TimeValue()
        self.smartfox = smartfox
        
    def getState(self) -> bool:
        """Get a Power Value"""
        return self._state

    def setState(self, value) -> None:
        if value == "0":
            self._state = False
        elif value == "1":
            self._state = True
        else:
            self._state = None
        
    def turnOn(self) -> None:
        self.smartfox.setRelay(relay=self, state=True)
        
    def turnOff(self) -> None:
        self.smartfox.setRelay(relay=self, state=False)
        
    state = property(getState, setState)
    
    def __str__(self):
        return f"relay {self.id} state: {str(self.value)}"

class PercentValue():
    """Smartfox PowerFactor Value used for Objects with PowerFactor Values"""
    def __init__(self):
        self.unit = "%"
        self._value = None

    def getValue(self) -> int:
        """Get a Value"""
        if self._value is None:
            return None
        return int(self._value)

    def setValue(self, value):
        if len(value.split(" ")) == 2: # Unit detected
            self._value = value.split(" ")[0]
        else:
            self._value = value
    value = property(getValue, setValue)

    def __str__(self):
        return f"percent value: {str(self.value)} {self.unit}"
    
class AnalogOut():
    """Smartfox Relay"""
    def __init__(self, smartfox, id: int = None) -> None:
        self.percentage = PercentValue()
        self.power = PowerValue()
        self.smartfox = smartfox
        
    def set(self, value) -> None: #Set Manuell
        self.smartfox.setAnalog(value=value, mode=1)

    def setAuto(self) -> None: #set Auto
        self.smartfox.setAnalog(value=0, mode=2)

    def off(self) -> None: #Set off
        self.smartfox.setAnalog(value=0, mode=0)
        
    def __str__(self):
        return f"analog out: {self.percentage} {self.power}"

class TempValue():
    """Smartfox PowerFactor Value used for Objects with PowerFactor Values"""
    def __init__(self):
        self.unit = "°C"
        self._value = None

    def getValue(self) -> float:
        """Get a Value"""
        if self._value is None:
            return None
        return float(self._value)

    def setValue(self, value):
        if len(value.split(" ")) == 2: # Unit detected
            self._value = value.split(" ")[0]
        else:
            self._value = value
    value = property(getValue, setValue)

    def __str__(self):
        return f"temp value: {self.value} {self.unit}"