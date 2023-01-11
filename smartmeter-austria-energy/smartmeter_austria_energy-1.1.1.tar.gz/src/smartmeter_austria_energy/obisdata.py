from .constants import PhysicalUnits
from .decrypt import Decrypt
from .obisvalue import ObisValueFloat, ObisValueString


class ObisData():
    def __init__(self, dec: Decrypt, wanted_values: list[str]) -> None:
        self._voltageL1 = ObisValueFloat(0, PhysicalUnits.V)
        self._voltageL2 = ObisValueFloat(0, PhysicalUnits.V)
        self._voltageL3 = ObisValueFloat(0, PhysicalUnits.V)
        self._currentL1 = ObisValueFloat(0, PhysicalUnits.A)
        self._currentL2 = ObisValueFloat(0, PhysicalUnits.A)
        self._currentL3 = ObisValueFloat(0, PhysicalUnits.A)
        self._realPowerIn = ObisValueFloat(0, PhysicalUnits.W)
        self._realPowerOut = ObisValueFloat(0, PhysicalUnits.W)
        self._realEnergyIn = ObisValueFloat(0, PhysicalUnits.Wh)
        self._realEnergyOut = ObisValueFloat(0, PhysicalUnits.Wh)
        self._reactiveEnergyIn = ObisValueFloat(0, PhysicalUnits.varh)
        self._reactiveEnergyOut = ObisValueFloat(0, PhysicalUnits.varh)
        self._deviceNumber = ObisValueFloat(0)
        self._logicalDeviceNumber = ObisValueFloat(0)

        for key in wanted_values:
            myValue = dec.get_obis_value(key)

            if (hasattr(self, key)):
                setattr(self, key, myValue)

    # Voltage
    @property
    def VoltageL1(self) -> ObisValueFloat:
        return self._voltageL1

    @VoltageL1.setter
    def VoltageL1(self, voltageL1):
        self._voltageL1 = voltageL1

    @property
    def VoltageL2(self) -> ObisValueFloat:
        return self._voltageL2

    @VoltageL2.setter
    def VoltageL2(self, voltageL2):
        self._voltageL2 = voltageL2

    @property
    def VoltageL3(self) -> ObisValueFloat:
        return self._voltageL3

    @VoltageL3.setter
    def VoltageL3(self, voltageL3):
        self._voltageL3 = voltageL3

    # Current
    @property
    def CurrentL1(self) -> ObisValueFloat:
        return self._currentL1

    @CurrentL1.setter
    def CurrentL1(self, currentL1):
        self._currentL1 = currentL1

    @property
    def CurrentL2(self) -> ObisValueFloat:
        return self._currentL2

    @CurrentL2.setter
    def CurrentL2(self, currentL2):
        self._currentL2 = currentL2

    @property
    def CurrentL3(self) -> ObisValueFloat:
        return self._currentL3

    @CurrentL3.setter
    def CurrentL3(self, currentL3):
        self._currentL3 = currentL3

    # Power
    @property
    def RealPowerIn(self) -> ObisValueFloat:
        return self._realPowerIn

    @RealPowerIn.setter
    def RealPowerIn(self, realPowerIn):
        self._realPowerIn = realPowerIn

    @property
    def RealPowerOut(self) -> ObisValueFloat:
        return self._realPowerOut

    @RealPowerOut.setter
    def RealPowerOut(self, realPowerOut):
        self._realPowerOut = realPowerOut

    # Calculated power property
    @property
    def RealPowerDelta(self) -> ObisValueFloat:
        return self._realPowerIn - self._realPowerOut

    # Energy
    @property
    def RealEnergyIn(self) -> ObisValueFloat:
        return self._realEnergyIn

    @RealEnergyIn.setter
    def RealEnergyIn(self, realEnergyIn):
        self._realEnergyIn = realEnergyIn

    @property
    def RealEnergyOut(self) -> ObisValueFloat:
        return self._realEnergyOut

    @RealEnergyOut.setter
    def RealEnergyOut(self, realEnergyOut):
        self._realEnergyOut = realEnergyOut

    @property
    def ReactiveEnergyIn(self) -> ObisValueFloat:
        return self._reactiveEnergyIn

    @ReactiveEnergyIn.setter
    def ReactiveEnergyIn(self, reactiveEnergyIn):
        self._reactiveEnergyIn = reactiveEnergyIn

    @property
    def ReactiveEnergyOut(self) -> ObisValueFloat:
        return self._reactiveEnergyOut

    @ReactiveEnergyOut.setter
    def ReactiveEnergyOut(self, reactiveEnergyOut):
        self._reactiveEnergyOut = reactiveEnergyOut

    # Device
    @property
    def DeviceNumber(self) -> ObisValueString:
        return self._deviceNumber
    @DeviceNumber.setter
    def DeviceNumber(self, deviceNumber):
        self._deviceNumber = deviceNumber

    @property
    def LogicalDeviceNumber(self) -> ObisValueString:
        return self._logicalDeviceNumber
    @LogicalDeviceNumber.setter
    def LogicalDeviceNumber(self, logicalDeviceNumber):
        self._logicalDeviceNumber = logicalDeviceNumber
