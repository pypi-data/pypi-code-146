import numpy as np


class mux:
    def __init__(self, data, config):
        self._data = data
        self._config = config

    def VinA(self):
        return (self._data["Vmux33"] - self._data["Vmux30"]) * 4

    def VinD(self):
        return (self._data["Vmux37"] - self._data["Vmux30"]) * 4

    def VDDA(self):
        return (self._data["Vmux34"] - self._data["Vmux30"]) * 2

    def VDDD(self):
        return (self._data["Vmux38"] - self._data["Vmux30"]) * 2

    def Vofs(self):
        return (self._data["Vmux36"] - self._data["Vmux30"]) * 4

    def VrefOVP(self):
        return (self._data["Vmux32"] - self._data["Vmux30"]) * 3.33

    def IinA(self):
        return (
            (self._data["Imux28"] - self._data["Vmux30"])
            / self._config["RD53B"]["Parameter"].get("R_Imux", 10000.0)
            * self._config["RD53B"]["Parameter"].get("kIinA", 21000.0)
        )

    def IinD(self):
        return (
            (self._data["Imux30"] - self._data["Vmux30"])
            / self._config["RD53B"]["Parameter"].get("R_Imux", 10000.0)
            * self._config["RD53B"]["Parameter"].get("kIinD", 21000.0)
        )

    def IshuntA(self):
        return (
            np.fmax(self._data["Imux29"] - self._data["Vmux30"], 0)
            / self._config["RD53B"]["Parameter"].get("R_Imux", 10000.0)
            * self._config["RD53B"]["Parameter"].get("kIshuntA", 26000.0)
        )

    def IshuntD(self):
        return (
            np.fmax(self._data["Imux31"] - self._data["Vmux30"], 0)
            / self._config["RD53B"]["Parameter"].get("R_Imux", 10000.0)
            * self._config["RD53B"]["Parameter"].get("kIshuntD", 26000.0)
        )

    def IcoreA(self):
        return self.IinA() - self.IshuntA()

    def IcoreD(self):
        return self.IinD() - self.IshuntD()

    def Iin(self):
        return self.IinA() + self.IinD()

    def Iref(self):
        return (self._data["Imux0"] - self._data["Imux63"]) / self._config["RD53B"][
            "Parameter"
        ].get("R_Imux", 10000.0)
