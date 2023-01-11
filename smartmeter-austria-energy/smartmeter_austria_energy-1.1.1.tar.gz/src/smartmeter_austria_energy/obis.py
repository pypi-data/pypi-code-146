class Obis:
    def to_bytes(code):
        return bytes([int(a) for a in code.split(".")])
    VoltageL1 = {
        "pos": "32.7.0",
        "byte": to_bytes("01.0.32.7.0.255"),
        "desc_name": "Voltage L1",
        "unit": "V",
        "mod": None,
    }
    VoltageL2 = {
        "pos": "52.7.0",
        "byte": to_bytes("01.0.52.7.0.255"),
        "desc_name": "Voltage L2",
        "unit": "V",
        "mod": "round(self.obis[d['byte']],2)",
    }
    VoltageL3 = {
        "pos": "72.7.0",
        "byte": to_bytes("01.0.72.7.0.255"),
        "desc_name": "Voltage L3",
        "unit": "V",
        "mod": "round(self.obis[d['byte']],2)",
    }
    CurrentL1 = {
        "pos": "31.7.0",
        "byte": to_bytes("1.0.31.7.0.255"),
        "desc_name": "Current L1",
        "unit": "A",
        "mod": "round(self.obis[d['byte']],2)",
    }
    CurrentL2 = {
        "pos": "51.7.0",
        "byte": to_bytes("1.0.51.7.0.255"),
        "desc_name": "Current L2",
        "unit": "A",
        "mod": "round(self.obis[d['byte']],2)",
    }
    CurrentL3 = {
        "pos": "71.7.0",
        "byte": to_bytes("1.0.71.7.0.255"),
        "desc_name": "Current L3",
        "unit": "A",
        "mod": "round(self.obis[d['byte']],2)",
    }
    RealPowerIn = {
        "pos": "1.7.0",
        "byte": to_bytes("1.0.1.7.0.255"),
        "desc_name": "InstantaneousPower In",
        "unit": "W",
        "mod": None,
    }
    RealPowerOut = {
        "pos": "2.7.0",
        "byte": to_bytes("1.0.2.7.0.255"),
        "desc_name": "InstantaneousPower Out",
        "unit": "W",
        "mod": None,
    }
    RealEnergyIn = {
        "pos": "1.8.0",
        "byte": to_bytes("1.0.1.8.0.255"),
        "desc_name": "ActiveEnergy In",
        "unit": "kWh",
        "mod": "self.obis[d['byte']] / 1000",
    }
    RealEnergyOut = {
        "pos": "2.8.0",
        "byte": to_bytes("1.0.2.8.0.255"),
        "desc_name": "ActiveEnergy Out",
        "unit": "kWh",
        "mod": "self.obis[d['byte']] / 1000",
    }
    ReactiveEnergyIn = {
        "pos": "3.8.0",
        "byte": to_bytes("1.0.3.8.0.255"),
        "desc_name": "ReactiveEnergy In",
        "unit": "W",
        "mod": None,
    }
    ReactiveEnergyOut = {
        "pos": "4.8.0",
        "byte": to_bytes("1.0.4.8.0.255"),
        "desc_name": "ReactiveEnergy Out",
        "unit": "W",
        "mod": None,
    }
    Factor = {
        "pos": "13.7.0",
        "byte": to_bytes("01.0.13.7.0.255"),
        "desc_name": "Factor",
        "unit": "",
        "mod": "round(self.obis[d['byte']],3)",
    }
    DeviceNumber = {
        "pos": "96.1.0",
        "byte": to_bytes("0.0.96.1.0.255"),
        "desc_name": "DeviceNumber",
        "unit": "",
        "mod": None,
    }
    LogicalDeviceNumber = {
        "pos": "42.0.0",
        "byte": to_bytes("0.0.42.0.0.255"),
        "desc_name": "LogicalDeviceNumber",
        "unit": "",
        "mod": None,
    }
